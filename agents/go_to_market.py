"""
GoToMarketAgent
---------------

Assembles a go‑to‑market strategy using prior results (partners,
design, market data).  Advertises the ``go_to_market`` capability.
Responds to DISCOVER, RFP and TASK messages.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent


class GoToMarketAgent(BaseAgent):
    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Builds go‑to‑market campaign plans and assets.",
            "capabilities": ["go_to_market"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=self.get_agent_card()))
        elif env.intent == Intent.RFP:
            proposal = {
                "capability": "go_to_market",
                "eta_days": 2,
                "cost_units": 4,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            region = env.payload.get("region", "global")
            partners = env.payload.get("partners", {})
            timeline = [
                ("Month 1", "Finalize partnerships and approvals"),
                ("Month 2", "Pilot with key suppliers/distributors"),
                ("Month 3", "Full campaign rollout"),
            ]
            assets = {
                "pitch_deck": f"Opportunity in {region}",
                "brochure": "Sustainability‑first value prop",
            }
            channels = ["Online", "Retail", "B2B partner marketing"]
            result = {
                "timeline": timeline,
                "assets": assets,
                "channels": channels,
                "key_partners": partners,
            }
            self.log(f"Compiled go‑to‑market plan for {region}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=result))
        else:
            await super().on_message(env)
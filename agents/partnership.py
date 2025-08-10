"""
PartnershipAgent
----------------

This agent identifies potential suppliers and distributors for a given
region.  It advertises the ``partnerships`` capability.  On DISCOVER
it returns its card; on RFP it proposes a cost/ETA; on TASK it
returns partner lists using the MCP client.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..mcp_client import MCPClient


class PartnershipAgent(BaseAgent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.mcp = MCPClient()

    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Finds suppliers and distributors for partnerships.",
            "capabilities": ["partnerships"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=self.get_agent_card()))
        elif env.intent == Intent.RFP:
            region = env.payload.get("region", "global")
            proposal = {
                "capability": "partnerships",
                "eta_days": 2,
                "cost_units": 3,
                "region": region,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            region = env.payload.get("region", "global")
            partners = self.mcp.partners(region)
            self.log(f"Partners for {region}: {partners}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=partners))
        else:
            await super().on_message(env)
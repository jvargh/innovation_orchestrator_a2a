"""
DesignArchitectAgent
--------------------

Generates product concepts, design assets and user journeys using
customer insights and MCP design assets.  Advertises the
``design_architecture`` capability.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..mcp_client import MCPClient


class DesignArchitectAgent(BaseAgent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.mcp = MCPClient()

    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Creates user journeys and design prototypes.",
            "capabilities": ["design_architecture"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=self.get_agent_card()))
        elif env.intent == Intent.RFP:
            proposal = {
                "capability": "design_architecture",
                "eta_days": 2,
                "cost_units": 3,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            top_requests = env.payload.get("top_requests", [])
            assets = self.mcp.design_assets()
            journey = [f"User need → '{need}'" for need in top_requests]
            journey += [
                "AI recommends sustainable options",
                "User compares footprint & cost",
                "Purchase & onboarding",
            ]
            result = {
                "style": assets["style"],
                "palette": assets["palette"],
                "journey": journey,
            }
            self.log(f"Created design with style {assets['style']} and palette {assets['palette']}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=result))
        else:
            await super().on_message(env)
"""
MarketInsightAgent
------------------

This agent queries the MCP for market trends and competitor information.
During discovery it advertises a card indicating it supports the
``market_insight`` capability and handles RFP and TASK intents.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..mcp_client import MCPClient


class MarketInsightAgent(BaseAgent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.mcp = MCPClient()

    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Collects market trends and competitor intelligence.",
            "capabilities": ["market_insight"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            # Return this agent's card
            card = self.get_agent_card()
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=card))
        elif env.intent == Intent.RFP:
            region = env.payload.get("region", "global")
            proposal = {
                "capability": "market_insight",
                "eta_days": 1,
                "cost_units": 2,
                "region": region,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            region = env.payload.get("region", "global")
            result = self.mcp.market_trends(region)
            self.log(f"Market trends for {region}: {result}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=result))
        else:
            await super().on_message(env)
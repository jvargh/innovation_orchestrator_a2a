"""
CustomerInsightAgent
--------------------

This agent analyzes customer sentiment and user feedback via the MCP.
It advertises the ``customer_insight`` capability.  On receiving a
DISCOVER message it returns its agent card.  For RFP, it proposes
a small cost and timeline.  Upon TASK it returns sentiment data.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..mcp_client import MCPClient


class CustomerInsightAgent(BaseAgent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.mcp = MCPClient()

    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Analyzes customer sentiment and top requests.",
            "capabilities": ["customer_insight"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=self.get_agent_card()))
        elif env.intent == Intent.RFP:
            product = env.payload.get("product", "unknown product")
            proposal = {
                "capability": "customer_insight",
                "eta_days": 1,
                "cost_units": 2,
                "product": product,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            product = env.payload.get("product", "unknown product")
            result = self.mcp.customer_signals(product)
            self.log(f"Customer signals for {product}: {result}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=result))
        else:
            await super().on_message(env)
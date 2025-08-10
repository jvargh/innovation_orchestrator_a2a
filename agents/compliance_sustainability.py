"""
ComplianceSustAgent
-------------------

This agent performs compliance and sustainability assessments via MCP.
It advertises the ``compliance_esg`` capability.  It responds to
DISCOVER, RFP and TASK intents.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..mcp_client import MCPClient


class ComplianceSustAgent(BaseAgent):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.mcp = MCPClient()

    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.address.name,
            "description": "Checks regional regulations and ESG frameworks.",
            "capabilities": ["compliance_esg"],
            "supported_intents": [intent.name for intent in (Intent.DISCOVER, Intent.RFP, Intent.TASK)],
            "endpoints": [self.address.name],
        }

    async def on_message(self, env: Envelope) -> None:
        if env.intent == Intent.DISCOVER:
            await self.send(env.reply(sender=self.address.name, intent=Intent.CARD, payload=self.get_agent_card()))
        elif env.intent == Intent.RFP:
            region = env.payload.get("region", "global")
            proposal = {
                "capability": "compliance_esg",
                "eta_days": 1,
                "cost_units": 2,
                "region": region,
            }
            await self.send(env.reply(sender=self.address.name, intent=Intent.PROPOSE, payload=proposal))
        elif env.intent == Intent.TASK:
            region = env.payload.get("region", "global")
            regs = self.mcp.regulations(region)
            self.log(f"Regulations for {region}: {regs}")
            await self.send(env.reply(sender=self.address.name, intent=Intent.RESULT, payload=regs))
        else:
            await super().on_message(env)
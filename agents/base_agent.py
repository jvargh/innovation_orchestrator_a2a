"""
Base definitions for all agents.

Agents share a common interface for handling messages via the A2A
protocol.  Each agent also exposes an "agent card" describing its
capabilities.  The card is used during discovery so that orchestrators
can determine which agents are available and what they can do.

``AgentContext`` bundles together the address, router and
conversation objects required by agents to communicate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..a2a_protocol import Envelope, Intent, Router, Conversation
from ..registry import Address


@dataclass
class AgentContext:
    """Context passed to each agent upon construction."""

    address: Address
    router: Router
    convo: Conversation
    name: str


class BaseAgent:
    """Abstract base class providing common agent functionality."""

    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self._log: list[str] = []

    @property
    def address(self) -> Address:
        return self.ctx.address

    async def start(self) -> None:
        """Optional hook executed when the agent is started."""
        pass

    async def on_message(self, env: Envelope) -> None:
        """Process an incoming envelope.

        Must be overridden by subclasses.  A default implementation logs
        receipt of unexpected messages.  Agents should use
        ``env.reply`` to send responses.
        """
        self.log(f"Received unhandled {env.intent.name} message from {env.sender}")

    def log(self, message: str) -> None:
        self._log.append(message)
        print(f"[{self.ctx.name}] {message}")

    def logs(self) -> list[str]:
        return self._log

    def get_agent_card(self) -> Dict[str, Any]:
        """Return metadata describing this agent.

        Agent cards advertise capabilities, supported message types,
        descriptions and other operational metadata.  Subclasses
        override this to provide meaningful information.
        """
        return {
            "name": self.address.name,
            "description": "Generic agent with no specific role.",
            "capabilities": [],
            "endpoints": [self.address.name],
        }

    async def send(self, env: Envelope) -> None:
        """Send an envelope via the router."""
        await self.ctx.router.send(env)
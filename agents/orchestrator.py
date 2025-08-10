"""
OrchestratorAgent
-----------------

The orchestrator coordinates specialized agents through the A2A protocol.
It begins by discovering available agents and reading their cards.  Then
it issues RFPs for required capabilities, accepts the first proposal
returned, assigns tasks with appropriate inputs and collects results.

This agent demonstrates a simplified variant of the routing pattern
highlighted in the Microsoft Semantic Kernel blog—albeit without
external Azure dependencies.  It illustrates how A2A flows and MCP
integration can be combined in a modular, extensible system.
"""

from __future__ import annotations

from typing import Any, Dict, List
import asyncio

from .base_agent import BaseAgent
from ..a2a_protocol import Envelope, Intent
from ..registry import Address


class OrchestratorAgent(BaseAgent):
    """Central orchestrator coordinating multi‑step plans across agents."""

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.agent_cards: Dict[str, Dict[str, Any]] = {}

    async def on_message(self, env: Envelope) -> None:
        # The orchestrator handles proposals and results via the
        # conversation helper.  We delegate resolution to the
        # conversation to wake any waiters.
        if env.intent in (Intent.PROPOSE, Intent.RESULT, Intent.CARD):
            # Use correlation id or message id to resolve
            key = env.correlation_id or env.message_id
            self.ctx.convo.resolve(key, env.payload)
        elif env.intent == Intent.INFO:
            # Log informational messages
            self.log(env.payload.get("message", ""))
        else:
            await super().on_message(env)

    async def discover_agents(self, addresses: List[Address]) -> None:
        """Request agent cards from all provided addresses."""
        tasks = []
        for addr in addresses:
            # Send DISCOVER message
            discover_env = Envelope(
                intent=Intent.DISCOVER,
                sender=self.address.name,
                recipient=addr.name,
                payload={},
            )
            # Create a future to wait for the card
            fut = self.ctx.convo.watch(discover_env.message_id)
            await self.send(discover_env)
            tasks.append(fut)
        # Wait for all card responses
        cards = await asyncio.gather(*tasks)
        # Index cards by capability
        for card in cards:
            name = card.get("name", "unknown")
            self.agent_cards[name] = card

    async def _rfp_and_execute(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send RFP, accept the first proposal and send the task.

        Returns the result payload once the agent completes the task.
        """
        # Build and send RFP
        rfp = Envelope(
            intent=Intent.RFP,
            sender=self.address.name,
            recipient=agent_name,
            payload=payload,
        )
        # Wait for proposal
        fut = self.ctx.convo.watch(rfp.message_id)
        await self.send(rfp)
        proposal = await fut
        # Accept the proposal (naive strategy).  Note: create a fresh envelope
        # targeted at the remote agent; do not use rfp.reply here because
        # that would invert sender/recipient.
        accept = Envelope(
            intent=Intent.ACCEPT,
            sender=self.address.name,
            recipient=agent_name,
            correlation_id=rfp.message_id,
            payload=proposal,
        )
        await self.send(accept)
        # Issue task.  Use the same correlation id so that results link back.
        task_env = Envelope(
            intent=Intent.TASK,
            sender=self.address.name,
            recipient=agent_name,
            correlation_id=rfp.message_id,
            payload=payload,
        )
        fut2 = self.ctx.convo.watch(task_env.correlation_id)
        await self.send(task_env)
        result = await fut2
        return result

    async def run_plan(self, *, region: str, product: str, addresses: Dict[str, Address]) -> Dict[str, Any]:
        """Execute the full orchestrated plan.

        Orders calls according to dependencies: customer insights and market
        insights first; compliance and partnerships next; design; then
        go‑to‑market.  Returns a unified dictionary with all results.
        """
        self.log(f"Starting plan for product '{product}' in region '{region}'")
        # Discover cards if not already
        if not self.agent_cards:
            await self.discover_agents(list(addresses.values()))
        # Step 1: market and customer insights concurrently
        market_task = asyncio.create_task(
            self._rfp_and_execute(addresses["market"].name, {"region": region})
        )
        customer_task = asyncio.create_task(
            self._rfp_and_execute(addresses["customer"].name, {"product": product})
        )
        market_info, customer_info = await asyncio.gather(market_task, customer_task)

        # Step 2: compliance and partnerships concurrently
        compliance_task = asyncio.create_task(
            self._rfp_and_execute(addresses["compliance"].name, {"region": region})
        )
        partners_task = asyncio.create_task(
            self._rfp_and_execute(addresses["partnership"].name, {"region": region})
        )
        compliance_info, partners_info = await asyncio.gather(compliance_task, partners_task)

        # Step 3: design using top requests from customer info
        design_info = await self._rfp_and_execute(
            addresses["design"].name, {"top_requests": customer_info.get("top_requests", [])}
        )

        # Step 4: go‑to‑market using region and partners
        gtm_info = await self._rfp_and_execute(
            addresses["gtm"].name, {"region": region, "partners": partners_info}
        )

        plan = {
            "region": region,
            "product": product,
            "market_insights": market_info,
            "customer_insights": customer_info,
            "compliance": compliance_info,
            "partners": partners_info,
            "design": design_info,
            "go_to_market": gtm_info,
        }
        self.log("Plan execution completed")
        return plan
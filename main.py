"""
Main entry point for the Innovation Orchestrator PoC.

This script sets up the in‑process A2A environment, registers
specialized agents and executes a multi‑step plan to derive a
go‑to‑market strategy from a high‑level request.  The demonstration
prints the aggregated plan and logs from each agent.

Usage::

    python main.py
"""

import asyncio

from .a2a_protocol import Router, Conversation
from .registry import Registry
from .agents.base_agent import AgentContext
from .agents.orchestrator import OrchestratorAgent
from .agents.market_insight import MarketInsightAgent
from .agents.customer_insight import CustomerInsightAgent
from .agents.partnership import PartnershipAgent
from .agents.compliance_sustainability import ComplianceSustAgent
from .agents.design_architect import DesignArchitectAgent
from .agents.go_to_market import GoToMarketAgent


import argparse
import json
from typing import Tuple, Optional


async def run_demo(region: str, product: str) -> None:
    """Run the orchestrator demo for a specified region and product.

    This helper function sets up the in‑process A2A environment, registers
    specialized agents and executes a multi‑step plan to derive a
    go‑to‑market strategy from the provided region and product.  It then
    prints the aggregated plan and logs from each agent.

    Args:
        region: Geographic region for the go‑to‑market analysis (e.g., "LATAM").
        product: High‑level description of the solution or product to be analyzed.
    """
    # Initialize communication primitives
    router = Router()
    convo = Conversation()
    registry = Registry()

    # Create addresses
    addr_orch = registry.addr("orchestrator")
    addr_market = registry.addr("market")
    addr_customer = registry.addr("customer")
    addr_partnership = registry.addr("partnership")
    addr_compliance = registry.addr("compliance")
    addr_design = registry.addr("design")
    addr_gtm = registry.addr("gtm")

    # Instantiate agents with context
    orchestrator = OrchestratorAgent(AgentContext(addr_orch, router, convo, "Orchestrator"))
    market = MarketInsightAgent(AgentContext(addr_market, router, convo, "Market Insight"))
    customer = CustomerInsightAgent(AgentContext(addr_customer, router, convo, "Customer Insight"))
    partnership = PartnershipAgent(AgentContext(addr_partnership, router, convo, "Partnership"))
    compliance = ComplianceSustAgent(AgentContext(addr_compliance, router, convo, "Compliance"))
    design = DesignArchitectAgent(AgentContext(addr_design, router, convo, "Design"))
    gtm = GoToMarketAgent(AgentContext(addr_gtm, router, convo, "Go‑to‑Market"))

    # Register agents with the router
    router.register(addr_orch.name, orchestrator.on_message)
    router.register(addr_market.name, market.on_message)
    router.register(addr_customer.name, customer.on_message)
    router.register(addr_partnership.name, partnership.on_message)
    router.register(addr_compliance.name, compliance.on_message)
    router.register(addr_design.name, design.on_message)
    router.register(addr_gtm.name, gtm.on_message)

    # Execute the orchestrated plan
    plan = await orchestrator.run_plan(
        region=region,
        product=product,
        addresses={
            "market": addr_market,
            "customer": addr_customer,
            "partnership": addr_partnership,
            "compliance": addr_compliance,
            "design": addr_design,
            "gtm": addr_gtm,
        },
    )

    # Print the final plan and logs
    print("\n=== Aggregated Plan ===")
    for key, value in plan.items():
        print(f"{key}: {value}")
    print("\n=== Agent Logs ===")
    for agent in [orchestrator, market, customer, partnership, compliance, design, gtm]:
        print(f"-- {agent.ctx.name} --")
        for line in agent.logs():
            print(f"  {line}")


def parse_input(file: Optional[str] = None, region: Optional[str] = None, product: Optional[str] = None) -> Tuple[str, str]:
    """Parse input parameters from a file or direct arguments.

    This helper supports three modes:
    - If a file path is provided, it attempts to read JSON containing
      keys ``region`` and ``product``.
    - If ``region`` and ``product`` arguments are provided, those values
      are used directly.
    - Otherwise, it prompts the user via standard input for region and product.

    Args:
        file: Optional path to a JSON file with ``region`` and ``product`` keys.
        region: Optional region string provided on the command line.
        product: Optional product string provided on the command line.

    Returns:
        A tuple of (region, product).
    """
    # Case 1: explicit region/product from CLI
    if region and product:
        return region, product

    # Case 2: file specified
    if file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("region", "").strip(), data.get("product", "").strip()
        except Exception as e:
            raise SystemExit(f"Failed to read input file '{file}': {e}")

    # Case 3: interactive prompt
    try:
        region = input("Enter the target region: ").strip()
        product = input("Enter the high‑level product/solution description: ").strip()
    except EOFError:
        raise SystemExit("No input provided. Exiting.")
    return region, product


def main() -> None:
    """Entry point for command‑line execution.

    Supports reading the target ``region`` and ``product`` from a JSON file
    via ``--file`` or from individual arguments ``--region`` and
    ``--product``. If neither are provided, prompts the user for the
    values.  Once obtained, it runs the innovation orchestrator.
    """
    parser = argparse.ArgumentParser(description="Run the Innovation Orchestrator PoC")
    parser.add_argument("--file", type=str, help="Path to a JSON file containing 'region' and 'product'")
    parser.add_argument("--region", type=str, help="Target region (e.g., LATAM, APAC, EMEA)")
    parser.add_argument("--product", type=str, help="High‑level description of the product/solution")
    args = parser.parse_args()

    region, product = parse_input(args.file, args.region, args.product)
    if not region or not product:
        raise SystemExit("Both region and product must be provided either via file or arguments.")
    asyncio.run(run_demo(region, product))


if __name__ == "__main__":
    main()
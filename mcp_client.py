"""
Mock implementation of the Model Context Protocol (MCP) client.

In a production environment, the MCP allows agents to access external
tools and data sources—including REST APIs, databases, file systems and
AI models—through a unified interface.  Here we provide deterministic
mocks for market trends, customer sentiment, regulatory information and
design assets.  These mocks return pseudo‑random values to simulate
varying data but remain reproducible due to seeding.
"""

from __future__ import annotations

import random
from typing import Dict


class MCPClient:
    """A simple mock for MCP.  Methods return structured data."""

    rng = random.Random(42)

    def market_trends(self, region: str) -> Dict:
        growth = round(1.05 + self.rng.random() * 0.1, 3)
        return {
            "region": region,
            "growth_rate": growth,
            "competitors": ["Contoso", "Fabrikam", "Globex", "Initech"],
            "trends": ["Circular economy", "Eco-packaging", "Blockchain tracking", "Reverse logistics"],
        }

    def customer_signals(self, product: str) -> Dict:
        sentiments = ["positive", "neutral", "negative"]
        top_needs = [
            "Lower cost",
            "More sustainability",
            "Better usability",
            "Transparent sourcing",
        ]
        return {
            "product": product,
            "average_sentiment": self.rng.choice(sentiments),
            "top_requests": self.rng.sample(top_needs, 3),
        }

    def regulations(self, region: str) -> Dict:
        return {
            "region": region,
            "regulatory_ready": self.rng.random() > 0.15,
            "esg_frameworks": ["GRI", "SASB", "CSRD"],
            "co2_intensity_cap": f"{round(0.8 + self.rng.random() * 0.3, 2)} kg/pack",
        }

    def partners(self, region: str) -> Dict:
        suppliers = [f"Supplier {i}" for i in range(1, 4)]
        distributors = [f"Distributor {i}" for i in range(1, 3)]
        return {
            "region": region,
            "suppliers": suppliers,
            "distributors": distributors,
        }

    def design_assets(self) -> Dict:
        palettes = ["green/blue", "teal/charcoal", "navy/lime"]
        return {
            "palette": self.rng.choice(palettes),
            "style": "modern",
            "components": ["icon set", "illustrations", "presentation template"],
        }
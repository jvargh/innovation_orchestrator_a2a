# Innovation Orchestrator (A2A + MCP) — PoC

_Last updated: Aug 10, 2025_

## Introduction
Innovation Orchestrator is a marketplace‑native, multi‑agent proof‑of‑concept that turns high‑level business objectives into launch‑ready strategies in **days, not months**. It demonstrates how a central orchestrator (inspired by Microsoft Semantic Kernel patterns) coordinates specialized agents via the **Agent‑to‑Agent (A2A)** protocol, while each agent uses a **Model Context Protocol (MCP)** client to pull external context (market data, customer signals, partners, compliance/ESG, design assets).

This PoC showcases the **“Building the Agentic Economy”** vision: agents discover, negotiate, and transact value in a living marketplace, producing integrated outputs (e.g., a go‑to‑market plan) from a single request.

---

## Description
From a request like:
> “Identify and prepare a go‑to‑market plan for a **circular economy supply‑chain solution** in **LATAM**.”

the orchestrator:
1. **Discovers** suitable agents via A2A **Agent Cards**.
2. **Negotiates** with agents (RFP → PROPOSE → ACCEPT).
3. **Assigns tasks** with typed payloads.
4. Agents **fetch data** via MCP (mock client in this PoC).
5. Orchestrator **synthesizes** results into a board‑ready launch plan.

### Business Impact
- **Speed to market**: compresses months of cross‑functional work into days.
- **Stronger product‑market fit**: continuous feedback keeps plans relevant.
- **Scalable capability**: enterprise‑grade outcomes for teams of any size.
- **Risk reduction**: embeds compliance & sustainability from day one.

---

## Functionality (What You Can Do)
- **A2A Messaging**: in‑process router + message envelopes for peer agents.
- **Discovery**: each agent returns a **card** with capabilities & metadata.
- **Negotiation**: RFP/PROPOSE/ACCEPT lifecycle before tasks are executed.
- **Tasking**: orchestrator issues `TASK` with correlation IDs and awaits `RESULT`.
- **MCP Data Access (mocked)**: agents call a custom MCP client for:
  - Market trends & competitors
  - Customer sentiment & top needs
  - Partner discovery (suppliers/distributors)
  - Compliance & ESG snapshots
  - Design assets & user journeys
- **Synthesis**: orchestrator assembles all outputs into a unified plan.

---

## End‑to‑End Flow
1. **Ingestion**: Accept `region` and `product` via **file** (`--file`) or **CLI/interactive** input.
2. **Discovery**: Orchestrator sends `DISCOVER` to agents → receives Agent Cards (capabilities, intents).
3. **RFP Round**: Orchestrator sends `RFP` → agents reply with `PROPOSE` (cost/ETA).
4. **Accept**: Orchestrator sends `ACCEPT` to chosen agent(s).
5. **Task Execution**: Orchestrator sends `TASK` with inputs (e.g., `region`, `product`).
6. **MCP Calls**: Agents invoke the MCP client to fetch external context (mocked here).
7. **Results**: Agents return `RESULT` payloads.
8. **Synthesis**: Orchestrator compiles a **go‑to‑market plan** (market, customers, partners, compliance/ESG, design, launch plan).
9. **Completion**: Final plan is printed (and could be persisted or sent to another system).

---

## Project Structure
```
innovation_orchestrator_a2a/
├─ a2a_protocol.py               # A2A message types, router, conversation helper
├─ mcp_client.py                 # Mock MCP client for external data
├─ registry.py                   # Agent address registry
├─ agents/
│  ├─ base_agent.py              # Base agent + Agent Card
│  ├─ market_insight.py          # Market trends & competitors
│  ├─ customer_insight.py        # Sentiment & top requests
│  ├─ partnership.py             # Suppliers & distributors
│  ├─ compliance_sustainability.py # Regulations & ESG snapshot
│  ├─ design_architect.py        # Concepts, journeys, assets
│  ├─ go_to_market.py            # Timeline, channels, assets
│  └─ orchestrator.py            # Discovery, negotiation, tasking, synthesis
└─ main.py                       # Entrypoint (CLI/file/interactive)
```

---

## Prerequisites
- **Python 3.10+**
- No external dependencies required (pure Python PoC).

> In a production build you would install Semantic Kernel + A2A + MCP clients and replace the in‑process router and mock MCP with real endpoints.

---

## Setup & Run

### 1) Clone and enter the project
```bash
git clone <your-repo-url>.git
cd <your-repo>/innovation_orchestrator_a2a
```

### 2) Provide inputs (three options)

**Option A — JSON file**
Create a file `input.json`:
```json
{
  "region": "LATAM",
  "product": "Circular Supply Chain Solution"
}
```
Run:
```bash
python -m innovation_orchestrator_a2a.main --file input.json
```

**Option B — CLI flags**
```bash
python -m innovation_orchestrator_a2a.main   --region LATAM   --product "Circular Supply Chain Solution"
```

**Option C — Interactive**
```bash
python -m innovation_orchestrator_a2a.main
# You will be prompted for region and product
```

---

## Implementation Notes
- **A2A Protocol**: `a2a_protocol.py` defines `Envelope` and `Intent` with a minimal router. Intents include: `DISCOVER`, `RFP`, `PROPOSE`, `ACCEPT`, `TASK`, `RESULT`, `INFO`, `ERROR`.
- **Agent Cards**: each agent advertises a `card()` describing capability and supported intents (used during discovery).
- **Negotiation**: orchestrator sends `RFP` and awaits `PROPOSE`; it then `ACCEPT`s and issues `TASK` to the target agent.
- **Correlation IDs**: the `Conversation` helper watches correlation IDs so the orchestrator can await specific responses.
- **MCP Client (mock)**: `mcp_client.py` provides deterministic fake data; swap this with real MCP servers (e.g., Azure Functions, data APIs).

---

## Sample Output (single run)
```
[Orchestrator] Starting plan for product 'Circular Supply Chain Solution' in region 'LATAM'
[Market Insight] Market trends for LATAM: {'region': 'LATAM', 'growth_rate': 1.114, 'competitors': ['Contoso', 'Fabrikam', 'Globex', 'Initech'], 'trends': ['Circular economy', 'Eco-packaging', 'Blockchain tracking', 'Reverse logistics']}
[Customer Insight] Customer signals for Circular Supply Chain Solution: {'product': 'Circular Supply Chain Solution', 'average_sentiment': 'positive', 'top_requests': ['Better usability', 'Lower cost', 'Transparent sourcing']}
[Compliance] Regulations for LATAM: {'region': 'LATAM', 'regulatory_ready': False, 'esg_frameworks': ['GRI', 'SASB', 'CSRD'], 'co2_intensity_cap': '0.83 kg/pack'}
[Partnership] Partners for LATAM: {'region': 'LATAM', 'suppliers': ['Supplier 1', 'Supplier 2', 'Supplier 3'], 'distributors': ['Distributor 1', 'Distributor 2']}
[Design] Created design with style modern and palette navy/lime
[Go‑to‑Market] Compiled go‑to‑market plan for LATAM
[Orchestrator] Plan execution completed

=== Aggregated Plan ===
region: LATAM
product: Circular Supply Chain Solution
market_insights: {'region': 'LATAM', 'growth_rate': 1.114, 'competitors': ['Contoso', 'Fabrikam', 'Globex', 'Initech'], 'trends': ['Circular economy', 'Eco-packaging', 'Blockchain tracking', 'Reverse logistics']}
customer_insights: {'product': 'Circular Supply Chain Solution', 'average_sentiment': 'positive', 'top_requests': ['Better usability', 'Lower cost', 'Transparent sourcing']}
compliance: {'region': 'LATAM', 'regulatory_ready': False, 'esg_frameworks': ['GRI', 'SASB', 'CSRD'], 'co2_intensity_cap': '0.83 kg/pack'}
partners: {'region': 'LATAM', 'suppliers': ['Supplier 1', 'Supplier 2', 'Supplier 3'], 'distributors': ['Distributor 1', 'Distributor 2']}
design: {'style': 'modern', 'palette': 'navy/lime', 'journey': ["User need → 'Better usability'", "User need → 'Lower cost'", "User need → 'Transparent sourcing'", 'AI recommends sustainable options', 'User compares footprint & cost', 'Purchase & onboarding']}
go_to_market: {'timeline': [('Month 1', 'Finalize partnerships and approvals'), ('Month 2', 'Pilot with key suppliers/distributors'), ('Month 3', 'Full campaign rollout')], 'assets': {'pitch_deck': 'Opportunity in LATAM', 'brochure': 'Sustainability‑first value prop'}, 'channels': ['Online', 'Retail', 'B2B partner marketing'], 'key_partners': {'region': 'LATAM', 'suppliers': ['Supplier 1', 'Supplier 2', 'Supplier 3'], 'distributors': ['Distributor 1', 'Distributor 2']}}

=== Agent Logs (excerpt) ===
-- Orchestrator --
  Starting plan for product 'Circular Supply Chain Solution' in region 'LATAM'
  Plan execution completed
-- Market Insight --
  Market trends for LATAM: {...}
-- Customer Insight --
  Customer signals for Circular Supply Chain Solution: {...}
-- Partnership --
  Partners for LATAM: {...}
-- Compliance --
  Regulations for LATAM: {...}
-- Design --
  Created design with style modern and palette navy/lime
-- Go‑to‑Market --
  Compiled go‑to‑market plan for LATAM
```

---

## Roadmap / Next Steps
- Replace mock MCP with real MCP servers (Azure Functions, data APIs).
- Swap in‑process router with a message bus (Azure Service Bus, Kafka).
- Add agent **reputation, pricing, and bidding** to proposals.
- Incorporate **Semantic Kernel** planners & plugins for richer orchestration.
- Persist plans and artifacts to storage; add a simple web UI for demos.

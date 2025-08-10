# Innovation Orchestrator (A2A + MCP) - Hackathon '25 - PoC

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
# How to Run Innovation Orchestrator (File Input & Interactive Input)

Below is a complete example showing two ways to run the **Innovation Orchestrator**:
- Using a **JSON input file**
- Using **manual (interactive) input**

The sample outputs illustrate each stage: **ingestion**, agents using the mock **MCP** to fetch data, **agentic (A2A) chatter** logs, and the **final aggregated plan**.

---

## 1) Using a file as input

Create a JSON file (e.g., `input.json`) with the region and product:

```json
{
  "region": "APAC",
  "product": "Sustainable Packaging Solution"
}
```

Run the orchestrator with the file:

```bash
python3 -m innovation_orchestrator_a2a.main --file input.json
```

**Sample output:**

```text
[Orchestrator] Starting plan for product 'Sustainable Packaging Solution' in region 'APAC'
[Market Insight] Received unhandled ACCEPT message from orchestrator
[Market Insight] Market trends for APAC: {...}  ← uses MCP to fetch market data
[Customer Insight] Received unhandled ACCEPT message from orchestrator
[Customer Insight] Customer signals for Sustainable Packaging Solution: {...}  ← uses MCP to fetch sentiment data
[Compliance] Received unhandled ACCEPT message from orchestrator
[Compliance] Regulations for APAC: {...}  ← uses MCP to fetch regulations/ESG data
[Partnership] Received unhandled ACCEPT message from orchestrator
[Partnership] Partners for APAC: {...}  ← uses MCP to find suppliers/distributors
[Design] Received unhandled ACCEPT message from orchestrator
[Design] Created design with style modern and palette navy/lime  ← uses MCP to pull design assets
[Go‑to‑Market] Received unhandled ACCEPT message from orchestrator
[Go‑to‑Market] Compiled go‑to‑market plan for APAC
[Orchestrator] Plan execution completed

=== Aggregated Plan ===
region: APAC
product: Sustainable Packaging Solution
market_insights: {...}
customer_insights: {...}
compliance: {...}
partners: {...}
design: {...}
go_to_market: {...}

=== Agent Logs ===
-- Orchestrator --
  Starting plan for product 'Sustainable Packaging Solution' in region 'APAC'
  Plan execution completed
-- Market Insight --
  Received unhandled ACCEPT message from orchestrator
  Market trends for APAC: {...}
-- Customer Insight --
  Received unhandled ACCEPT message from orchestrator
  Customer signals for Sustainable Packaging Solution: {...}
-- Partnership --
  Received unhandled ACCEPT message from orchestrator
  Partners for APAC: {...}
-- Compliance --
  Received unhandled ACCEPT message from orchestrator
  Regulations for APAC: {...}
-- Design --
  Received unhandled ACCEPT message from orchestrator
  Created design with style modern and palette navy/lime
-- Go‑to‑Market --
  Received unhandled ACCEPT message from orchestrator
  Compiled go‑to‑market plan for APAC
```

**Step through the flow:**

- **Ingestion:** The `--file` flag tells the orchestrator to load the `region` and `product` from `input.json`.
- **MCP access:** Each agent invokes the mock MCP client to fetch its domain data (market trends, customer signals, regulations, partners, design assets) before returning results.
- **Agentic chatter:** The log lines beginning “Received unhandled ACCEPT message…” and the subsequent “Market trends for …” represent the A2A lifecycle (**RFP → PROPOSE → ACCEPT → TASK → RESULT**).
- **Result:** The orchestrator aggregates all agent results into a unified plan and prints both the plan and each agent’s log.

---

## 2) Using manual (interactive) input

Run the orchestrator without flags:

```bash
python3 -m innovation_orchestrator_a2a.main
```

When prompted, enter values like:

```text
Enter the target region:  LATAM
Enter the high‑level product/solution description:  Circular Supply Chain Solution
```

**Sample output (abridged):**

```text
[Orchestrator] Starting plan for product 'Circular Supply Chain Solution' in region 'LATAM'
[Market Insight] Market trends for LATAM: {...}
[Customer Insight] Customer signals for Circular Supply Chain Solution: {...}
[Compliance] Regulations for LATAM: {...}
...
[Go‑to‑Market] Compiled go‑to‑market plan for LATAM
[Orchestrator] Plan execution completed

=== Aggregated Plan ===
region: LATAM
product: Circular Supply Chain Solution
market_insights: {...}
customer_insights: {...}
...
```

The process is identical to the file‑based run: the orchestrator collects `region` and `product` from the user, kicks off the same A2A negotiation/communication sequence, uses MCP for data, and finishes with a consolidated plan.


---

## Roadmap / Next Steps
- Replace mock MCP with real MCP servers (Azure Functions, data APIs).
- Swap in‑process router with a message bus (Azure Service Bus, Kafka).
- Add agent **reputation, pricing, and bidding** to proposals.
- Incorporate **Semantic Kernel** planners & plugins for richer orchestration.
- Persist plans and artifacts to storage; add a simple web UI for demos.

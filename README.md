# Day 8 — Multi-Agent Merchant Intelligence Crew

## What this builds
A 3-agent CrewAI crew that analyses merchant performance data, generates pricing recommendations, and drafts personalised outreach emails — in both sequential and hierarchical execution modes.

## Business problem
Merchants with declining order frequency and high SLA breach rates need targeted intervention. A blanket discount is lazy. The right intervention is the smallest one that changes behaviour — and it needs to feel human, not automated.

## Architecture

```
Coverage Analyst
→ reads merchant CSV data
→ calculates severity scores per merchant
→ produces structured report with root cause classification

        ↓ (output passed as context)

Pricing Optimizer
→ receives analyst report
→ designs optimal incentive per segment (BYOC vs Platform)
→ shows ROI case for every recommendation (Rs 350 AOV, 18% margin)

        ↓ (both outputs passed as context)

Merchant Comms Specialist
→ receives analyst report + pricing recommendations
→ drafts personalised outreach email per priority merchant
→ references merchant-specific zone, order numbers, courier type
→ never uses generic templates
```

## Agents

| Agent | Role | Tools |
|---|---|---|
| Coverage Analyst | Senior Merchant Coverage Analyst | read_merchant_data, calculate_severity_score |
| Pricing Optimizer | Merchant Pricing Strategist | None — reasons from context |
| Merchant Comms | Merchant Communications Specialist | None — reasons from context |
| Manager Agent | Crew Manager (hierarchical mode only) | Delegation only |

## Severity scoring model

Each merchant is scored 0–100 across two dimensions:

- **Order trend score (max 50)** — percentage decline from weeks 1–2 average to week 3
- **SLA score (max 50)** — SLA breach rate × 100, capped at 50

| Score | Label |
|---|---|
| 60–100 | CRITICAL |
| 35–59 | HIGH |
| 15–34 | MEDIUM |
| 0–14 | LOW |

## Execution modes

### Sequential
Tasks run in hardcoded order. Output of each task passed as context to the next.
- Predictable and debuggable
- You are the manager — all delegation decisions made at design time
- Lower token cost — no routing layer

### Hierarchical (guided)
A Manager Agent reads every task brief before delegating to specialists.
- Manager honours pre-assigned agents but adds a reasoning layer
- Adds routing tax — latency and token cost per task
- True autonomous hierarchical value only appears when agent assignment and task order are left fully to the Manager

## Key findings from this build

- Sequential mode produced clean execution — all 3 priority merchants covered in correct order
- Hierarchical mode: Manager read every task brief before delegating — confirmed pre-assigned agents rather than making autonomous decisions
- Guided hierarchical (explicit ordering in Manager goal) is the most production-appropriate mode — full autonomy introduces unpredictable failure modes
- Context passing quality determines downstream output quality — structured expected outputs are contracts between agents

## Tech stack

- CrewAI 1.14.6
- OpenAI GPT-4o
- Python 3.13

## Mock data

10 Mumbai merchants across zones including Andheri East, Bandra West, Powai, Dharavi, Juhu, Andheri West, Borivali, Kurla, Malad, Thane. Mix of BYOC and Platform courier types.

Declining merchants (intentionally built into data): M002 Mumbai Tiffins, M004 Curry House, M006 Noodle Bar, M008 Dosa Point.

## How to run

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Add your API key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here
```

### Run
```bash
venv/bin/python main.py
```
Choose 1 for sequential, 2 for hierarchical.

## Output files
- `output_sequential.txt` — full sequential crew output
- `output_hierarchical.txt` — full hierarchical crew output

## Project structure

```
ai_d8/
├── agents.py          # Agent definitions — role, goal, backstory, tools
├── tasks.py           # Task definitions — description, expected output, context
├── tools.py           # Tool functions — read_merchant_data, calculate_severity_score
├── main.py            # Crew assembly and execution
├── data/
│   └── merchants.csv  # Mock merchant performance data
├── output_sequential.txt
├── output_hierarchical.txt
├── requirements.txt
└── README.md
```

## PM mental models from this build

- **Agent design is org design** — vague role definition produces inconsistent work, same as a vague job description
- **Task expected output is your acceptance criteria** — without it the agent decides what done looks like
- **Context passing is your handoff document** — its quality determines downstream output quality
- **Separation of concerns** — agents.py, tasks.py, tools.py, main.py each have one job
- **Hierarchical mode adds a routing tax** — only worth it when delegation decisions are genuinely complex
- **Give agents minimum tools needed** — every extra tool is a decision point where the agent can make a wrong call
- **Guided hierarchical > pure hierarchical for production** — full Manager autonomy introduces unpredictable failure modes


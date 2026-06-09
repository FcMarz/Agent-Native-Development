# 🏟️ Simulation Arena — Cooperative Agent Debate & Consensus Testbed

> Cycle 02, Milestone A | Agent-Native Development Laboratory

## Purpose

The Simulation Arena is a **multi-agent debate sandbox** where specialized agent roles negotiate research consensus on a given topic. Instead of a single agent planning in a loop, three distinct personas engage in structured rounds:

| Role | Persona | Objective |
|:-----|:--------|:----------|
| **🐂 Bull** | The Advocate | Argues *for* the strategic importance of the entity/trend. Highlights opportunities, growth vectors, and moats. |
| **🐻 Bear** | The Skeptic | Argues *against* hype. Identifies risks, substitution threats, unsustainable economics, and structural weaknesses. |
| **⚖️ Arbitrator** | The Judge | Synthesizes both positions into a scored consensus verdict with a confidence level and actionable recommendation. |

## Architecture

```
simulation_arena/
├── README.md                    # This file
├── config.json                  # Debate topics and engine settings
├── roles/                       # Agent role prompt templates
│   ├── bull.md                  # Bull advocate system prompt
│   ├── bear.md                  # Bear skeptic system prompt
│   └── arbitrator.md            # Arbitrator judge system prompt
├── engine.py                    # Core debate orchestrator
├── backends/                    # LLM backend adapters
│   ├── __init__.py
│   ├── mock_backend.py          # Deterministic mock for testing
│   └── ollama_backend.py        # Ollama local model adapter (future)
├── debates/                     # Output: completed debate transcripts
│   └── .gitkeep
└── run_debate.py                # CLI entry point
```

## How It Works

1. **Topic Injection**: A research topic (e.g., "Skyfire Agent Payments") is loaded from `config.json` or passed via CLI.
2. **Round 1 — Opening Statements**: Bull and Bear each produce their opening argument.
3. **Round 2 — Rebuttal**: Each agent reads the other's opening and produces a targeted rebuttal.
4. **Round 3 — Verdict**: The Arbitrator reads all four arguments and produces a structured consensus report with scores.
5. **Output**: The full debate transcript is saved to `debates/` as a timestamped markdown file.

## Backends

| Backend | Status | Description |
|:--------|:-------|:------------|
| `mock` | ✅ Active | Deterministic template-based responses for testing |
| `ollama` | 🔜 Planned | Local LLM inference via Ollama API |
| `api` | 🔜 Planned | Remote API (OpenAI-compatible) |

## Usage

```bash
# Run a debate with the mock backend
python3 WORKSPACE/simulation_arena/run_debate.py --topic "Skyfire Agent Payments"

# Run with a specific backend
python3 WORKSPACE/simulation_arena/run_debate.py --backend mock --topic "MCP Protocol"
```

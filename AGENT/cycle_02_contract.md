# Cycle 2 Agent Contract: Simulation, Evaluation, & Optimization

This contract defines the operational parameters, templates, and execution guidelines for Cycle 2 research sprints.

---

## 🎯 Cycle 2 Targets
1. **Debate Scope**: Sprints consist of exactly **4 topics** (debates) per research run.
2. **Evaluation Coordinates**: The Evaluator Agent maps coordinates dynamically onto the Strategic Position Matrix using composite mathematical scaling.
3. **Audit Constraints**: All generated field notes must clear the `HeuristicCritic` loop in `run_03_critic_loop.py` prior to publication.

---

## 🔬 Core Protocols
* **Routing Standard**: Agents must invoke the entry point `agent.py` to negotiate goals.
* **Context Budget**: Standard execution threads must limit initial injected file context to <20KB (using Level 1 and 2 progressive disclosure) to preserve token budget.
* **Local Recovery (Escape Hatch)**: When encountering system failures (e.g. out of memory, full disk), agents are authorized to allocate a temporary 20% free-form context window, run diagnostics like `SERVICES/cleanup_memory.sh` autonomously, recover system stability, and resume stateful execution.

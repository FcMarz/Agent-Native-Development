# Agent Guidelines: Meta-Orchestration & Dual-Routing Model

Welcome to the Agent Room. This directory contains instructions, cycle contracts, and operational guidelines for autonomous agents operating in this workspace.

---

## 🎯 Core Mission
Your goal is to conduct high-fidelity research on **Agent-Native Development, Architectures, and Startups**. You must prioritize discovering patterns, best practices, and strategic shifts in the market.

---

## 🔀 Meta-Routing & Task Execution
To balance execution rigor and cognitive flexibility, the workspace implements a **Dual-Routing System** managed by `agent.py`:

1. **Meta-Agent (Strategic Planner)**:
   - Collaborates with the Human User to define new research runs and compile findings.
   - Negotiates and designs **Cycle-Specific Contracts** stored in the `AGENT/` folder (e.g. `AGENT/cycle_02_contract.md`).
2. **Stateful Pipeline Execution (`STATEFUL PIPELINE MODE`)**:
   - Standard execution steps (running simulations, compiling reports, updating index files) are statefully tracked in `.agent/state.json`.
   - Context injection uses the **Progressive Disclosure Principle** (loading only specific manifest dependencies) to minimize token expenditure.
3. **Ad-Hoc Sandbox Execution (`FREE-FORM SANDBOX MODE`)**:
   - Complex debugging, troubleshooting, and environmental errors are routed to free-form mode.
   - During stateful execution, a **20% free-form context escape hatch** is pre-authorized to recover from failures (like out-of-memory or port collisions) before returning control to the pipeline.

---

## ✍️ Formatting & Archiving Standards
* **Field Notes**: Profile individual entities following the templates defined in cycle contracts.
* **Interim Reports**: Compiled and placed in `ARCHIVE/cycle_XX/` (e.g. `ARCHIVE/cycle_02/`).
* **Version Control**: Every significant step (run debates, evaluation, report compilation, state update) must be captured in a Git commit.

# Empirical Evaluation & Self-Healing Guidelines

This document outlines metrics and diagnostics guidelines for analyzing the performance, robustness, and resource footprint of the multi-agent system.

---

## 📊 Empirical Metrics & Rubric

In computer science studies, agentic pipelines should be evaluated quantitatively. The following metrics are implemented in this repository to track efficiency and compliance:

### 1. Context Bloat Efficiency ($E_{ctx}$)
Measures the percentage of workspace context saved by using **Progressive Disclosure Context Routing** over loading the entire workspace:

$$E_{ctx} = \left( 1 - \frac{\text{Manifest Context Size (KB)}}{\text{Full Workspace Size (KB)}} \right) \times 100\%$$

* **Baseline Target**: $> 80\%$ context reduction.
* **Why it matters**: Keeping context sizes below 20KB prevents LLM attention drift and reduces cost.

### 2. Loop Convergence Rate ($C_{loop}$)
Measures how many turns the Writer-Critic loop needs to satisfy all formatting, link, and length requirements:

$$C_{loop} = \text{Audit Iterations before Approval}$$

* **Excellent**: $C_{loop} = 1$ (Passes on the first attempt).
* **Satisfactory**: $C_{loop} \le 3$.
* **Stalled**: $C_{loop} > 5$ (Triggers automatic fallback warning).

### 3. Token Cost Index ($TCI$)
Tracks the total tokens consumed per research sprint:

$$TCI = \text{Debate Tokens} + \text{Evaluator Tokens} + \left( C_{loop} \times \text{Audit Loop Tokens} \right)$$

---

## 🛡️ Self-Healing & Diagnostic Protocols

When running autonomous agents on hardware, physical resource bounds (like memory leaks or disk overflow) will occur. The **Escape Hatch Protocol** handles this:

### OOM & Cache Cleansing Loop
1. The orchestrator detects a standard exit code failure or exception.
2. If `FREE-FORM SANDBOX MODE` is triggered via the escape hatch, the agent invokes:
   ```bash
   ./SERVICES/cleanup_memory.sh
   ```
3. This script performs three critical functions:
   - Identifies and terminates runaway Python or Node processes.
   - Clears OS-level page caches and releases unused virtual memory.
   - Prunes temporary cache files from `.tempmediaStorage/` and web caches.
4. Once system state returns to healthy levels, the agent resumes execution.

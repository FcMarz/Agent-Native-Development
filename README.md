# Agent-Native Development Laboratory

Welcome to the **Agent-Native Development Laboratory**, an autonomous research sandbox and diagnostic engineering workspace designed to evaluate next-generation agent architectures, frameworks, and developer tooling.

---

## 📂 Repository Structure

```
├── AGENT/                  # Meta-guidelines and Cycle-specific Contracts (e.g. cycle_02_contract.md)
├── ARCHIVE/                # Historical Interim and Final Insight Reports
├── GOVERNANCE/             # Rules of engagement and human-agent boundary contracts
├── LOGS/                   # Session diaries tracking git commits and run activities
├── PROJECT_MANAGEMENT/     # Configuration files and strategic matrix coordinates
├── SERVICES/               # Backend scripts (intake server, evaluators, critics, static UI dashboard)
└── WORKSPACE/              # Active research sandbox (simulation arena configs, transcripts, field notes)
```

---

## 🤖 Orchestration & The Dual-Routing Model

The workspace utilizes a root-level coordinator [agent.py](./agent.py) to manage agent sessions statefully and cost-effectively:

### 1. Stateful Pipeline Mode
Standard operational tasks (like running debate sandboxes or compiling findings) are tracked step-by-step in `.agent/state.json`. Context injection utilizes a **Progressive Disclosure Principle** (via `.agent/context_manifest.json`) to load only the required file dependencies for the active step, saving >70% on token budgets.

### 2. Free-Form Sandbox Mode (Escape Hatch)
Unforeseen execution blockages (like port conflicts, memory exhaustion, or critic audit errors) are routed to free-form mode. During stateful execution, the agent has a pre-authorized **20% free-form context escape hatch** to crawl diagnostic logs, run scripts, and recover system stability before returning control to the pipeline.

### 🛠️ Execution Commands
* **Check Stateful Task Status**:
  ```bash
  ./agent.py status
  ```
* **Execute active step**:
  ```bash
  ./agent.py run <step_index>
  ```
* **Test router logic**:
  ```bash
  ./agent.py route "debug memory timeout"
  ```
* **Run A/B simulation test**:
  ```bash
  ./agent.py ab-test
  ```
* **Run Hybrid Router Stress Test**:
  ```bash
  ./agent.py stress-test
  ```

---

## 📚 CS Case Study Documentation
* **System Architecture**: Read [architecture.md](./FIELDNOTES/architecture.md) for dataflow diagrams, progressive disclosure mechanisms, and multi-agent debate design patterns.
* **Empirical Evaluation Metrics**: Read [evaluation.md](./FIELDNOTES/evaluation.md) to study context reduction calculations, loop convergence rates, and self-healing protocols.

---

## 📈 Dashboard & Verification
* **Start the Intake Server**:
  Launch the backend server to host API endpoints and serve static assets:
  ```bash
  python3 SERVICES/input_server.py
  ```
  By default, the server runs on [http://localhost:8484](http://localhost:8484). (To run on a custom port, pass it as an argument: `python3 SERVICES/input_server.py <port>`).
* **Access the Findings Board**:
  Navigate to [http://localhost:8484/board](http://localhost:8484/board) (or open [board.html](./SERVICES/static/board.html) directly) in a web browser to inspect the interactive **Strategic Positioning Matrix** and play back research progress step-by-step.
* **Resource Cleaner**: Run [cleanup_memory.sh](./SERVICES/cleanup_memory.sh) to inspect memory, diagnose dangling sub-processes, or drop page caches via `--clean`.

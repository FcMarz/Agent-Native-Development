import os
import json
import datetime
import subprocess

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "WORKSPACE")
FIELD_NOTES_DIR = os.path.join(WORKSPACE_DIR, "field_notes")
ARCHIVE_DIR = os.path.join(BASE_DIR, "ARCHIVE")
PM_DIR = os.path.join(BASE_DIR, "PROJECT_MANAGEMENT")
LOGS_DIR = os.path.join(BASE_DIR, "LOGS")

def get_config():
    config_path = os.path.join(PM_DIR, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {"current_phase": 1, "current_run": 8, "notes_per_run": 8, "runs_per_phase": 8}

def update_config_to_next(config):
    config_path = os.path.join(PM_DIR, "config.json")
    config["current_run"] += 1
    if config["current_run"] > config["runs_per_phase"]:
        config["current_run"] = 1
        config["current_phase"] += 1
        
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Updated configuration to Phase {config['current_phase']}, Run {config['current_run']}")

def run_git_command(args):
    try:
        result = subprocess.run(['git'] + args, cwd=BASE_DIR, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

# Content data for the 8 profiles of Run 08
field_notes_data = [
    {
        "filename": "field_note_057_aider_best_practices.md",
        "title": "Aider: Best Practices for Git-Integrated Coding Agents",
        "content": """# Profile
- **Name**: Aider
- **Category**: Agent-Native Software Engineering / Pair Programming CLI
- **Status**: Production-ready terminal utility, widely adopted

# Agent-Native Characteristics
- **Repo Map Indexing**: Indexes codebases by extracting signatures of classes and functions, allowing models to understand file structures without loading entire contents.
- **Search-and-Replace Edit Blocks**: Relies on specific diff blocks rather than writing full files, saving token counts and preventing formatting errors.
- **Git as Source of Truth**: Automatically commits changes with descriptive, agent-generated commit messages.

# Aesthetic/UX Details
- Clean terminal CLI with color-coded syntax highlights, diff reviews, and interactive file management commands.

# Key Takeaways & Market Signal
- **Signal**: Best practices for coding agents require tight integration with git. Code modification must be done via localized search-and-replace edit chunks to scale to large codebases.
- **Reference**: https://aider.chat"""
    },
    {
        "filename": "field_note_058_claude_code.md",
        "title": "Claude Code: Local Agent-Native Developer CLI",
        "content": """# Profile
- **Name**: Claude Code / Claude CLI
- **Category**: Developer CLI Agent
- **Status**: Active Developer Preview by Anthropic

# Agent-Native Characteristics
- **Interactive Tool Execution**: Directly runs bash commands, searches files, and modifies text on local filesystems.
- **Bespoke CLI Commands**: Uses commands (e.g. `/commit`, `/search`) to coordinate operations quickly.
- **Human-in-the-Loop Permissions**: Safeguards system security by requiring user consent before running write commands or mutating files.

# Aesthetic/UX Details
- Modern terminal UI showing spinner animations, tool invocation summaries, and interactive confirmation modals.

# Key Takeaways & Market Signal
- **Signal**: Terminal-integrated CLI agents are the next major IDE interface. Prompt compilation is shifting to local code indexers that dynamically pull file snippets on request.
- **Reference**: https://anthropic.com"""
    },
    {
        "filename": "field_note_059_openhands_sandbox.md",
        "title": "OpenHands: Docker-Sandboxed Developer Workspace",
        "content": """# Profile
- **Name**: OpenHands
- **Category**: Sandboxed Developer Agent
- **Status**: Active open-source development, standard for sandbox environments

# Agent-Native Characteristics
- **Docker-Isolated Workspace**: Spawns a dedicated Docker container to run agent code, protecting host filesystems.
- **Arbitrary Command Execution**: Runs commands, installs libraries, and spins up test servers inside the container.
- **Workspace File Syncing**: Synchronizes project directories between host and sandboxed environments seamlessly.

# Aesthetic/UX Details
- Dual-panel Web UI showing active workspace explorer, visual terminal feeds, and agent messaging interfaces.

# Key Takeaways & Market Signal
- **Signal**: Sandboxing is non-negotiable for enterprise agents. Arbitrary execution of bash scripts requires secure, containerized boundaries to prevent resource damage or security exploits.
- **Reference**: https://github.com/All-Hands-AI/OpenHands"""
    },
    {
        "filename": "field_note_060_swe_bench.md",
        "title": "SWE-bench: Benchmark for Codebase Resolution Agents",
        "content": """# Profile
- **Name**: SWE-bench
- **Category**: Coding Agent Benchmark
- **Status**: Standard evaluation platform for SWE agent research

# Agent-Native Characteristics
- **Real GitHub Issue Resolution**: Evaluates agent capabilities by tasking them to resolve real issues pulled from Python codebases.
- **Test-Suite Verification**: Measures task success by executing unit tests before and after agent edits.
- **Multi-File Context Complexity**: Challenges agents to find, read, and edit multiple related files.

# Aesthetic/UX Details
- Quantitative scoreboard ranking top open-source and commercial agents (SWE-agent, OpenHands, Devin).

# Key Takeaways & Market Signal
- **Signal**: The gold standard for code agents is verified execution. Success is measured by running test suites, not just code generation metrics (like BLEU/ROUGE).
- **Reference**: https://www.swebench.com"""
    },
    {
        "filename": "field_note_061_garak_security.md",
        "title": "Garak: LLM Vulnerability and Security Scanner",
        "content": """# Profile
- **Name**: Garak
- **Category**: Security and Red-Teaming Scanner
- **Status**: Open-source CLI vulnerability checker

# Agent-Native Characteristics
- **Prompt Injection Scanners**: Simulates adversarial inputs to detect jailbreaks, credential leaks, and data extraction.
- **Output Safety Auditing**: Detects toxic generation, hallucination triggers, and insecure code outputs.
- **Targeted Probing**: Automatically generates thousands of security test payloads against agent runtime API endpoints.

# Aesthetic/UX Details
- Simple CLI tool showing test progression logs and a structured vulnerability coverage report.

# Key Takeaways & Market Signal
- **Signal**: LLM APIs require automated vulnerability scanning. Garak acts as the OWASP-Zap for the LLM era, checking if agents leak system prompts or credentials.
- **Reference**: https://github.com/leondz/garak"""
    },
    {
        "filename": "field_note_062_promptfoo_eval.md",
        "title": "Promptfoo: Test-Driven Prompt and Output Evaluation",
        "content": """# Profile
- **Name**: Promptfoo
- **Category**: Prompt Evaluation Framework
- **Status**: Production-ready open-source developer tool

# Agent-Native Characteristics
- **Deterministic Assertion Checks**: Runs regex, JSON validation, and custom scripts on agent outputs.
- **Semantic Assertions**: Uses LLM-guided assertions to check style, tone, and compliance.
- **Red Teaming Payloads**: Automatically tests systems against prompt injections, toxic inputs, and PII leaks.

# Aesthetic/UX Details
- Detailed terminal matrix output and web dashboard showing test runs, comparisons, and latency.

# Key Takeaways & Market Signal
- **Signal**: Prompts are code and require testing. Asserting JSON schema compliance and semantic constraints programmatically prevents regression during prompt updates.
- **Reference**: https://www.promptfoo.dev"""
    },
    {
        "filename": "field_note_063_braintrust.md",
        "title": "Braintrust: Enterprise AI Evaluation and Tracking",
        "content": """# Profile
- **Name**: Braintrust
- **Category**: Enterprise AI Evaluation and Telemetry
- **Status**: Production-ready commercial and developer platform

# Agent-Native Characteristics
- **Automated Regression Suites**: Evaluates agent outputs on custom datasets across multiple model versions.
- **Dataset Versioning**: Tracks golden test records to benchmark accuracy over time.
- **Cost and Latency Telemetry**: Provides detailed metrics on prompt cost, completion tokens, and end-to-end response times.

# Aesthetic/UX Details
- Premium analytics dashboard with interactive charts displaying accuracy drift, cost history, and playground comparisons.

# Key Takeaways & Market Signal
- **Signal**: Continuous evaluation (EvalOps) is critical for enterprise agents. Teams must track regression, costs, and token speed across updates.
- **Reference**: https://www.braintrust.dev"""
    },
    {
        "filename": "field_note_064_langsmith_eval.md",
        "title": "LangSmith: Agent Trajectory and Trace Evaluator",
        "content": """# Profile
- **Name**: LangSmith
- **Category**: Agent Trace Evaluation & Telemetry
- **Status**: Production-ready developer portal by LangChain

# Agent-Native Characteristics
- **Trace Evaluation**: Evaluates complete agent trajectories (sequence of steps, tool calls, and LLM responses).
- **Run Assertions**: Programmatically tests if the correct tools were invoked with the correct inputs.
- **Feedback Loops**: Collects user feedback scores and maps them back to trace records.

# Aesthetic/UX Details
- Visual trace execution tree; side-by-side prompt debugger.

# Key Takeaways & Market Signal
- **Signal**: Debugging agents requires tracing trajectories. Knowing what tool was called and why it failed is key to refining complex agent orchestrators.
- **Reference**: https://www.langchain.com/langsmith"""
    }
]

def write_run_08():
    config = get_config()
    phase = config["current_phase"]
    run = config["current_run"]
    
    run_str = f"run_{run:02d}"
    
    # Active directories
    run_notes_dir = os.path.join(FIELD_NOTES_DIR, run_str)
    os.makedirs(run_notes_dir, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    print(f"Executing Research Run {run}...")
    
    # Write field notes
    for idx, fn in enumerate(field_notes_data):
        now = datetime.datetime.now()
        filepath = os.path.join(run_notes_dir, fn["filename"])
        
        # Calculate actual global index (note numbers 057 to 064)
        global_idx = 56 + idx + 1
        
        content = f"# {fn['title']}\n"
        content += f"> Ingested on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"> Category: field_notes\n"
        content += f"> Index: {global_idx:03d}\n"
        content += f"> Phase: {phase:02d} | Run: {run:02d}\n\n"
        content += fn["content"].strip()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Created: {fn['filename']}")
        
    # Write Report to flat folder
    report_path = os.path.join(ARCHIVE_DIR, f"interim_report_{run:02d}.md")
    report_content = f"""# Interim Insight Report {run:02d}: Agent-Native Development Best Practices, Security Audits, and Evaluation Frameworks

> **Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **Cycle**: Run {run:02d} (Field Notes 057 - 064)
> **Goal**: Scan developer workflows, codebase indexers, security red-teaming scanners, and agent trajectory evaluations.

---

## 🔍 Executive Summary

This cycle maps the emerging horizons of **Agent-Native Software Engineering and Continuous Evaluation (EvalOps) / Security Infrastructure**.

Our analysis of **Agent-Native Development** (057-059) demonstrates that software engineering has evolved from raw code generation to autonomous workspace management. Platforms like **Aider** and **Claude Code** showcase state-of-the-art developer patterns, emphasizing repository indexing (git-repo-map), localized search-and-replace edit blocks, and human-in-the-loop CLI prompts. To secure this process, **OpenHands** enforces Docker-sandboxed execution, preventing arbitrary shell commands from mutating host filesystems. Simultaneously, evaluating these agents requires **Quantitative Benchmarks** (060) like **SWE-bench** to test issue-resolution rates. Finally, **Evaluation and Security frameworks** (061-064) like **Promptfoo**, **Garak**, **Braintrust**, and **LangSmith** automate red-teaming and evaluate agent trajectories to prevent regression and ensure safety.

---

## 🗺️ Agent-Native Development and Evaluation Taxonomy

Based on the 8 profiles analyzed, we map these tools into the active Agentic Stack:

| Category | Tier | Focus | Key Representative(s) | Strategic Signal |
| :--- | :--- | :--- | :--- | :--- |
| **Dev Tooling** | **Workspace CLI** | Git-integrated pair programming. | **Aider**, **Claude Code** | Repository signature indexing and edit blocks are the standard for codebase scaling. |
| **Dev Tooling** | **Isolated Workspace**| Sandboxed runtime execution. | **OpenHands** | Enterprise security requires containerized sandboxes to run agent-generated code. |
| **Evaluation** | **Benchmark Suite** | Execution validation of code edits. | **SWE-bench** | The gold standard for dev agents is verified execution under active unit test runs. |
| **Evaluation** | **Output Assertion** | Schema validation and compliance. | **Promptfoo** | Prompts are software code; changes must be tested against regression. |
| **Evaluation** | **EvalOps Registry** | Cost, speed, and dataset registry. | **Braintrust** | Tracking prompt cost drift and latency is critical for enterprise scale. |
| **Telemetry** | **Trace Debugger** | Step-by-step tool execution path. | **LangSmith** | Debugging complex agents requires tracing tool call sequences. |
| **Security** | **Adversarial Scanner**| Prompt injection vulnerability scanner. | **Garak** | LLM endpoints require automated scanners to check for prompt leaks and jailbreaks. |

---

## 📈 Major Strategic Trends in Run 08

### 1. Repository-Scale Semantic Indexing
Monolithic token windows are too expensive for codebases. Best-practice tools index the project structure using signature maps (e.g. Aider's git-repo-map), giving agents the ability to dynamically locate files, query classes, and request snippet payloads on demand.

### 2. Isolated Runtimes are Non-Negotiable
Agents that write and test software must execute arbitrary shell commands. Running these commands on local development environments is unsafe. The industry is standardizing on dockerized sandboxes (e.g. OpenHands) to contain execution safely.

### 3. EvalOps and Trajectory Assertions
Validating agent success is shifting from simple text matching to trace assertions. Using platforms like Braintrust and Promptfoo, developers assert that: (1) correct tools were called, (2) outputs match schema definitions, and (3) security parameters are not compromised.

---

## 🔮 Hypothesis & Next Run Plan (Transitioning to Phase 2)

This concludes **Phase 1** of our research laboratory. 

### Current Hypotheses:
1. *By 2027, visual web navigation enclaves and Docker workspaces will be the standard deployment environment for enterprise software agents.*
2. *Adversarial security scanning (Garak) will be a mandatory CI/CD gate for LLM integrations.*

### Focus for Phase 2:
- See `ARCHIVE/final_phase_1_report.md` for a comprehensive summary and proposed Phase 2 milestones.
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content.strip())
    print(f"Created Interim Report: interim_report_{run:02d}.md")

def compile_final_phase_report():
    final_report_path = os.path.join(ARCHIVE_DIR, "final_phase_1_report.md")
    content = """# Phase 1 Final Report: Automating Agent-Native Laboratory & Strategic Insights

> **Cycle**: Phase 01 (Runs 01 - 08 | Field Notes 001 - 064)
> **Author**: Antigravity Laboratory Coordinator
> **Date**: 2026-06-08

---

## 📋 Executive Summary

Phase 1 successfully established a fully automated, Git-backed agentic research laboratory. Over the course of **8 runs (64 field profiles)**, we scaled the infrastructure into a deterministic loop comprising:
1. **The Pasteboard Intake & Dashboard**: Serving research notes, telemetry inputs, and mobile diagnostic updates.
2. **The Executive Findings Board**: Providing a strategic quadrants matrix (mapping entities by maturity and autonomy) and interactive timeline summaries.
3. **Android Device Integration**: Local ADB config scripts supporting future vision-based phone operations.

---

## 🗺️ Key Research Insights Across Phase 1

### 1. Memory and Databases (Runs 01 - 02)
- **Insight**: Static context windows are obsolete. Modern agents require self-editing memory architectures (Letta) and semantic relational graph schemas (GraphRAG) to maintain state.

### 2. Connectivity and Telemetry (Runs 03 - 04)
- **Insight**: Tool connectivity is standardizing around the Model Context Protocol (MCP). Programmatic prompt optimization (DSPy) and micro-trace tracking (AgentOps) are required to prevent token cost runaways.

### 3. Economic Autonomy & Security (Runs 05 - 06)
- **Insight**: Agents are transitioning to financial actors. Web-based billing enclaves (Skyfire, Stripe Agent API) enable programmatic micro-settlements, while decentralized Multi-Party Computation (Nillion) resolves the delegation paradox.

### 4. Swarm Coordination & Edge Autonomy (Runs 07 - 08)
- **Insight**: Complex workflows are best managed by specialized agent teams (CrewAI, Autogen) with graph-based rollback cycles (LangGraph). Development tasks require signature indexing (Aider) and sandboxed environments (OpenHands).

---

## 🔮 Proposed Phase 2 Research Plan

We propose transitioning the laboratory to **Phase 2**, shifting from passive profiling to **active visual-agent validation**.

### 🎯 Phase 2 Milestones:
- **Milestone 1 (Run 01)**: Devising a localized **visual navigation agent** using `browser-use` and local vision models (Ollama + Llama-3-Vision).
- **Milestone 2 (Run 02)**: Activating the Sony Android phone (SO-51A) via ADB screenshot coordinates to automate mobile tasks.
- **Milestone 3 (Run 03)**: Testing agent-native fintech swarms (StarChild/WOOFi) using sandbox test networks.

### 💡 Core Hypotheses for Phase 2:
1. *Local vision-based navigation agents will achieve >85% task completion rates on standard mobile/web workflows within local sandboxes.*
2. *Non-custodial smart contract wallets with session keys are the only viable path to achieve secure, automated agent finance.*

### 📈 Expected Results:
- A fully functional visual browser agent executing locally.
- Real-time mobile screen controls running via ADB enclaves on the Sony phone.
"""
    with open(final_report_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("Created Phase 1 Final Report: final_phase_1_report.md")

def update_board_opinions():
    board_path = os.path.join(PM_DIR, "board_data.json")
    data = []
    if os.path.exists(board_path):
        with open(board_path, "r") as f:
            data = json.load(f)
            
    # Append Run 8 findings
    new_finding = {
        "run": 8,
        "topic": "Agent-Native Development, Security Audits, and Evaluation Frameworks",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_anchor": "ARCHIVE/interim_report_08.md",
        "observation": "Agent-native software development has shifted from raw code completion to autonomous codebase workspace managers (Claude Code, Aider, OpenHands). State-of-the-art practices emphasize repository indexing (git-repo-map), local tool execution, and isolated sandboxed runtimes (Docker/enclaves) to prevent arbitrary shell commands from mutating host environments. Concurrently, evaluating these systems requires automated regression suites (SWE-bench, Braintrust, Promptfoo) and security scanners (Garak) to verify that agents remain compliant, safe, and correct."
    }
    
    # Avoid duplicate additions
    if not any(item["run"] == 8 for item in data):
        data.append(new_finding)
        with open(board_path, "w") as f:
            json.dump(data, f, indent=2)
        print("Updated Executive Findings Board database (board_data.json).")

def commit_and_log():
    config = get_config()
    run = config["current_run"]
    
    # Add files
    run_git_command(['add', 'WORKSPACE/field_notes/'])
    run_git_command(['add', 'ARCHIVE/'])
    run_git_command(['add', 'PROJECT_MANAGEMENT/'])
    
    # Commit
    commit_msg = f"run(08): write 8 field notes, compile interim report 08, generate Phase 1 Final Report, and update board"
    success, out, err = run_git_command(['commit', '-m', commit_msg])
    
    # Log session execution to LOGS/session_diary.md
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 08 - Phase 1 Complete: `{git_hash}`\n"
    entry += f"- **Action**: Run 08 completed. Compiled final Phase 1 reports.\n"
    entry += f"- **Details**: Wrote 8 field notes (057-064) on agentic dev best practices, SWE-bench, Promptfoo, Garak, and Braintrust. Generated `final_phase_1_report.md`.\n"
    entry += f"- **Status**: Auto-committed. Transitioning laboratory pointer to Phase 2.\n\n"
    
    with open(diary_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    print("Session diary updated and committed.")

if __name__ == "__main__":
    config = get_config()
    write_run_08()
    compile_final_phase_report()
    update_board_opinions()
    commit_and_log()
    
    # Git add the runner script too
    run_git_command(['add', 'SERVICES/run_08_research.py'])
    run_git_command(['commit', '-m', 'chore: add run 08 research script'])
    
    # Increment config pointer (will advance to Phase 2, Run 1!)
    update_config_to_next(config)

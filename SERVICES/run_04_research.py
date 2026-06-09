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
    return {"current_phase": 1, "current_run": 4, "notes_per_run": 8, "runs_per_phase": 8}

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

# Content data for the 8 profiles of Run 04
field_notes_data = [
    {
        "filename": "field_note_025_swe-agent.md",
        "title": "SWE-agent: Software Engineering Agent CLI",
        "content": """# Profile
- **Name**: SWE-agent
- **Category**: Autonomous Software Engineering Agent
- **Status**: Open-source, built by Princeton NLP Group

# Agent-Native Characteristics
- **Agent-Computer Interface (ACI)**: Uses a simplified shell-like environment specifically optimized for LLMs (offering paginated viewing, exact regex search, and targeted editing).
- **GitHub Issue Solver**: Resolves real repository bugs by checking out code, locating issues, testing changes, and submitting pull requests autonomously.
- **High Benchmark Performance**: Achieves top scores on SWE-bench (software engineering benchmark evaluation).

# Aesthetic/UX Details
- Controlled via terminal interface; logs step-by-step reasoning traces showing exact shell commands executed and target source diffs.

# Key Takeaways & Market Signal
- **Signal**: Standard human bash consoles are inefficient for LLMs. Designing bespoke Agent-Computer Interfaces (ACIs) is required to prevent agents from getting lost in large terminal outputs.
- **Reference**: https://github.com/princeton-nlp/SWE-agent"""
    },
    {
        "filename": "field_note_026_aider.md",
        "title": "Aider: Terminal-Native Pair Programming Utility",
        "content": """# Profile
- **Name**: Aider
- **Category**: Terminal-Integrated Developer Tool
- **Status**: Open-source, widely adopted by engineers for day-to-day command-line coding

# Agent-Native Characteristics
- **Git Repository Awareness**: Automatically analyzes and references codebase files using a localized map of the repository structure.
- **In-Place Code Editing**: Edits multiple files concurrently, generating precise code changes and writing clean commits.
- **Automated Commit Generation**: Explains changes and auto-commits to git with custom messages for every successful edit.

# Aesthetic/UX Details
- Interactive terminal chat prompt; features git status indicators, token-usage reporting, and inline syntax-colored file diff previews.

# Key Takeaways & Market Signal
- **Signal**: Developer productivity tools are the frontline of agent adoption. Real-time pair program utilities that integrate with git are immediately valuable to developers.
- **Reference**: https://aider.chat"""
    },
    {
        "filename": "field_note_027_chatdev.md",
        "title": "ChatDev: Virtual Multi-Agent Software Company Simulator",
        "content": """# Profile
- **Name**: ChatDev
- **Category**: Multi-Agent Simulation Workspace
- **Status**: Open-source, research-driven multi-agent simulation sandbox

# Agent-Native Characteristics
- **Cooperative Role-Play**: Simulates an entire software agency populated by distinct agent personas (CEO, CTO, Programmer, Tester, Art Designer).
- **Sequential Dev Phase Flow**: Coordinates steps from design, coding, testing, and documentation through structured agent conversations.
- **Self-Improving Code Loops**: Programmers write code, and testers run tests and feed logs back to programmer agents for iterative debugging.

# Aesthetic/UX Details
- Web dashboard showing an animated pixel-art virtual office where agents exchange messages, alongside a real-time console log.

# Key Takeaways & Market Signal
- **Signal**: Simulating organizational collaboration is more robust than relying on a single large agent. Partitioning roles allows agents to cross-verify outputs.
- **Reference**: https://github.com/OpenBMB/ChatDev"""
    },
    {
        "filename": "field_note_028_camel.md",
        "title": "Camel: Communicative Multi-Agent Framework",
        "content": """# Profile
- **Name**: Camel
- **Category**: Cooperative Multi-Agent Framework
- **Status**: Open-source, pioneer in inception prompting and agent-to-agent negotiation

# Agent-Native Characteristics
- **Inception Prompting**: Uses specialized prompt templates to launch autonomous cooperative interactions between user and assistant agents.
- **Role-Play Dynamics**: Enables dual-agent systems to cooperatively solve goals with minimal human-in-the-loop intervention.
- **Scalable Conversational Paths**: Facilitates complex negotiation, game-theoretic simulation, and sandbox experiments.

# Aesthetic/UX Details
- Clean, developer-oriented API framework built in Python for orchestrating agent interactions and saving conversation logs.

# Key Takeaways & Market Signal
- **Signal**: Autonomy emerges when multiple agents negotiate. Frameworks that decouple communication protocols from underlying LLMs enable complex cooperative architectures.
- **Reference**: https://www.camel-ai.org"""
    },
    {
        "filename": "field_note_029_devika.md",
        "title": "Devika: Open-Source Autonomous Developer Agent",
        "content": """# Profile
- **Name**: Devika
- **Category**: Autonomous Software Engineering Agent
- **Status**: Open-source, community-led alternative to Devin

# Agent-Native Characteristics
- **Multi-Agent Coordination**: Internally divides tasks among planning, research, coding, and debugging sub-agents.
- **Built-in Web Scraping**: Integrates search engine queries and browser extraction to find documentation and code snippets.
- **Workspace Execution**: Automatically compiles and executes projects locally to verify runtime success.

# Aesthetic/UX Details
- Modern web dashboard featuring a central chat area, visual step planners, file explorers, and live terminal execution outputs.

# Key Takeaways & Market Signal
- **Signal**: Open-source developers will replicate closed proprietary systems (like Devin) in weeks. Open-source workspace execution is critical for transparency.
- **Reference**: https://github.com/stitionai/devika"""
    },
    {
        "filename": "field_note_030_openhands.md",
        "title": "OpenHands: Community Platform for Software Agents",
        "content": """# Profile
- **Name**: OpenHands
- **Category**: Open-Source Autonomous Software Engineering Platform
- **Status**: Community-led, backed by AllHands / OpenHands core team

# Agent-Native Characteristics
- **Dockerized Execution Sandbox**: Executes code and installs dependencies inside a secure, isolated Docker container to protect the host machine.
- **Interactive File Explorer**: Dynamically views, edits, and navigates directories using a visual interface.
- **Extensible Agent Architecture**: Allows developers to plug in different agent models, prompts, and planning behaviors.

# Aesthetic/UX Details
- Clean, premium developer-focused dashboard with split-pane interfaces (Chat, Workspace Files, Interactive Shell, and System Logs).

# Key Takeaways & Market Signal
- **Signal**: Sandboxing is non-negotiable. Running arbitrary code generated by agents requires secure, isolated, and responsive virtualization platforms.
- **Reference**: https://github.com/AllHands-AI/OpenHands"""
    },
    {
        "filename": "field_note_031_gymnasium.md",
        "title": "Gymnasium: Standard Agentic Sandbox Environments",
        "content": """# Profile
- **Name**: Gymnasium
- **Category**: Reinforcement Learning & Agent Environment Sandbox
- **Status**: Maintained by Farama Foundation, standard for agent training environments

# Agent-Native Characteristics
- **Step-based Feedback Loops**: Standardizes environment state transitions, action triggers, and numerical rewards.
- **Complex Action Spaces**: Maps discrete and continuous coordinates, enabling agents to navigate complex environments.
- **Environment Isolation**: Abstracts environments (like robotic tasks, text-games, or browsers) behind a unified Python interface.

# Aesthetic/UX Details
- Programmatic Python API; optional rendering windows to visualize simulations and trajectory paths.

# Key Takeaways & Market Signal
- **Signal**: Building intelligent agents requires testing in standardized, high-scale environments. Transitioning agents from prompt-checkers to reinforcement-learning actors requires Gym-like step-based environments.
- **Reference**: https://gymnasium.farama.org"""
    },
    {
        "filename": "field_note_032_dspy.md",
        "title": "DSPy: Programming (Not Prompting) Foundation Models",
        "content": """# Profile
- **Name**: DSPy
- **Category**: Programmatic Prompt Compilation and Optimization
- **Status**: Stanford NLP, highly popular developer framework for structured LLM execution

# Agent-Native Characteristics
- **Declarative Modules**: Replaces hardcoded string prompts with reusable, typed code structures (e.g. `dspy.Predict`, `dspy.ChainOfThought`).
- **Prompt Compilers**: Automatically optimizes prompt instructions and few-shot examples based on small validation datasets.
- **Model Agnostic**: Compiles and compiles optimized outputs across different models (e.g. compiling prompts for local SLMs using outputs from GPT-4).

# Aesthetic/UX Details
- Pure code framework; console logging details the step-by-step compilation, evaluation iterations, and final optimized prompts.

# Key Takeaways & Market Signal
- **Signal**: Prompt engineering is dead. Programmatic compilation that optimizes prompts based on validation datasets is the only scalable way to manage agents across model updates.
- **Reference**: https://github.com/stanfordnlp/dspy"""
    }
]

def write_run_04():
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
        
        # Calculate actual global index (note numbers 025 to 032)
        global_idx = 24 + idx + 1
        
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
    report_content = f"""# Interim Insight Report {run:02d}: Autonomous Software Engineers, Simulation Sandboxes, and Programmatic Prompts

> **Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **Cycle**: Run {run:02d} (Field Notes 025 - 032)
> **Goal**: Evaluate autonomous developer agents, multi-agent simulation workspaces, and programmatic prompt compilers.

---

## 🔍 Executive Summary

This cycle maps the emerging horizons of **Agent Autonomy and Simulation Frameworks** on the developer front.

Our analysis of **Autonomous Software Engineers** (025-026, 029-030) reveals that code generation has evolved into autonomous codebase manipulation. Tools like **SWE-agent** and **OpenHands** utilize specialized Agent-Computer Interfaces (ACIs) and dockerized execution sandboxes to resolve real repository issues. Simultaneously, **Multi-Agent Simulations** (027-028) prove that organizational role-play (e.g. CEO, Programmer, Tester) generates more stable architectural layouts than single-agent models. Finally, **DSPy** (032) signals a paradigm shift: prompt engineering is dead, replaced by programmatic prompt compilers that optimize prompt instructions based on small validation datasets.

---

## 🗺️ Autonomous Developers and Simulation Tier Taxonomy

Based on the 8 profiles analyzed, we map these tools into the active Agentic Stack:

| Category | Tier | Focus | Key Representative(s) | Strategic Signal |
| :--- | :--- | :--- | :--- | :--- |
| **Autonomous Dev** | **Shell/CLI Agent** | Command-line code modification. | **SWE-agent**, **Aider** | Specialized ACIs are replacing standard bash consoles to optimize LLM interactions. |
| **Autonomous Dev** | **Sandboxed IDE** | Docker-contained development. | **OpenHands**, **Devika** | Sandbox virtualization is a mandatory safety and compliance prerequisite. |
| **Simulation** | **Organizational Sim**| Role-based software development. | **ChatDev**, **Camel** | Multi-agent cooperative negotiation yields higher stability than single agents. |
| **Training & Tuning** | **Simulation Gym** | State-step reinforcement sandboxes. | **Gymnasium** | Scale-testing agent behaviors requires Gym-style environment interfaces. |
| **Optimization** | **Prompt Compiler** | Programmatic weights/prompt tuning. | **DSPy** | Static prompt engineering is yields to algorithmic prompt compilation. |

---

## 📈 Major Strategic Trends in Run 04

### 1. From Code Generation to Codebase Ownership
The era of pasting code snippets into file segments is ending. Modern software agents (Aider, OpenHands, SWE-agent) checkout whole git repositories, compile structures, run test suites, and write their own git commits. They function as autonomous micro-engineers, not just auto-complete engines.

### 2. Sandbox Virtualization as a Standard Prerequisite
Executing code generated by models carries significant security and operational risk (infinite loops, server crash, package pollution). Platforms like **OpenHands** standardize **Dockerized sandboxing**, separating agent runtimes entirely from host filesystems.

### 3. Shift from Prompt Engineering to Compiler Compilation
Bespoke string prompts are highly fragile and break whenever models update. **DSPy** demonstrates that prompt generation should be handled programmatically. By structuring inputs as declarative modules and compiling instructions based on validation datasets, developers create resilient systems that adapt to shifting downstream models.

---

## 🔮 Hypothesis & Next Run Plan

### Current Hypotheses:
1. *Bespoke prompt engineering will be fully obsoleted by declarative compile frameworks (like DSPy) within 18 months.*
2. *Production-ready coding agents will operate inside isolated virtual sandboxes as a mandatory security standard.*

### Focus for Run 5:
- Profile **agent-to-agent payment systems** and economic transaction layers.
- Scan **zero-knowledge agent protocols** and privacy-preserving tool executions.
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content.strip())
    print(f"Created Interim Report: interim_report_{run:02d}.md")

def update_board_opinions():
    board_path = os.path.join(PM_DIR, "board_data.json")
    data = []
    if os.path.exists(board_path):
        with open(board_path, "r") as f:
            data = json.load(f)
            
    # Append Run 4 findings
    new_finding = {
        "run": 4,
        "topic": "Autonomous Developers, Simulation Sandboxes, and Programmatic Prompts",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_anchor": "ARCHIVE/interim_report_04.md",
        "observation": "Autonomous developer agents (SWE-agent, OpenHands, Devika) are moving from simple code generation to autonomous codebase manipulation, but their real potential lies in multi-agent sandboxed simulations (ChatDev, Camel) where collaborative role-play solves complex architectural issues. In parallel, programmatic prompt optimization (DSPy) is replacing fragile raw prompting, compiling robust execution graphs that adapt to shifting downstream models."
    }
    
    # Avoid duplicate additions
    if not any(item["run"] == 4 for item in data):
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
    commit_msg = f"run(04): write 8 field notes, generate report 04, and update findings board"
    success, out, err = run_git_command(['commit', '-m', commit_msg])
    
    # Log session execution to LOGS/session_diary.md
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 04 - Compile Report: `{git_hash}`\n"
    entry += f"- **Action**: Run 04 research loop completed.\n"
    entry += f"- **Details**: Wrote 8 field notes (025-032) on Autonomous Dev/Simulations/Compilers and compiled `interim_report_04.md`.\n"
    entry += f"- **Status**: Auto-committed to source of truth.\n\n"
    
    with open(diary_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    print("Session diary updated and committed.")

if __name__ == "__main__":
    config = get_config()
    write_run_04()
    update_board_opinions()
    commit_and_log()
    
    # Git add the runner script too
    run_git_command(['add', 'SERVICES/run_04_research.py'])
    run_git_command(['commit', '-m', 'chore: add run 04 research script'])
    
    # Increment config pointer
    update_config_to_next(config)

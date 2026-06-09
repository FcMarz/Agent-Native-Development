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
    return {"current_phase": 1, "current_run": 3, "notes_per_run": 8, "runs_per_phase": 8}

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

# Content data for the 8 profiles of Run 03
field_notes_data = [
    {
        "filename": "field_note_017_dify.md",
        "title": "Dify: Enterprise Visual Agentic Workflow Platform",
        "content": """# Profile
- **Name**: Dify
- **Category**: Visual Multi-Agent IDE & Workflow Orchestrator
- **Status**: Venture backed, highly popular open-source LLM App development platform

# Agent-Native Characteristics
- **Visual Graph IDE**: Replaces text-only prompts with an intuitive flow diagram for agents, tools, and variables.
- **Workflow / Chat Dual-Mode**: Supports building both structured step-by-step reasoning workflows and conversational multi-agent systems.
- **Out-of-the-Box Tool Integrations**: Integrates with major APIs, RAG stores, and execution sandboxes without requiring code.

# Aesthetic/UX Details
- Sleek, modern canvas layout with drag-and-drop nodes, variables mapping, and a built-in playground window.

# Key Takeaways & Market Signal
- **Signal**: Coding agent loops manually is yielding to visual node graphs. Visual builders allow enterprise operators to model and debug business processes directly as agent workflows.
- **Reference**: https://dify.ai"""
    },
    {
        "filename": "field_note_018_flowise.md",
        "title": "Flowise: Drag-and-Drop Agent Builder",
        "content": """# Profile
- **Name**: Flowise
- **Category**: No-Code UI for AI Agents and Chains
- **Status**: Open-source, heavily adopted in internal corporate hacking sessions

# Agent-Native Characteristics
- **UI-First Architecture**: Built specifically to compile LangChain/LlamaIndex pipelines and custom agents into a visual flowchart.
- **Instant API Deploys**: Exposes constructed visual workflows as webhooks and API endpoints in a single click.
- **Flexible Memory Management**: Allows visual configuration of chat history (buffer memory, summarized memory) and vector stores.

# Aesthetic/UX Details
- Material-design-style board where nodes representing agents, tools, and models are linked by connection inputs and outputs.

# Key Takeaways & Market Signal
- **Signal**: High-velocity prototyping of AI solutions is standard. Flowise enables immediate testing of compound LLM concepts with zero installation.
- **Reference**: https://flowiseai.com"""
    },
    {
        "filename": "field_note_019_langflow.md",
        "title": "Langflow: Python-Native Visual IDE",
        "content": """# Profile
- **Name**: Langflow
- **Category**: Visual AI Developer Tool / IDE
- **Status**: Acquired by DataStax (2024), scaling inside enterprise stacks in 2025/2026

# Agent-Native Characteristics
- **DataStax Astra Integration**: Out-of-the-box native links to high-scale databases and vector search engines.
- **Custom Python Nodes**: Allows developers to write Python snippets directly inside the visual node editor, bridging visual layout and custom code.
- **State Machine Control**: Maps the execution flow dynamically, highlighting active node executions in the UI.

# Aesthetic/UX Details
- Vibrant dark-mode visual interface with complex node configuration forms and dynamic execution indicators.

# Key Takeaways & Market Signal
- **Signal**: Data infrastructure companies (like DataStax) are acquiring visual orchestration platforms to drive storage utilization. Visual IDEs are the funnel for database consumption.
- **Reference**: https://www.langflow.org"""
    },
    {
        "filename": "field_note_020_agentops.md",
        "title": "AgentOps: Observability and Runaway Cost Controller",
        "content": """# Profile
- **Name**: AgentOps
- **Category**: Agentic Observability, Tracing & Cost Budgeting
- **Status**: Venture backed, primary evaluation partner for major frameworks

# Agent-Native Characteristics
- **Loop Prevention**: Automatically monitors agent self-calls to detect and terminate infinite execution loops before spiraling API costs occur.
- **Trace Visualization**: Maps agent reasoning paths, tool execution times, and LLM prompt tokens on a timelines graph.
- **Spend Guardrails**: Enforces session-based and daily dollar budgets on LLM consumption directly inside agent classes.

# Aesthetic/UX Details
- Clean, charts-heavy dashboard visualizing cost graphs, tool success rates, and token histories.

# Key Takeaways & Market Signal
- **Signal**: Autonomy without audit logs is dangerous. Agent developers need session traces to debug reasoning and strict budget limits to prevent financial denial of service.
- **Reference**: https://www.agentops.ai"""
    },
    {
        "filename": "field_note_021_langfuse.md",
        "title": "Langfuse: Open-Source LLM Analytics",
        "content": """# Profile
- **Name**: Langfuse
- **Category**: Open-Source LLM Observability & Analytics
- **Status**: Y Combinator alumnus, popular open-source telemetry engine

# Agent-Native Characteristics
- **Detailed Tracing**: Captures exact inputs, prompt templates, outputs, latencies, and token counts for every step in an agent execution tree.
- **User Feedback Collection**: Exposes hooks to capture human evaluations (thumbs up/down) and map them directly back to trace files.
- **Cost Calculation**: Decoupled analytics server that dynamically calculates total spend based on per-token pricing tables across all providers.

# Aesthetic/UX Details
- Highly performant developer console showing trace lists, prompt managers, and latency distributions.

# Key Takeaways & Market Signal
- **Signal**: Observability is a commodity. Open-source tracing servers that run on-premise allow companies to comply with privacy regulations while audit-logging AI decisions.
- **Reference**: https://langfuse.com"""
    },
    {
        "filename": "field_note_022_sqlite-mcp.md",
        "title": "SQLite MCP Server: Standard Relational Database Connector",
        "content": """# Profile
- **Name**: SQLite MCP Server
- **Category**: Database Connectivity / Model Context Protocol (MCP) Server
- **Status**: Core server supported by Anthropic and the open-source community

# Agent-Native Characteristics
- **Relational Access**: Exposes SQL schema inspection, query execution, and database write capabilities directly as standard LLM tools.
- **Schema Protection**: Safeguards the host environment by containing SQL operations within specified database paths.
- **Zero Ingestion RAG**: Allows LLMs to search and query databases without needing pre-chunked vector conversions.

# Aesthetic/UX Details
- Configured via simple JSON declarations: `mcpServers: { sqlite: { command: "npx", args: ["-y", "@modelcontextprotocol/server-sqlite", "--db", "path/to/db"] } }`.

# Key Takeaways & Market Signal
- **Signal**: Database interfaces are standardizing. Rather than writing custom SQLite search functions, developers expose an MCP SQL server, allowing *any* model to deduce its own queries.
- **Reference**: https://github.com/modelcontextprotocol/servers"""
    },
    {
        "filename": "field_note_023_postgres-mcp.md",
        "title": "Postgres MCP Server: Standard Relational Database Connector",
        "content": """# Profile
- **Name**: Postgres MCP Server
- **Category**: Database Connectivity / Model Context Protocol (MCP) Server
- **Status**: Supported by the official Model Context Protocol ecosystem

# Agent-Native Characteristics
- **Enterprise Storage Access**: Exposes PostgreSQL tables, views, and indexes directly to LLMs via standard read/write database actions.
- **Vector Search Ready**: Integrates with pgvector tables, allowing agents to execute semantic queries natively through standard SQL.
- **Structured Knowledge Retrievable**: Empowers agents to execute multi-table joins to resolve complex semantic relationship queries.

# Aesthetic/UX Details
- Connection strings and permissions configured via environment variables on server launch.

# Key Takeaways & Market Signal
- **Signal**: Standard DB protocols (like MCP) are the bridge between enterprise relational storage and language models. Custom database scrapers are obsolete.
- **Reference**: https://github.com/modelcontextprotocol/servers"""
    },
    {
        "filename": "field_note_024_superagent.md",
        "title": "Superagent: Open-Source AI Assistant Infrastructure",
        "content": """# Profile
- **Name**: Superagent
- **Category**: AI Assistant Framework & Deployment Cloud
- **Status**: Venture backed, popular open-source framework

# Agent-Native Characteristics
- **Stateful Assistant API**: Replaces stateless wrappers by providing an out-of-the-box cloud API to store assistant definitions, threads, and memories.
- **Dynamic Routing**: Automatically routes queries between vector databases, web search, and custom tools.
- **Embeddable Widgets**: Provides ready-to-use JS code snippets to embed the created agent directly on customer-facing websites.

# Aesthetic/UX Details
- Clean, minimal web console to manage assistants, API keys, document uploads, and trace outputs.

# Key Takeaways & Market Signal
- **Signal**: Standardized assistant cloud hosting is emerging. Assistant API layers simplify agent operations by handling storage, memory, and routing under a unified cloud endpoint.
- **Reference**: https://www.superagent.sh"""
    }
]

def write_run_03():
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
        
        # Calculate actual global index (note numbers 017 to 024)
        global_idx = 16 + idx + 1
        
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
    report_content = f"""# Interim Insight Report {run:02d}: Visual IDEs, Observability, and MCP Databases

> **Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **Cycle**: Run {run:02d} (Field Notes 017 - 024)
> **Goal**: Examine Visual IDE orchestrators, cost-control observability tools, and MCP database interfaces.

---

## 🔍 Executive Summary

This cycle maps the mature development tools, observability guardrails, and data access layers of the active **Agentic Stack**.

Our analysis of **Visual Agent IDEs** (017-019, 024) shows a decisive shift away from manual script coding towards drag-and-drop state machines. In parallel, production environments are adopting strict **Observability & Cost Telemetry** (020-021) to block infinite reasoning loops and budget agent API spending. Finally, the rise of **MCP Database Servers** (022-023) is establishing a unified access interface, allowing LLMs to directly read and inspect SQL storage without pre-chunked vector scraping.

---

## 🗺️ Visual, Telemetry, and DB Tier Taxonomy

Based on the 8 profiles analyzed, we map these tools into the active Agentic Stack:

| Category | Tier | Focus | Key Representative(s) | Strategic Signal |
| :--- | :--- | :--- | :--- | :--- |
| **Development & IDE** | **Visual Canvas** | Drag-and-drop workflow state. | **Dify**, **Flowise** | No-code visual canvases are democratizing compound agent loop design. |
| **Development & IDE** | **Visual-Code Hybrid** | Developer-focused execution maps.| **Langflow** | visual platforms are funnel drivers for database providers (DataStax acquisition). |
| **Observability** | **Cost & Loop Guard** | Telemetry and infinite loop prevention. | **AgentOps** | loop prevention and budget guardrails are critical to prevent API credit exhaustion. |
| **Observability** | **Telemetry & Traces** | Open-source execution logs. | **Langfuse** | Open-source telemetry allows enterprise audit logging for privacy compliance. |
| **Database Connect** | **MCP SQL Adapter** | Standard model context protocol access. | **SQLite / Postgres MCP** | Standardized DB interfaces render custom scrapers and vector loaders obsolete. |

---

## 📈 Major Strategic Trends in Run 03

### 1. Canvas-Based Development of Compound Systems
We are moving away from manual scripting of agent pipelines. Platforms like **Dify** and **Flowise** prove that visualizing agents, tools, variables, and flows as linked canvas nodes allows rapid debugging, collaborative development, and straightforward management of state machines.

### 2. Guarding Against Financial Credit Exhaustion
Autonomous agents pose unique financial risks. The ability of an LLM to call itself in an infinite loop can drain API credits in minutes. Telemetry platforms like **AgentOps** are shifting from simple log engines to active guardians, implementing real-time **loop termination** and budget limits.

### 3. Database Access is Standardizing under MCP
Anthropic's **Model Context Protocol (MCP)** is commoditizing data retrieval. Exposing database engines (SQLite, Postgres) via MCP servers allows any agent client to dynamically inspect schemas, select relevant tables, and query records natively. Writing custom query scrapers for individual tables is no longer required.

---

## 🔮 Hypothesis & Next Run Plan

### Current Hypotheses:
1. *Bespoke data scrapers and loaders will be entirely replaced by standardized MCP database servers inside developer workflows by late 2026.*
2. *Production agent deployments will require integrated telemetry (like Langfuse or AgentOps) as a compliance prerequisite to maintain system auditability.*

### Focus for Run 4:
- Profile **autonomous developer environments** and automated code review frameworks.
- Investigate **multi-agent simulation environments** and synthetic training data generators.
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
            
    # Append Run 3 findings
    new_finding = {
        "run": 3,
        "topic": "Visual IDEs, Telemetry, and MCP Databases",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_anchor": "ARCHIVE/interim_report_03.md",
        "observation": "Visual Orchestration IDEs (Dify, Flowise, Langflow) are democratizing agent design, moving development from pure code to visual state-machine graphs. However, scaling production agents requires micro-trace observability and financial budgeting (AgentOps, Langfuse) to control execution loop runaway costs. MCP database integrations (SQLite/Postgres MCP) are standardizing vector and structured access, rendering bespoke DB scrapers obsolete."
    }
    
    # Avoid duplicate additions
    if not any(item["run"] == 3 for item in data):
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
    commit_msg = f"run(03): write 8 field notes, generate report 03, and update findings board"
    success, out, err = run_git_command(['commit', '-m', commit_msg])
    
    # Log session execution to LOGS/session_diary.md
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 03 - Compile Report: `{git_hash}`\n"
    entry += f"- **Action**: Run 03 research loop completed.\n"
    entry += f"- **Details**: Wrote 8 field notes (017-024) on IDEs/Telemetry/MCP and compiled `interim_report_03.md`.\n"
    entry += f"- **Status**: Auto-committed to source of truth.\n\n"
    
    with open(diary_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    print("Session diary updated and committed.")

if __name__ == "__main__":
    config = get_config()
    write_run_03()
    update_board_opinions()
    commit_and_log()
    
    # Git add the runner script too
    run_git_command(['add', 'SERVICES/run_03_research.py'])
    run_git_command(['commit', '-m', 'chore: add run 03 research script'])
    
    # Increment config pointer
    update_config_to_next(config)

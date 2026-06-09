import os
import datetime
import subprocess

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "WORKSPACE")
FIELD_NOTES_DIR = os.path.join(WORKSPACE_DIR, "field_notes")
ARCHIVE_DIR = os.path.join(BASE_DIR, "ARCHIVE")
INTERIM_DIR = os.path.join(ARCHIVE_DIR, "interim")
LOGS_DIR = os.path.join(BASE_DIR, "LOGS")

def ensure_dirs():
    os.makedirs(FIELD_NOTES_DIR, exist_ok=True)
    os.makedirs(INTERIM_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

def run_git_command(args):
    try:
        result = subprocess.run(['git'] + args, cwd=BASE_DIR, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

# Content data for 8 field notes
field_notes_data = [
    {
        "filename": "field_note_001_mcp-anthropic.md",
        "title": "Model Context Protocol (MCP) by Anthropic",
        "content": """# Profile
- **Name**: Model Context Protocol (MCP)
- **Category**: Open Standard / Tool Orchestration Protocol
- **Creator**: Anthropic (Released November 2024, standardized throughout 2025/2026)
- **Status**: Open-source specification & SDKs (Python, TypeScript)

# Agent-Native Characteristics
- **Universal Connectivity**: Solves the N×M integration bottleneck by introducing a "USB-C port for AI".
- **Client-Server Architecture**: Separates the MCP Client (e.g., Claude Desktop, IDEs like Cursor/VS Code) from the MCP Server (e.g., databases, GitHub, Slack, local terminals).
- **JSON-RPC Communication**: Allows agents to safely inspect available tools, query resources, and request prompts via a lightweight standardized protocol.

# Aesthetic/UX Details
- Exposes structured schemas that render automatically inside developer IDEs.
- Allows humans to monitor agent tool calls in real-time, providing click-to-approve interface gates for unsafe operations.

# Key Takeaways & Market Signal
- **Signal**: Walled gardens are giving way to unified APIs. Instead of building custom wrappers, startups are building MCP-compliant servers, ensuring instant compatibility with all major LLMs.
- **Reference**: https://modelcontextprotocol.io"""
    },
    {
        "filename": "field_note_002_skyfire.md",
        "title": "Skyfire: Financial Rails for AI Agents",
        "content": """# Profile
- **Name**: Skyfire
- **Category**: Agentic Fintech / Digital Economy Infrastructure
- **Founders**: Amir Sarhangi & Craig DeWitt (former Ripple executives)
- **Backing**: a16z Crypto, Coinbase Ventures, Circle, Ripple
- **Valuation / Funding**: $8.5M seed (Aug 2024, scaling in 2025/2026)

# Agent-Native Characteristics
- **KYA (Know Your Agent)**: Cryptographically signs credentials to prove the agent's identity and legitimacy, preventing standard anti-bot/WAF blocks.
- **Micro-Payments (KYAPay)**: Enables high-frequency, low-value transactions (e.g., $0.005 per token/API call) using stablecoins (USDC) and fiat rails.
- **Spending Guardrails**: Allows humans to set explicit daily/weekly budgets, rate limits, and allowed endpoints for each agent, mitigating risk of rogue spending.

# Aesthetic/UX Details
- Developers manage agents via a sleek dashboard that displays spend velocity, active wallets, and KYA status.
- Alerts trigger instantly if an agent approaches its pre-set financial cap.

# Key Takeaways & Market Signal
- **Signal**: Agents cannot achieve true operational independence if they are blocked by human-centric credit cards, CAPTCHAs, and billing address checks. Financial infrastructure must treat AI as a primary citizen.
- **Reference**: https://skyfire.xyz"""
    },
    {
        "filename": "field_note_003_cognition-devin.md",
        "title": "Devin by Cognition AI",
        "content": """# Profile
- **Name**: Devin
- **Category**: Autonomous Engineering Agent / Virtual Developer
- **Creator**: Cognition AI (Scott Wu, CEO)
- **Backing**: Founders Fund, Peter Thiel (Valued at $2B in 2024/2025)

# Agent-Native Characteristics
- **Agent Sandbox Environment**: Provides a dedicated, containerized virtual machine for the AI agent, complete with a terminal, code editor, and active browser.
- **Long-Horizon Planning**: Built to handle complex tasks (like upgrading a deprecated library across a large codebase) requiring hundreds of sequential steps.
- **Self-Correction Loop**: Continuously tests code, reads stack traces, and iterates on fixes without human prompt-chaining.

# Aesthetic/UX Details
- Features a side-by-side terminal, editor, and visual browser window where the human can see Devin's thoughts, plans, and active screens in real-time.
- Allows humans to pause the run, inject feedback directly into the terminal, and resume the task.

# Key Takeaways & Market Signal
- **Signal**: Software engineering is shifting from IDE autocomplete to delegation. The developer's role is evolving into an "Architect and Quality Assurer" directing autonomous agents.
- **Reference**: https://cognition.ai"""
    },
    {
        "filename": "field_note_004_langgraph.md",
        "title": "LangGraph by LangChain",
        "content": """# Profile
- **Name**: LangGraph
- **Category**: Multi-Agent State Orchestration Framework
- **Creator**: LangChain Inc. (Harrison Chase, CEO)
- **Status**: Open-source library with cloud hosting (LangGraph Cloud)

# Agent-Native Characteristics
- **Graph-Based Flow**: Models agent workflows as cyclic graphs (Nodes = agents/tools, Edges = decisions).
- **State Persistence**: Maintains conversational and execution history across multi-step runs, allowing agents to pause, sleep, and resume without losing context.
- **Human-in-the-Loop Gates**: Built-in support for interrupting execution to await human review (e.g. before sending an email or applying a database migration).

# Aesthetic/UX Details
- Integrates with LangSmith to provide interactive execution graphs, step-by-step latency logging, and run-trace visualizations.
- Simple, node-focused developer syntax.

# Key Takeaways & Market Signal
- **Signal**: Simple linear prompt chaining (LangChain v1) is insufficient for complex enterprise logic. Stateful multi-agent graphs with loops are now the standard design pattern.
- **Reference**: https://langchain.com/langgraph"""
    },
    {
        "filename": "field_note_005_sierra-ai.md",
        "title": "Sierra AI: Transactional Customer Agents",
        "content": """# Profile
- **Name**: Sierra
- **Category**: Enterprise AI Agent Platform
- **Founders**: Bret Taylor (OpenAI Chairman, former co-CEO Salesforce) & Clay Bavor (former Google VP)
- **Backing**: Sequoia Capital (Valued at $1.4B in late 2024)

# Agent-Native Characteristics
- **Transactional Capability**: Moves beyond answering FAQs to executing business tasks by integrating with enterprise APIs (SAP, Salesforce, Shopify).
- **Hallucination Mitigation**: Uses "active governance" models that constrain agent actions to predefined company guidelines and workflows.
- **Adaptive Conversational Logic**: Can manage context shifts (e.g. customer asking a billing question in the middle of processing a return).

# Aesthetic/UX Details
- Premium enterprise-focused dashboard showing resolution rates, cost-per-ticket, API health, and transcripts.
- Focuses heavily on high-fidelity brand voice alignment.

# Key Takeaways & Market Signal
- **Signal**: The chatbot market is dead; the transactional customer agent market has begun. The value is not in "answering questions" but in "resolving tickets" by writing to enterprise systems.
- **Reference**: https://sierra.ai"""
    },
    {
        "filename": "field_note_006_multion.md",
        "title": "MultiOn: Autonomous Web Browsing API",
        "content": """# Profile
- **Name**: MultiOn
- **Category**: Browser-Native Agent Platform / Web Automation API
- **Status**: VC backed (General Catalyst, Y Combinator)

# Agent-Native Characteristics
- **VLM-Driven Navigation**: Uses custom Vision-Language Models to interact with the visual browser DOM (clicking, typing, scrolling).
- **Agentic Browsing API**: Exposes an API endpoint (`/browse`) that allows external agents to delegate browser actions (e.g. "Buy a flight to Berlin", "Fill out this form").
- **CAPTCHA & Auth Handling**: Employs heuristic solving and session storage to bypass bot-detection systems on human-centric websites.

# Aesthetic/UX Details
- Shows a virtual browser window rendering live execution, so humans can watch the agent navigate pages and fill inputs.
- Highly programmatic developer API.

# Key Takeaways & Market Signal
- **Signal**: Until all websites expose agent-friendly API endpoints, browser-automation agents are the only way to integrate LLMs with legacy, web-based software.
- **Reference**: https://multion.ai"""
    },
    {
        "filename": "field_note_007_crewai.md",
        "title": "CrewAI: Role-Playing Orchestration Framework",
        "content": """# Profile
- **Name**: CrewAI
- **Category**: Multi-Agent Role-Playing Orchestration
- **Founder**: João Moura
- **Status**: Highly popular open-source framework with CrewAI Enterprise offerings

# Agent-Native Characteristics
- **Role & Persona Definition**: Allows developers to explicitly define an agent's "Role", "Goal", and "Backstory" to optimize system outputs.
- **Hierarchical & Consensus Delegation**: Supports complex organizational models where agents can automatically delegate tasks to sub-agents, request feedback, or build consensus.
- **Tool Integration**: Integrates directly with CrewTools (web search, file reading, scraping tools) for autonomous execution.

# Aesthetic/UX Details
- Clean, highly readable Python syntax.
- Verbose CLI outputs illustrating agent thoughts, thoughts-to-actions, and peer-to-peer conversations.

# Key Takeaways & Market Signal
- **Signal**: Dividing complex tasks among highly specialized, small agent personas yields superior results compared to using a single generalist LLM.
- **Reference**: https://crewai.com"""
    },
    {
        "filename": "field_note_008_decart-oasis.md",
        "title": "Decart: Generative World Models for Agent Testing",
        "content": """# Profile
- **Name**: Decart AI
- **Category**: World Models / Generative AI Simulation
- **Backing**: Sequoia Capital
- **Tech Highlight**: Created "Oasis" (first real-time generative video game model, October 2024)

# Agent-Native Characteristics
- **Interactive Generative Environments**: Simulates complex, interactive 3D/2D spaces in real-time, responding dynamically to user or agent actions.
- **Zero-Engine Physics**: Generates physics, lighting, and environments entirely through video frame generation in a neural network, bypassing traditional game engines (Unity/Unreal).
- **Agent Sandbox/Simulators**: Provides an ideal, safe training ground for vision-based agents (e.g. robotics, web navigation droids) to fail and learn.

# Aesthetic/UX Details
- Displays interactive, playable video environments rendered at 20+ FPS.
- Low-latency visual feed.

# Key Takeaways & Market Signal
- **Signal**: Building simulation environments for training AI agents is moving from hand-coded rules to generative world models. Agents can learn to navigate real-world physics inside a neural net.
- **Reference**: https://decart.ai"""
    }
]

def write_field_notes():
    ensure_dirs()
    print("Writing 8 field notes...")
    for idx, fn in enumerate(field_notes_data):
        now = datetime.datetime.now()
        filepath = os.path.join(FIELD_NOTES_DIR, fn["filename"])
        content = f"# {fn['title']}\n"
        content += f"> Ingested on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"> Category: field_notes\n"
        content += f"> Index: {idx + 1:03d}\n\n"
        content += fn["content"].strip()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"  Created: {fn['filename']}")

def write_interim_report():
    ensure_dirs()
    filepath = os.path.join(INTERIM_DIR, "interim_report_01.md")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_content = f"""# Interim Insight Report 01: The Emergence of the Agentic Stack

> **Date**: {now}
> **Cycle**: Run 1 (Field Notes 001 - 008)
> **Goal**: Map the foundational building blocks of Agent-Native architecture.

---

## 🔍 Executive Summary

Our initial scan of the 2026 agentic landscape reveals a major architectural transition. We are moving away from **"agent wrappers"** (which merely feed prompt templates into an API) and towards a structured, standard-compliant **Agentic Stack**. 

The core drivers of this shift are standardized tool-connectivity, economic and identity autonomy, sandbox operating environments, and role-based multi-agent graphs.

---

## 🗺️ The Agentic Stack Taxonomy

Based on the 8 profiles analyzed, we define the core tiers of agent-native infrastructure:

| Tier | Primary Purpose | Key Representative(s) | Market Signal |
| :--- | :--- | :--- | :--- |
| **Connectivity Protocol** | How agents talk to databases, tools, and IDEs. | **Model Context Protocol (MCP)** | Walled API gardens are collapsing into open standards. |
| **Identity & Payment Rails** | How agents transact and prove legitimacy. | **Skyfire** | Agents need crypto-wallets, KYA protocols, and micro-payment capability to act autonomously. |
| **Sandbox Environment** | Where agents execute code and navigate. | **Devin**, **MultiOn** | Agents need dedicated execution environments (virtual machines and VLMs) to operate. |
| **Orchestration & State** | How agents reason, plan, and delegate. | **LangGraph**, **CrewAI** | Multi-agent coordination requires explicit graph state machines and role delegation. |
| **Simulation & Testing** | Virtual training grounds for agent behavior. | **Decart (Oasis)** | World models are replacing manual game engines for training visual/physical agents. |

---

## 📈 Major Strategic Trends in 2026

### 1. The "USB-C" Standard for Tool Use
Anthropic's **MCP** is rapidly becoming the consensus standard for connecting LLMs to local/remote environments. By separating the client from the server, any developer can expose tools to *any* compliant agent with zero friction. The N×M integration problem is solved.

### 2. Autonomous Financial Sovereignty
Fintech is transforming to support AI-to-AI transactions. **Skyfire** is proving that agents must hold digital wallets and cryptographically sign their identities to bypass CAPTCHAs and fraud detection. Micropayments for single API calls or tokens are the native currency of the agentic economy.

### 3. Containerization as a First-Class Citizen
As demonstrated by **Devin**, agents can no longer operate in a vacuum. A robust agent requires an isolated operating system with an editor, browser, and bash shell to compile code, debug errors, and verify its own output in a loop.

### 4. Specialized Multi-Agent Systems
The industry is moving away from monolithic generalist agents. Frameworks like **CrewAI** and **LangGraph** show that dividing labor among specialized personas (e.g., an Editor Agent, a Scraper Agent, a Validator Agent) with a shared state machine yields vastly superior results.

---

## 🔮 Hypothesis & Next Run Plan

### Current Hypotheses:
1. *Startups that expose an MCP-compliant server for their data/service will experience a 10x adoption velocity among agent developers compared to traditional REST APIs.*
2. *As agents scale, computing resource costs and financial spend will spiral unless unified budgeting/guardrails (like Skyfire wallets) are embedded directly into orchestration frameworks.*

### Focus for Run 2:
- Identify and profile startups building **agent-native database engines** (designed for vectorized vector search and structured memory retrieval).
- Investigate **agentic security / guardrail platforms** that monitor agent reasoning paths for malicious prompt injection.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content.strip())
        
    print(f"Created Interim Report: interim_report_01.md")

def commit_changes():
    print("Staging and committing files to Git...")
    # Add files
    run_git_command(['add', 'WORKSPACE/field_notes/'])
    run_git_command(['add', 'ARCHIVE/interim/interim_report_01.md'])
    
    # Commit
    success, out, err = run_git_command(['commit', '-m', 'run(01): write 8 field notes and generate interim report 01'])
    if success:
        print("Git Commit Successful.")
        print(out)
    else:
        print("Git Commit Failed:")
        print(err)

def log_session_run():
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 01 - Compile Report: `{git_hash}`\n"
    entry += f"- **Action**: Run 01 research loop completed.\n"
    entry += f"- **Details**: Wrote 8 field notes (001-008) and compiled `interim_report_01.md`.\n"
    entry += f"- **Status**: Auto-committed to source of truth.\n\n"
    
    file_exists = os.path.exists(diary_path)
    with open(diary_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# Workspace Session Diary\n\n")
        f.write(entry)
    print("Session diary updated.")

if __name__ == "__main__":
    ensure_dirs()
    write_field_notes()
    write_interim_report()
    commit_changes()
    log_session_run()

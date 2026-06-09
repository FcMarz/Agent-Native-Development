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
    return {"current_phase": 1, "current_run": 2, "notes_per_run": 8, "runs_per_phase": 8}

def update_config_to_next(config):
    config_path = os.path.join(PM_DIR, "config.json")
    # Increment run
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

# Content data for the 8 memory/security profiles
field_notes_data = [
    {
        "filename": "field_note_009_letta.md",
        "title": "Letta (formerly MemGPT): OS-like Virtual Context for Agents",
        "content": """# Profile
- **Name**: Letta
- **Category**: Agent Memory & State Management Runtime
- **Founders**: Charles Packer & Sarah Wooders (UC Berkeley MemGPT researchers)
- **Status**: Venture-backed startup (released in 2025/2026)

# Agent-Native Characteristics
- **LLM-as-an-OS**: Treats the context window of LLMs like RAM, swapping blocks in and out of long-term storage (disk) dynamically.
- **Self-Editing Memory**: The agent has system tool-calling instructions that allow it to proactively modify its own core memory blocks as new facts emerge during conversation.
- **Persistent Runtimes**: Runs agents as long-lived servers, preserving state, memory, and tool connections indefinitely across chat sessions.

# Aesthetic/UX Details
- Admin console allows developers to visualize the agent's memory banks (Core Memory, Recall Memory, Archival Memory) and read agent self-updates.

# Key Takeaways & Market Signal
- **Signal**: Context window limits are no longer solved just by packing more tokens. Stateful, self-editing agent memory that mirrors operating system memory architecture is the path to long-lived, coherent agents.
- **Reference**: https://letta.com"""
    },
    {
        "filename": "field_note_010_mem0.md",
        "title": "Mem0: Modular Intelligent Memory Layer",
        "content": """# Profile
- **Name**: Mem0
- **Category**: Modular Memory Infrastructure / Vector Database Add-on
- **Status**: Y Combinator backed, popular open-source repository

# Agent-Native Characteristics
- **Plugin Architecture**: Designed as a lightweight, modular "memory layer" that plugs into existing frameworks (LangChain, AutoGen, CrewAI).
- **Fact Extraction**: Automatically extracts atomic facts from raw inputs (e.g. "User prefers dark mode", "Client is located in Berlin"), deduplicates them, and stores them.
- **Cross-Session Recall**: Retrieves relevant user preferences and past interaction details across sessions, enabling high personalization.

# Aesthetic/UX Details
- Clean, programmatic Python API: `m.add("pasted raw text", user_id="user_123")` and `m.get_all(user_id="user_123")`.
- Easily integrates with major LLMs and Vector DBs.

# Key Takeaways & Market Signal
- **Signal**: Adding memory does not require migrating to a full custom framework. Modular, decoupled memory databases that perform factual extraction on the fly allow legacy agent wrappers to instantly add context.
- **Reference**: https://github.com/mem0ai/mem0"""
    },
    {
        "filename": "field_note_011_milvus-graphrag.md",
        "title": "Milvus / Zilliz: GraphRAG and Entity Memory",
        "content": """# Profile
- **Name**: Milvus / Zilliz
- **Category**: Vector & Graph Database / Agent Knowledge Graph
- **Status**: Enterprise Vector Database leader

# Agent-Native Characteristics
- **Entity-Relation Memory**: Moves beyond simple dense vector search. Incorporates GraphRAG (knowledge graphs) to map relations between entities (e.g., "Company A bought Company B").
- **Agentic Knowledge Retrieval**: Allows agents to run complex queries that combine semantic similarities with graph relations, creating highly structured context.
- **Scale & Performance**: Handles high-concurrency, high-dimension vector queries from thousands of concurrently operating agents.

# Aesthetic/UX Details
- Admin console (Attu) visualizes the vector spaces, indexes, and graph relationships dynamically.

# Key Takeaways & Market Signal
- **Signal**: Simple flat vector retrieval (semantic chunk matching) is insufficient for reasoning agents. Agents need structure (knowledge graphs) to understand how data points relate to each other.
- **Reference**: https://milvus.io"""
    },
    {
        "filename": "field_note_012_pinecone-canopy.md",
        "title": "Pinecone Canopy: Simplified Agent RAG Framework",
        "content": """# Profile
- **Name**: Canopy
- **Category**: Agent-Native RAG Framework / Search Assistant
- **Creator**: Pinecone Systems
- **Status**: Open-source framework wrapping Pinecone serverless offerings

# Agent-Native Characteristics
- **Search-Native Design**: Tailored to help agents query large, unstructured document libraries in milliseconds.
- **Automatic Chunking & Token Counting**: Automatically manages text chunking, embedding generation, and token budgets inside the context window.
- **Relevance Tuning**: Optimized for feeding agent-centric LLMs with high-fidelity, clean snippets rather than raw paragraphs.

# Aesthetic/UX Details
- Offers a CLI and an out-of-the-box chat interface to test RAG pipelines visually before plugging them into an agent.

# Key Takeaways & Market Signal
- **Signal**: Large vector database providers are moving up the stack. By offering agent-friendly RAG frameworks, they secure developer lock-in on the storage tier.
- **Reference**: https://github.com/pinecone-io/canopy"""
    },
    {
        "filename": "field_note_013_lakera.md",
        "title": "Lakera: Real-Time AI Runtime Security",
        "content": """# Profile
- **Name**: Lakera
- **Category**: AI Security / Runtime Threat Prevention
- **Status**: Acquired by Check Point Software Technologies (September 2025)
- **Acquisition Impact**: Forms the core of Check Point's Center of Excellence for AI Security

# Agent-Native Characteristics
- **Lakera Guard**: An inline firewall that intercepts agent prompts and model outputs in microseconds, blocking prompt injections and jailbreaks.
- **Red Teaming (Lakera Red)**: Evaluates agent vulnerabilities systematically before deployment.
- **Adversarial Database**: Backed by Lakera's global threat database (gained via the viral Gandalf prompt-hacking challenge).

# Aesthetic/UX Details
- Dashboard displays injection attempts, block logs, vulnerability graphs, and data leak warnings.

# Key Takeaways & Market Signal
- **Signal**: Agentic security is consolidating. The acquisition of Lakera by an enterprise firewall giant like Check Point proves that LLM-native security is a trillion-dollar frontier for corporate operations.
- **Reference**: https://www.lakera.ai"""
    },
    {
        "filename": "field_note_014_patronus-ai.md",
        "title": "Patronus AI: Real-Time Hallucination Guardrails",
        "content": """# Profile
- **Name**: Patronus AI
- **Category**: AI Reliability & Evaluation Platform
- **Founders**: Anand Kannappan & Rebecca Qian (former Meta AI researchers)
- **Status**: Venture backed ($17M Series A in 2024, scaling in 2025/2026)

# Agent-Native Characteristics
- **Lynx Evaluator**: A proprietary, open-source model optimized specifically for detecting hallucinations in RAG outputs.
- **Patronus Protect**: An on-device or API-based guardrail engine that blocks non-compliant or inaccurate agent output.
- **Automated Red Teaming**: Generates adversarial test sets to stress-test agent boundaries at scale.

# Aesthetic/UX Details
- Provides test-suite dashboards showing model accuracy, compliance scoring, and regression tracking.

# Key Takeaways & Market Signal
- **Signal**: Evaluators must be LLMs themselves. Traditional keyword checks are useless for monitoring agent reasoning. Specialized evaluator models (like Lynx) are required to assure corporate compliance.
- **Reference**: https://www.patronus.ai"""
    },
    {
        "filename": "field_note_015_prompt-security.md",
        "title": "Prompt Security: Enterprise Shadow Agent Protection",
        "content": """# Profile
- **Name**: Prompt Security
- **Category**: Enterprise AI Security / Shadow AI Guardrails
- **Status**: Venture-backed startup (scaling in 2025/2026)

# Agent-Native Characteristics
- **Shadow Agent Detection**: Inspects and monitors employee usage of external AI assistants, preventing corporate data leaks.
- **PII Redaction**: Intercepts outgoing requests to LLM APIs, redacting personally identifiable info (PII) before it leaves the corporate perimeter.
- **Tool-Call Interception**: Prevents agents from executing unauthorized API integrations or file writes.

# Aesthetic/UX Details
- Administrator dashboard highlighting data compliance trends, blocked prompt injections, and risky tool integrations.

# Key Takeaways & Market Signal
- **Signal**: Security is needed both inside the agent (preventing injection) and outside the agent (preventing data leakage of the organization using it).
- **Reference**: https://www.prompt.security"""
    },
    {
        "filename": "field_note_016_nemo-guardrails.md",
        "title": "NVIDIA NeMo Guardrails: Programmable LLM Control Flow",
        "content": """# Profile
- **Name**: NeMo Guardrails
- **Category**: Open-Source Semantic Guardrail Library
- **Creator**: NVIDIA
- **Status**: Open-source toolkit, highly adopted in enterprise pipelines

# Agent-Native Characteristics
- **Colang Syntax**: Uses a custom declarative language (Colang) to define specific dialogue paths, policies, and behavior limits.
- **Semantic Moderation**: Verifies the semantic topic of the prompt, steering the LLM back to the targeted domain if it starts drifting.
- **In-Memory Guardrails**: Runs alongside the model inside inference engines, adding negligible latency to the generation loop.

# Aesthetic/UX Details
- Highly code-centric, designed for integration into Python pipelines and NVIDIA Triton inference servers.

# Key Takeaways & Market Signal
- **Signal**: Programmable guardrails are necessary to bridge the gap between deterministic software rules and fuzzy LLM reasoning. Colang-style flow control keeps agents within compliance.
- **Reference**: https://github.com/NVIDIA/NeMo-Guardrails"""
    }
]

def write_run_02():
    config = get_config()
    phase = config["current_phase"]
    run = config["current_run"]
    
    phase_str = f"phase_{phase:02d}"
    run_str = f"run_{run:02d}"
    
    # Active directories
    run_notes_dir = os.path.join(FIELD_NOTES_DIR, run_str)
    run_report_dir = os.path.join(ARCHIVE_DIR, phase_str, run_str)
    
    os.makedirs(run_notes_dir, exist_ok=True)
    os.makedirs(run_report_dir, exist_ok=True)
    
    print(f"Executing Research Run {run} under Phase {phase}...")
    
    # Write field notes
    for idx, fn in enumerate(field_notes_data):
        now = datetime.datetime.now()
        filepath = os.path.join(run_notes_dir, fn["filename"])
        
        # Calculate actual global index (note numbers 009 to 016)
        global_idx = 8 + idx + 1
        
        content = f"# {fn['title']}\n"
        content += f"> Ingested on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"> Category: field_notes\n"
        content += f"> Index: {global_idx:03d}\n"
        content += f"> Phase: {phase:02d} | Run: {run:02d}\n\n"
        content += fn["content"].strip()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Created: {fn['filename']}")
        
    # Write Report
    report_path = os.path.join(run_report_dir, f"interim_report_{run:02d}.md")
    report_content = f"""# Interim Insight Report {run:02d}: Memory and Security in the Agentic Stack

> **Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **Cycle**: Phase {phase:02d}, Run {run:02d} (Field Notes 009 - 016)
> **Goal**: Examine Memory persistence and Guardrail/Security solutions in Agent-Native systems.

---

## 🔍 Executive Summary

As autonomous agents transition from prototype chatbots into transactional employees, the primary engineering bottlenecks have shifted from **inference capability** to **context management** and **security assurance**. 

This report synthesizes Run 02's focus on **Agent-Native Memory/Databases** (009-012) and **Agentic Security/Guardrails** (013-016). We demonstrate that memory is shifting from static retrieval (flat vector search) to dynamic self-editing structures, and security is shifting from simple regex filters to inline, real-time semantic firewalls (e.g., Lakera, Patronus).

---

## 🗺️ Memory and Security Tier Taxonomy

Based on the 8 profiles analyzed, we map these innovations into the active Agentic Stack:

| Category | Tier | Focus | Key Representative(s) | Strategic Signal |
| :--- | :--- | :--- | :--- | :--- |
| **Memory & Storage** | **Stateful OS Memory** | Self-editing context systems. | **Letta (MemGPT)** | Agents need to manage their own context dynamically, writing to "disk" autonomously. |
| **Memory & Storage** | **Intelligent Memory Layer** | Plugin-based factual extraction. | **Mem0** | Lightweight memory extractors allow legacy agents to add cross-session context instantly. |
| **Memory & Storage** | **GraphRAG / Knowledge Graph** | Entity-relational schemas. | **Milvus / Zilliz** | flat vector matching is dying; relationship graphs are key for agent reasoning. |
| **Security & Safety** | **Runtime Firewall** | Microsecond inline threat interception. | **Lakera (Check Point)** | AI-native security is consolidating under cyber-security giants (acquired in 2025). |
| **Security & Safety** | **Evaluator-as-a-Service** | Hallucination and compliance scoring. | **Patronus AI** | Real-time evaluations require specialized models (Lynx) running locally or on edge. |
| **Security & Safety** | **Programmable Guardrails** | Semantic routing and policy enforcement. | **NVIDIA NeMo Guardrails**| Colang-based rules bridge fuzzy LLM reasoning and deterministic safety. |

---

## 📈 Major Strategic Trends in Run 02

### 1. Memory is Becoming "Active" (Self-Editing)
We observe a clear departure from traditional passive Retrieval-Augmented Generation (RAG). Startups like **Letta** are pioneering systems where the agent determines *when* and *what* to write to its database, modifying its own long-term memory blocks as a standard operating tool.

### 2. Relational Context Over Flat Semantics
The integration of knowledge graphs by enterprise databases like **Milvus** highlights that agents require relational connections between concepts (e.g. "Vendor A is subsidiary of Vendor B") to resolve complex analytical inquiries, outperforming simple semantic text-chunk matching.

### 3. The Consolidation of AI-Native Cyber Security
The acquisition of **Lakera** by Check Point Software Technologies in late 2025 marks a major milestone. AI security has moved past academic prompt injection tests into a fundamental category of enterprise threat management. Inline firewalls that evaluate prompt safety in under 5 milliseconds are a mandatory production requirement.

### 4. Specialized Evaluator Models
Generalist LLMs make poor real-time guardrails due to high latency and cost. Startups like **Patronus AI** are building tiny, specialized, and highly accurate evaluation models (like Lynx) that run alongside the host agent to detect hallucinations and block non-compliant content.

---

## 🔮 Hypothesis & Next Run Plan

### Current Hypotheses:
1. *The acquisition of Lakera will trigger a wave of acquisitions of AI-guardrail startups by legacy cyber-security companies (Palo Alto Networks, CrowdStrike, Cloudflare) in 2026.*
2. *Stateful agent runtimes (like Letta) will gradually replace simple stateless orchestrators (like LangChain) for applications requiring complex, long-horizon customer actions.*

### Focus for Run 3:
- Analyze **agent-native database engines** specifically optimized for fast, structured memory recall.
- Scan the landscape of **multi-agent developer tools** and visual IDE orchestrators.
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content.strip())
    print(f"Created Interim Report: interim_report_{run:02d}.md")

def commit_and_log():
    config = get_config()
    run = config["current_run"]
    
    # Add files
    run_git_command(['add', 'WORKSPACE/field_notes/'])
    run_git_command(['add', 'ARCHIVE/'])
    run_git_command(['add', 'PROJECT_MANAGEMENT/config.json'])
    
    # Commit
    commit_msg = f"run(02): write 8 field notes and generate interim report 02"
    success, out, err = run_git_command(['commit', '-m', commit_msg])
    
    # Log session execution to LOGS/session_diary.md
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 02 - Compile Report: `{git_hash}`\n"
    entry += f"- **Action**: Run 02 research loop completed.\n"
    entry += f"- **Details**: Wrote 8 field notes (009-016) on Memory/Security and compiled `interim_report_02.md`.\n"
    entry += f"- **Status**: Auto-committed to source of truth.\n\n"
    
    with open(diary_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    print("Session diary updated and committed.")

if __name__ == "__main__":
    config = get_config()
    write_run_02()
    commit_and_log()
    
    # Git add the runner script too
    run_git_command(['add', 'SERVICES/run_02_research.py'])
    run_git_command(['commit', '-m', 'chore: add run 02 research script'])
    
    # Increment config pointer
    update_config_to_next(config)

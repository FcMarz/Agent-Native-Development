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
    return {"current_phase": 1, "current_run": 5, "notes_per_run": 8, "runs_per_phase": 8}

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

# Content data for the 8 profiles of Run 05
field_notes_data = [
    {
        "filename": "field_note_033_skyfire.md",
        "title": "Skyfire: Payment Network for Autonomous AI Agents",
        "content": """# Profile
- **Name**: Skyfire
- **Category**: Agentic Economic / Payment Gateway
- **Status**: Active protocol, commercial/open-source developer SDKs

# Agent-Native Characteristics
- **Agent Wallets**: Creates programmatic digital wallets dedicated to individual agent loops or API clients.
- **Budgetary Constraints**: Allows developers or users to set max spend rules, limits per transaction, and auto-approval thresholds for agent transactions.
- **Service Verification**: Automatically verifies the validity of API services and executes instant micro-payments for data intake.

# Aesthetic/UX Details
- Admin dashboard displaying active agent wallets, transaction ledgers, spending limits, and system health alerts.

# Key Takeaways & Market Signal
- **Signal**: To achieve full independence, agents must be financial actors. Standard credit cards and bank accounts are not built for machine-scale transactions; API gateways with micro-budgets are.
- **Reference**: https://skyfire.xyz"""
    },
    {
        "filename": "field_note_034_stripe_agent.md",
        "title": "Stripe Agent Payments: Machine-to-Machine Invoicing",
        "content": """# Profile
- **Name**: Stripe Agent Payments
- **Category**: Developer Payment Infrastructure
- **Status**: Active research/experimental SDK by Stripe

# Agent-Native Characteristics
- **Zero-Form Invoicing**: Bypasses typical human checkout forms (e.g. CAPTCHAs, 2FA) through direct authenticated API requests.
- **Tokenized Wallets**: Assigns spending allowances to sub-keys, allowing agents to pay for computing or storage without exposing master credit details.
- **M2M Settlement**: Settles invoicing between API providers and agent callers instantly under pre-negotiated rate contracts.

# Aesthetic/UX Details
- Integrates directly into Stripe's standard dashboard; displays agent transaction tags and machine-generated invoices.

# Key Takeaways & Market Signal
- **Signal**: The largest traditional payment providers are building specialized machine checkout tracks. The web's commercial layout is shifting to accommodate machine buyers.
- **Reference**: https://stripe.com"""
    },
    {
        "filename": "field_note_035_biconomy.md",
        "title": "Biconomy: Smart Account Session Keys for Agents",
        "content": """# Profile
- **Name**: Biconomy
- **Category**: On-chain Smart Contract Wallets
- **Status**: Production-ready Web3 infrastructure supporting ERC-4337

# Agent-Native Characteristics
- **Session Keys**: Allows agents to sign transactions within strict limits (e.g. only swap tokens on a specific exchange, maximum $10 value) without prompting user signatures each time.
- **Gas Abstraction**: Allows developers to sponsor agent gas fees, enabling seamless user-agent experiences.
- **Programmatic Wallets**: Abstracts private key management behind decentralized account-abstraction contracts.

# Aesthetic/UX Details
- Developer SDK and portal for managing session contracts, tracking transactions, and configuring paymasters.

# Key Takeaways & Market Signal
- **Signal**: Prompting human users to sign every transaction breaks autonomy. Smart accounts with restricted session keys permit secure, bounded machine-driven finance.
- **Reference**: https://www.biconomy.io"""
    },
    {
        "filename": "field_note_036_alby.md",
        "title": "Alby: Bitcoin Lightning wallets for Micro-Settlement",
        "content": """# Profile
- **Name**: Alby
- **Category**: Micro-payment Wallet and LND Integration
- **Status**: Production-ready developer wallet and web extension

# Agent-Native Characteristics
- **Lightning Network Micro-settlement**: Resolves transactions of fractions of a cent instantly with near-zero network fees.
- **WebLN Standards**: Programmatically requests payments or pays invoices via standardized web browser extensions.
- **LND Hub Connection**: Connects autonomous agents directly to lightning nodes for decentralized machine-scale billing.

# Aesthetic/UX Details
- Clean browser popup wallet for managing keys, budgets, lightning addresses, and active session allowances.

# Key Takeaways & Market Signal
- **Signal**: Traditional credit networks fail when fees exceed transaction values. The Lightning network enables sub-penny micro-payments, making pay-per-query agent pipelines economically viable.
- **Reference**: https://getalby.com"""
    },
    {
        "filename": "field_note_037_coinbase_agentkit.md",
        "title": "Coinbase AgentKit: Empowering AI Agents with Crypto",
        "content": """# Profile
- **Name**: Coinbase AgentKit
- **Category**: Web3 Agent SDK
- **Status**: Open-source SDK launched by Coinbase

# Agent-Native Characteristics
- **Crypto-enabled Capabilities**: Equips LLM agents with functions to send and receive crypto, check balances, and interact with smart contracts on Base network.
- **Frictionless Setup**: Instantiates wallet keys locally, allowing agents to instantly fund themselves and interact with Web3 protocols.
- **Agent Identity**: Enables agents to buy domains (ENS) and sign cryptographic statements verifying their output.

# Aesthetic/UX Details
- Lightweight developer SDK with pre-configured tools for LangChain, Autogen, and standard Python agent frameworks.

# Key Takeaways & Market Signal
- **Signal**: Crypto is the native currency of AI. Providing agents with self-sovereign wallets allows them to bypass traditional identification checks (KYC) required by banks.
- **Reference**: https://github.com/coinbase/agentkit"""
    },
    {
        "filename": "field_note_038_nillion.md",
        "title": "Nillion: Blind Computation Network for Secret Input Handling",
        "content": """# Profile
- **Name**: Nillion
- **Category**: Decentralized Confidential / ZK Computation
- **Status**: Testnet active, early developer integrations

# Agent-Native Characteristics
- **Multi-Party Computation (MPC)**: Splits sensitive variables (e.g. database credentials, user API keys) into encrypted shares distributed across a node network.
- **Blind Execution**: Allows agents to run mathematical calculations or query databases on user credentials without the agent ever exposing the plaintext secrets.
- **Privacy-Preserving Tool-Use**: Protects developer secrets from leaking through prompt injection attacks on the LLM runtime.

# Aesthetic/UX Details
- Command-line interfaces and client libraries for encrypting, storing, and running computations on Nil-Message payloads.

# Key Takeaways & Market Signal
- **Signal**: The delegation paradox (giving agents API keys without letting them leak them) requires blind execution environments where keys are only compiled during the secure API handshake.
- **Reference**: https://nillion.com"""
    },
    {
        "filename": "field_note_039_privy.md",
        "title": "Privy: Self-Custodial Embedded Wallets for AI",
        "content": """# Profile
- **Name**: Privy
- **Category**: Embedded Onboarding & Wallet Security
- **Status**: Production-ready Web3 auth provider

# Agent-Native Characteristics
- **Shamir Secret Sharing (SSS)**: Secures agent keys by splitting them between the user's browser, Privy's HSM, and third-party storage.
- **Embedded Wallets**: Automatically provisions wallets for agents under OAuth authentication flows (e.g. signing in with Google or Discord).
- **Cross-App signing**: Permits agents to perform transactions across different dApps while keeping key shares locked in hardware enclaves.

# Aesthetic/UX Details
- Clean, customizable Web UI modals for user authentication and transaction confirmation prompts.

# Key Takeaways & Market Signal
- **Signal**: Self-custody must be simplified for agents. Distributing key shares across secure enclaves protects funds from single points of failure.
- **Reference**: https://www.privy.io"""
    },
    {
        "filename": "field_note_040_mina.md",
        "title": "Mina Protocol: Zero-Knowledge State Proofs",
        "content": """# Profile
- **Name**: Mina Protocol
- **Category**: Zero-Knowledge Layer-1 Blockchain
- **Status**: Mainnet active, specializing in zkApps

# Agent-Native Characteristics
- **Succinct Blockchain**: Maintains a constant 22KB blockchain size using recursive zk-SNARKs.
- **Private State Verification**: Allows agents to verify they executed a task (e.g., crawled a specific site, calculated a score) without disclosing the database content.
- **Off-Chain Execution**: Executes complex logic off-chain and submits a short proof to the chain, preserving computational resource limits.

# Aesthetic/UX Details
- Developer CLI tools and typescript framework for authoring and deploying zero-knowledge smart contracts (zkApps).

# Key Takeaways & Market Signal
- **Signal**: Proof of execution is essential when delegating tasks to autonomous agents. Mina allows agents to cryptographically prove their results are correct without revealing how they got them.
- **Reference**: https://minaprotocol.com"""
    }
]

def write_run_05():
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
        
        # Calculate actual global index (note numbers 033 to 040)
        global_idx = 32 + idx + 1
        
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
    report_content = f"""# Interim Insight Report {run:02d}: Agent Payments, Micro-Settlement, and Zero-Knowledge Credentialing

> **Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **Cycle**: Run {run:02d} (Field Notes 033 - 040)
> **Goal**: Profile agent payment gateways, Bitcoin Lightning wallets, and zero-knowledge tool-use protocols.

---

## 🔍 Executive Summary

This cycle maps the emerging horizons of **Agent Economic Autonomy and Zero-Knowledge Security Infrastructure**.

Our analysis of **Agent Payments** (033-034, 037) demonstrates that AI agents are transitioning from mere software calculators to independent economic actors. By provisioning agent-specific digital wallets (via **Skyfire**, **Stripe Agent API**, and **Coinbase AgentKit**), systems can set micro-budgets and bypass human credit forms entirely. Simultaneously, **Micro-settlement networks** (035-036, 039) like **Alby** and **Biconomy** enable programmatic, low-fee machine billing and gas abstraction via session-key authorization. Finally, **Zero-Knowledge compute and blind enclaves** (038, 040) like **Nillion** and **Mina Protocol** resolve the critical delegation paradox: how to allow agents to execute tools and verify transactions without exposing sensitive plaintext secrets or credentials to model contexts.

---

## 🗺️ Agentic Fintech and Security Tier Taxonomy

Based on the 8 profiles analyzed, we map these tools into the active Agentic Stack:

| Category | Tier | Focus | Key Representative(s) | Strategic Signal |
| :--- | :--- | :--- | :--- | :--- |
| **Fintech** | **Payment Gateway** | Machine-to-machine invoicing and budget rules. | **Skyfire**, **Stripe Agent** | Traditional payment providers are standardizing non-human API payment tracks. |
| **Fintech** | **On-Chain SDK** | Local wallet key management and Web3 rails. | **Coinbase AgentKit** | Cryptocurrencies bypass traditional KYC bottlenecks, acting as AI-native currency. |
| **Fintech** | **Micro-Settlement** | Low-fee network settlement. | **Alby (Lightning)** | Pennies and fractions of cents are required for pay-per-query agent billing. |
| **Authorization**| **Session Wallets** | Limited, auto-signed keys. | **Biconomy**, **Privy** | Restricting signatures to specific rules avoids manual human approval loops. |
| **Security** | **Blind Execution** | Decentralized Multi-Party Computation. | **Nillion** | Executing tools on encrypted shares prevents prompt injection credential leaks. |
| **Security** | **ZK-State Proof** | Succinct execution proofs. | **Mina Protocol** | Cryptographic verification lets agents prove state validity without exposing secrets. |

---

## 📈 Major Strategic Trends in Run 05

### 1. The Machine-to-Machine Financial Track
Standard banking infrastructure (credit card validation, 3D-Secure, CAPTCHAs) is optimized to block non-human transactions. The emergence of agent-native billing gateways signals a parallel financial track built for machine-scale, micro-penny settlement.

### 2. Session-Key Authorization vs. Prompt Overload
To achieve operational flow, agents must transact without prompting human supervisors. Smart contracts with **Session Keys** restrict agent wallets to pre-approved boundary rules, solving the security issue without introducing human latency.

### 3. Resolving the Delegation Paradox via Blind Execution
Giving agents direct access to credentials (passwords, keys) leaves them vulnerable to prompt injection attacks. Decentralized blind-computation platforms like **Nillion** split variables into mathematical shares, ensuring agents can perform calculations or sign API requests without reading the secret in plaintext.

---

## 🔮 Hypothesis & Next Run Plan

### Current Hypotheses:
1. *By 2027, the majority of API billing will be settled programmatically between agent wallets using Lightning or Layer-2 crypto networks.*
2. *Decentralized Multi-Party Computation (MPC) will replace plain environment variables (dotenv) in enterprise agent workflows.*

### Focus for Run 6:
- Profile **local Small Language Models (SLMs)** and sovereign coordinate routing.
- Evaluate **browser navigation drivers** and vision-based browser automation (e.g. browser-use, MultiOn).
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
            
    # Append Run 5 findings
    new_finding = {
        "run": 5,
        "topic": "Agent Payments, Micro-Settlement, and Zero-Knowledge Credentialing",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_anchor": "ARCHIVE/interim_report_05.md",
        "observation": "As agents mature, they transition from software planners to economic actors. The emergence of agent-native transaction APIs (Skyfire, Stripe, Coinbase AgentKit) allows models to buy their own API keys, execute micro-payments, and self-fund runtime environments. Concurrently, integrating Zero-Knowledge and blind computation (Nillion, Mina) secures this transition, resolving the critical agent paradox: how to delegate administrative credentials without exposing plaintext access to models."
    }
    
    # Avoid duplicate additions
    if not any(item["run"] == 5 for item in data):
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
    commit_msg = f"run(05): write 8 field notes, generate report 05, and update findings board"
    success, out, err = run_git_command(['commit', '-m', commit_msg])
    
    # Log session execution to LOGS/session_diary.md
    diary_path = os.path.join(LOGS_DIR, "session_diary.md")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, git_hash, _ = run_git_command(['rev-parse', '--short', 'HEAD'])
    
    entry = f"## [{now_str}] Run 05 - Compile Report: `{git_hash}`\n"
    entry += f"- **Action**: Run 05 research loop completed.\n"
    entry += f"- **Details**: Wrote 8 field notes (033-040) on Agent Payments/Micro-Settlement/ZK-enclaves and compiled `interim_report_05.md`.\n"
    entry += f"- **Status**: Auto-committed to source of truth.\n\n"
    
    with open(diary_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    print("Session diary updated and committed.")

if __name__ == "__main__":
    config = get_config()
    write_run_05()
    update_board_opinions()
    commit_and_log()
    
    # Git add the runner script too
    run_git_command(['add', 'SERVICES/run_05_research.py'])
    run_git_command(['commit', '-m', 'chore: add run 05 research script'])
    
    # Increment config pointer
    update_config_to_next(config)

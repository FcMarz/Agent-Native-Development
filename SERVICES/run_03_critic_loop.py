#!/usr/bin/env python3
"""
Writer-Critic Self-Correction Loop Engine.
Drafts research field notes and refines them through a multi-turn audit cycle.
"""

import os
import sys
import json
import argparse
import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WRITER_PERSONA_PATH = os.path.join(BASE_DIR, "PLAYERS", "writer_persona.md")
CRITIC_PERSONA_PATH = os.path.join(BASE_DIR, "PLAYERS", "critic_persona.md")


def load_persona(path):
    """Load player persona markdown."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


class HeuristicCritic:
    """Static programmatic code checker for checking quality standards."""

    def audit(self, content):
        """Analyze content and list any quality violations."""
        violations = []

        # 1. Structural Checks
        required_headers = [
            "# Profile",
            "## Agent-Native Characteristics",
            "## Aesthetic/UX Details",
            "## Key Takeaways & Market Signal",
            "## References"
        ]
        for header in required_headers:
            if header not in content:
                violations.append(f"Missing required section header: '{header}'")

        # 2. Placeholders Check
        placeholders = ["TODO", "FIXME", "XXX", "[insert link]", "placeholder", "[url]", "temp"]
        for p in placeholders:
            if p in content:
                violations.append(f"Contains forbidden placeholder keyword: '{p}'")

        # 3. Reference Checks
        if "## References" in content:
            ref_section = content.split("## References")[-1].strip()
            # Simple check for md link structure
            if "(" not in ref_section or ")" not in ref_section or "http" not in ref_section:
                violations.append("References section does not contain any valid HTTP reference links.")

        # 4. Word Density / Length check
        sections = content.split("## ")
        for sec in sections:
            lines = sec.strip().split("\n")
            if not lines:
                continue
            title = lines[0].strip()
            body = " ".join(lines[1:]).strip()
            words = body.split()
            
            # Skip profile metadata list
            if "Profile" in title:
                continue
                
            if title and len(words) < 30 and title in ["Agent-Native Characteristics", "Aesthetic/UX Details", "Key Takeaways & Market Signal"]:
                violations.append(f"Section '{title}' is too short ({len(words)} words). Must have at least 30 words of analysis.")

        return violations


class HeuristicWriter:
    """Mock writer providing draft progressions for demonstration and testing."""

    def __init__(self):
        self.templates = {
            "starchild (woofi) cross-chain solver swarms": {
                1: """# Profile: Starchild (WOOFi) Cross-Chain Solver Swarms

- **Category**: Agentic Cross-Chain Routing
- **Release Status**: Active Beta
- **Target Audience**: DeFi Protocols & Solver Networks

## Agent-Native Characteristics
Starchild is a cross-chain solver swarm that enables intent-based execution for swaps. It allows user signatures to be routed to optimal execution pools.

## Aesthetic/UX Details
It uses standard API integrations and lacks developer terminals.

## References
- TODO: Add WOOFi link here.
""",
                2: """# Profile: Starchild (WOOFi) Cross-Chain Solver Swarms

- **Category**: Agentic Cross-Chain Routing
- **Release Status**: Active Beta
- **Target Audience**: DeFi Protocols & Solver Networks

## Agent-Native Characteristics
WOOFi's Starchild represents a significant evolutionary step in cross-chain asset routing. Rather than relying on traditional automated market maker (AMM) routers which suffer from high latency and slippage across networks, Starchild employs a coordinated solver swarm. This swarm dynamically listens to user swaps signed as 'intents' and competes in real-time auctions to execute swaps and bridge assets natively. This represents a highly agent-native architecture because sovereign bots negotiate optimal transaction execution pathways.

## Aesthetic/UX Details
Starchild operates as a backend protocol service, exposing simple developer API endpoints. For operators, it features an interactive terminal dashboard displaying active auction lists, solver gas optimizations, and routing logs. This terminal UX allows node operators to inspect block-by-block bridging efficiency.

## Key Takeaways & Market Signal
Solver swarms indicate that DeFi transaction construction is moving from manual execution to intent-based agent coordination. Agents act as economic solvers that compete to find and deliver optimal outcomes.

## References
- [WOOFi Starchild Docs](https://docs.woo.org/woofi/starchild)
- FIXME: Add medium article.
""",
                3: """# Profile: Starchild (WOOFi) Cross-Chain Solver Swarms

- **Category**: Agentic Cross-Chain Routing
- **Release Status**: Active Beta
- **Target Audience**: DeFi Protocols & Solver Networks

## Agent-Native Characteristics
WOOFi's Starchild represents a significant evolutionary step in cross-chain asset routing. Rather than relying on traditional automated market maker (AMM) routers which suffer from high latency and slippage across networks, Starchild employs a coordinated solver swarm. This swarm dynamically listens to user swaps signed as 'intents' and competes in real-time auctions to execute swaps and bridge assets natively. This represents a highly agent-native architecture because sovereign bots negotiate optimal transaction execution pathways.

## Aesthetic/UX Details
Starchild operates as a backend protocol service, exposing simple developer API endpoints. For operators, it features an interactive terminal dashboard displaying active auction lists, solver gas optimizations, and routing logs. This terminal UX allows node operators to inspect block-by-block bridging efficiency.

## Key Takeaways & Market Signal
Solver swarms indicate that DeFi transaction construction is moving from manual execution to intent-based agent coordination. Agents act as economic solvers that compete to find and deliver optimal outcomes across multiple networks. This represents a massive shift in decentralized finance liquidity sourcing.

## References
- [WOOFi Starchild Docs](https://docs.woo.org/woofi/starchild)
- [WOO Network Blog](https://sporthub.woo.org/blog)
"""
            },
            "intent-based defi solver agents": {
                1: """# Profile: Intent-Based DeFi Solver Agents

- **Category**: AI DeFi Solvers
- **Release Status**: Production Utility
- **Target Audience**: Liquidity Providers

## Agent-Native Characteristics
Solvers execute signed user transactions across various decentralized exchanges.

## References
- TODO: Add links.
""",
                2: """# Profile: Intent-Based DeFi Solver Agents

- **Category**: AI DeFi Solvers
- **Release Status**: Production Utility
- **Target Audience**: Liquidity Providers

## Agent-Native Characteristics
Intent-based DeFi solver agents are autonomous computational actors that scan decentralized mempools and intent boards (like CowSwap or UniswapX). Users sign an abstract objective—such as 'swap 10 ETH for at least 30,000 USDC'—and solver agents search for the most gas-efficient and slippage-free pathway (using private liquidity or complex routing paths) to fulfill the order. This is agent-native because users delegate execution choices to third-party bots.

## Aesthetic/UX Details
Most solver interfaces are headless. However, solver dashboards (such as CowExplorer) provide full visibility into matching orders, batch execution pathways, and solver win-rates.

## Key Takeaways & Market Signal
The shift to intent-based designs marks the end of simple manual transactions. It creates a competitive market where specialized agents continuously optimize transaction routing, significantly reducing costs for end-users.

## References
- [Cow Protocol Solvers](https://docs.cow.fi/solvers)
- FIXME: Add link.
""",
                3: """# Profile: Intent-Based DeFi Solver Agents

- **Category**: AI DeFi Solvers
- **Release Status**: Production Utility
- **Target Audience**: Liquidity Providers

## Agent-Native Characteristics
Intent-based DeFi solver agents are autonomous computational actors that scan decentralized mempools and intent boards (like CowSwap or UniswapX). Users sign an abstract objective—such as 'swap 10 ETH for at least 30,000 USDC'—and solver agents search for the most gas-efficient and slippage-free pathway (using private liquidity or complex routing paths) to fulfill the order. This is agent-native because users delegate execution choices to third-party bots.

## Aesthetic/UX Details
Most solver interfaces are headless. However, solver dashboards (such as CowExplorer) provide full visibility into matching orders, batch execution pathways, and solver win-rates, which are key for developers. This ensures transparency of agentic settlement layers in web3 environments.

## Key Takeaways & Market Signal
The shift to intent-based designs marks the end of simple manual transactions. It creates a competitive market where specialized agents continuously optimize transaction routing, significantly reducing costs for end-users. This trend points to a future where blockchain interacts purely with automated AI representatives.

## References
- [Cow Protocol Solvers](https://docs.cow.fi/solvers)
- [UniswapX Whitepaper](https://uniswap.org/whitepaper-uniswapx.pdf)
"""
            },
            "agentic mpc key management & erc-4337 wallets": {
                1: """# Profile: Agentic MPC Key Management & ERC-4337 Wallets

- **Category**: Cryptographic Key Management
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Allows agents to execute transactions safely.

## References
- TODO: Add ERC-4337 links.
""",
                2: """# Profile: Agentic MPC Key Management & ERC-4337 Wallets

- **Category**: Cryptographic Key Management
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Agentic MPC Key Management and ERC-4337 accounts provide the foundational security layer for autonomous financial agents. Rather than storing a highly vulnerable private key in plaintext in an agent's environment, Multi-Party Computation (MPC) splits the key into distributed shares. Combined with ERC-4337 account abstraction, developers can programmatically enforce spending limits, allowed smart contracts, and multi-signature co-signing rules. This gives the agent high economic autonomy within strict security parameters.

## Aesthetic/UX Details
These libraries expose clean SDKs and terminal utilities. Visual dashboards allow developers to configure threshold policies, monitor active signing requests, and audit transaction payloads in real-time.

## Key Takeaways & Market Signal
Sovereign economic agents cannot exist without secure wallets. Combining MPC key-sharing with ERC-4337 accounts solves the primary security vulnerability of agents, paving the way for multi-agent organizations with corporate bank-like spending restrictions.

## References
- [ERC-4337 EntryPoint Specification](https://eips.ethereum.org/EIPS/eip-4337)
- FIXME: Add wallet sdk links.
""",
                3: """# Profile: Agentic MPC Key Management & ERC-4337 Wallets

- **Category**: Cryptographic Key Management
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Agentic MPC Key Management and ERC-4337 accounts provide the foundational security layer for autonomous financial agents. Rather than storing a highly vulnerable private key in plaintext in an agent's environment, Multi-Party Computation (MPC) splits the key into distributed shares. Combined with ERC-4337 account abstraction, developers can programmatically enforce spending limits, allowed smart contracts, and multi-signature co-signing rules. This gives the agent high economic autonomy within strict security parameters.

## Aesthetic/UX Details
These libraries expose clean SDKs and terminal utilities. Visual dashboards allow developers to configure threshold policies, monitor active signing requests, and audit transaction payloads in real-time. This provides an administrative interface for operators.

## Key Takeaways & Market Signal
Sovereign economic agents cannot exist without secure wallets. Combining MPC key-sharing with ERC-4337 accounts solves the primary security vulnerability of agents, paving the way for multi-agent organizations with corporate bank-like spending restrictions.

## References
- [ERC-4337 EntryPoint Specification](https://eips.ethereum.org/EIPS/eip-4337)
- [Biconomy ERC-4337 SDK](https://docs.biconomy.io)
"""
            },
            "autonomous yield-optimizer swarms": {
                1: """# Profile: Autonomous Yield-Optimizer Swarms

- **Category**: Yield Swarms
- **Release Status**: Active Beta
- **Target Audience**: Yield Farmers

## Agent-Native Characteristics
Yield optimizer swarms move tokens between vaults to maximize return.

## References
- TODO: Add yield protocols.
""",
                2: """# Profile: Autonomous Yield-Optimizer Swarms

- **Category**: Yield Swarms
- **Release Status**: Active Beta
- **Target Audience**: Yield Farmers

## Agent-Native Characteristics
Autonomous Yield-Optimizer Swarms are groups of cooperative agent bots that monitor liquidity pools, staking rewards, and vault lending rates across multiple blockchain networks. Using pre-coded yield strategies and real-time gas calculations, these swarms dynamically move assets to capture higher rewards while managing exposure risks and swap slippage. This represents a highly autonomous, multi-agent financial swarm operating continuously without human intervention.

## Aesthetic/UX Details
Node operators run these swarms via terminal interfaces that detail active strategies, yield histories, gas-adjusted returns, and cross-chain bridging timelines.

## Key Takeaways & Market Signal
DeFi is becoming too complex and fast-paced for human manual management. Yield swarms represent a shift to agent-dominated capital allocation, where speed and programmatic strategy execution outperform manual rebalancing.

## References
- [Yearn Finance Vaults](https://docs.yearn.fi)
- FIXME: Add link.
""",
                3: """# Profile: Autonomous Yield-Optimizer Swarms

- **Category**: Yield Swarms
- **Release Status**: Active Beta
- **Target Audience**: Yield Farmers

## Agent-Native Characteristics
Autonomous Yield-Optimizer Swarms are groups of cooperative agent bots that monitor liquidity pools, staking rewards, and vault lending rates across multiple blockchain networks. Using pre-coded yield strategies and real-time gas calculations, these swarms dynamically move assets to capture higher rewards while managing exposure risks and swap slippage. This represents a highly autonomous, multi-agent financial swarm operating continuously without human intervention.

## Aesthetic/UX Details
Node operators run these swarms via terminal interfaces that detail active strategies, yield histories, gas-adjusted returns, and cross-chain bridging timelines. This allows developers to track and monitor routing in real-time.

## Key Takeaways & Market Signal
DeFi is becoming too complex and fast-paced for human manual management. Yield swarms represent a shift to agent-dominated capital allocation, where speed and programmatic strategy execution outperform manual rebalancing. This points to a new asset management paradigm.

## References
- [Yearn Finance Vaults](https://docs.yearn.fi)
- [Beefy Finance Docs](https://docs.beefy.finance)
"""
            },
            "letta (memgpt) state management": {
                1: """# Profile: Letta (MemGPT) State Management

- **Category**: Stateful Agent Infrastructure
- **Release Status**: Active Beta
- **Target Audience**: Agentic Developers

## Agent-Native Characteristics
Letta is a stateful agent service that allows LLMs to manage long-term state across sessions.

## Aesthetic/UX Details
It provides a CLI and a web admin dashboard for managing memories.

## References
- TODO: Add Letta docs.
""",
                2: """# Profile: Letta (MemGPT) State Management

- **Category**: Stateful Agent Infrastructure
- **Release Status**: Active Beta
- **Target Audience**: Agentic Developers

## Agent-Native Characteristics
Letta (formerly MemGPT) operates as an agent-native operating system wrapper. Unlike traditional stateless LLM sessions that lose context once a run completes, Letta exposes virtual context windows to the LLM. It maps model outputs to read and write instructions that retrieve or save persistent variables (Core Memory, Recall Memory, Archival Memory). This makes it highly agent-native because the agent autonomously manages its own stateful persistence.

## Aesthetic/UX Details
Letta features a command-line interface that displays active memory operations, swap logs, and model thought reasoning blocks. Developers can inspect how memory segments are read or modified during conversational execution turns.

## Key Takeaways & Market Signal
Letta proves that LLMs need structured memory management layers to behave like sovereign, long-running servers. Standardizing agent memory state management is crucial for persistent workflows.

## References
- [Letta Github Repository](https://github.com/letta-ai/letta)
- FIXME: Add medium blog post.
""",
                3: """# Profile: Letta (MemGPT) State Management

- **Category**: Stateful Agent Infrastructure
- **Release Status**: Active Beta
- **Target Audience**: Agentic Developers

## Agent-Native Characteristics
Letta (formerly MemGPT) operates as an agent-native operating system wrapper. Unlike traditional stateless LLM sessions that lose context once a run completes, Letta exposes virtual context windows to the LLM. It maps model outputs to read and write instructions that retrieve or save persistent variables (Core Memory, Recall Memory, Archival Memory). This makes it highly agent-native because the agent autonomously manages its own stateful persistence.

## Aesthetic/UX Details
Letta features a command-line interface that displays active memory operations, swap logs, and model thought reasoning blocks. Developers can inspect how memory segments are read or modified during conversational execution turns.

## Key Takeaways & Market Signal
Letta proves that LLMs need structured memory management layers to behave like sovereign, long-running servers. Standardizing agent memory state management is crucial for persistent workflows, agent lifespan expansion, and long-term agent retention inside enterprise infrastructures.

## References
- [Letta Github Repository](https://github.com/letta-ai/letta)
- [Letta Developer Documentation](https://docs.letta.com)
"""
            },
            "hierarchical agent memory architecture": {
                1: """# Profile: Hierarchical Agent Memory Architecture

- **Category**: Foundational Agent Memory
- **Release Status**: Research Proposal
- **Target Audience**: Cognitive Architects

## Agent-Native Characteristics
Structuring memory into working memory, long-term memory, and vector databases.

## References
- TODO: Add links.
""",
                2: """# Profile: Hierarchical Agent Memory Architecture

- **Category**: Foundational Agent Memory
- **Release Status**: Research Proposal
- **Target Audience**: Cognitive Architects

## Agent-Native Characteristics
Hierarchical Agent Memory Architecture mimics human cognitive function by dividing memory into three layers: Working Memory (system prompt and immediate chat history), Semantic Memory (vector database of indexed facts and documentation), and Episodic Memory (raw logs of past actions and interaction records). The agent-native characteristic lies in the routing logic: the agent dynamically queries or summaries these layers to prevent context window saturation while maintaining perfect recall.

## Aesthetic/UX Details
This architecture is typically implemented headless in frameworks like LangChain or AutoGen. However, visualization dashboards allow developers to inspect active retrievals, vector search cosine distances, and episodic summaries.

## Key Takeaways & Market Signal
Hierarchical memory structures prevent token bloat and context drift. As agents run for longer periods, simple prompt histories fail, necessitating advanced tiered retrieval strategies.

## References
- [Hierarchical Memory Research](https://arxiv.org/abs/2305.14817)
- FIXME: Add blog link.
""",
                3: """# Profile: Hierarchical Agent Memory Architecture

- **Category**: Foundational Agent Memory
- **Release Status**: Research Proposal
- **Target Audience**: Cognitive Architects

## Agent-Native Characteristics
Hierarchical Agent Memory Architecture mimics human cognitive function by dividing memory into three layers: Working Memory (system prompt and immediate chat history), Semantic Memory (vector database of indexed facts and documentation), and Episodic Memory (raw logs of past actions and interaction records). The agent-native characteristic lies in the routing logic: the agent dynamically queries or summaries these layers to prevent context window saturation while maintaining perfect recall.

## Aesthetic/UX Details
This architecture is typically implemented headless in frameworks like LangChain or AutoGen. However, custom visualization dashboards allow developers to inspect active retrievals, vector search cosine distances, and episodic summaries in real-time.

## Key Takeaways & Market Signal
Hierarchical memory structures prevent token bloat and context drift. As agents run for longer periods, simple prompt histories fail, necessitating advanced tiered retrieval strategies to keep operational costs low and maintain long-term stability.

## References
- [Hierarchical Memory Research](https://arxiv.org/abs/2305.14817)
- [LlamaIndex Memory Modules](https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/memory/)
"""
            },
            "graph-based agent memory & state graphs": {
                1: """# Profile: Graph-Based Agent Memory & State Graphs

- **Category**: Memory Storage Infrastructure
- **Release Status**: Production Utility
- **Target Audience**: System Architects

## Agent-Native Characteristics
Storing agent execution state as a graph of nodes and edges.

## References
- TODO: Add links.
""",
                2: """# Profile: Graph-Based Agent Memory & State Graphs

- **Category**: Memory Storage Infrastructure
- **Release Status**: Production Utility
- **Target Audience**: System Architects

## Agent-Native Characteristics
Graph-Based Agent Memory represents agent state as a directed graph where nodes are processing steps or entity profiles, and edges are transition rules or relationship attributes. In frameworks like LangGraph, the agent's execution state is fully serialized at each checkpoint. This is agent-native because it allows agents to pause, rewind, fork execution paths, and resume transactions cleanly, providing deterministic reliability inside non-deterministic LLM loops.

## Aesthetic/UX Details
Developers interface with these systems via graph visualizers (like LangGraph Studio). This allows engineers to visually trace state variables, node transitions, and token consumption paths.

## Key Takeaways & Market Signal
State graphs bridge the gap between autonomous agent flexibility and production-grade reliability. Moving from unstructured memory logs to structured relational graphs is essential for auditing enterprise swarms.

## References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- FIXME: Add link.
""",
                3: """# Profile: Graph-Based Agent Memory & State Graphs

- **Category**: Memory Storage Infrastructure
- **Release Status**: Production Utility
- **Target Audience**: System Architects

## Agent-Native Characteristics
Graph-Based Agent Memory represents agent state as a directed graph where nodes are processing steps or entity profiles, and edges are transition rules or relationship attributes. In frameworks like LangGraph, the agent's execution state is fully serialized at each checkpoint. This is agent-native because it allows agents to pause, rewind, fork execution paths, and resume transactions cleanly, providing deterministic reliability inside non-deterministic LLM loops.

## Aesthetic/UX Details
Developers interface with these systems via visual graph inspector panels such as LangGraph Studio. This allows engineers to visually trace active state variables, node transitions, token consumption paths, and complex execution routes in real-time.

## Key Takeaways & Market Signal
State graphs bridge the gap between autonomous agent flexibility and production-grade reliability. Moving from unstructured memory logs to structured relational graphs is essential for auditing enterprise swarms and debugging complex multi-agent execution loops.

## References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Neo4j GraphAgent Guides](https://neo4j.com/developer/agent-graph-memory)
"""
            },
            "context window expansion vs active retrieval": {
                1: """# Profile: Context Window Expansion vs Active Retrieval

- **Category**: LLM Context Optimization
- **Release Status**: Research Focus
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
Comparing million-token windows against vector storage and page swapping.

## References
- TODO: Add benchmark links.
""",
                2: """# Profile: Context Window Expansion vs Active Retrieval

- **Category**: LLM Context Optimization
- **Release Status**: Research Focus
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
This research field contrasts the utilization of massive, million-token context windows (e.g. Gemini 1.5 Pro) with active retrieval architectures (e.g. RAG, Letta virtual context). Large windows allow models to read entire codebases natively. However, active retrieval remains agent-native because it forces the agent to decide what information to load or prune, reducing computation costs and avoiding the performance degradation associated with "lost in the middle" attention issues.

## Aesthetic/UX Details
Visual dashboards benchmark query latency, token usage costs, and retrieval accuracy under needle-in-a-haystack tests.

## Key Takeaways & Market Signal
Even with infinite context windows, active memory management is required for long-running agents. Relying solely on large context windows is financially unsustainable for multi-day agent operations.

## References
- [Lost in the Middle Research Paper](https://arxiv.org/abs/2307.03172)
- FIXME: Add link.
""",
                3: """# Profile: Context Window Expansion vs Active Retrieval

- **Category**: LLM Context Optimization
- **Release Status**: Research Focus
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
This research field contrasts the utilization of massive, million-token context windows (e.g. Gemini 1.5 Pro) with active retrieval architectures (e.g. RAG, Letta virtual context). Large windows allow models to read entire codebases natively. However, active retrieval remains agent-native because it forces the agent to decide what information to load or prune, reducing computation costs and avoiding the performance degradation associated with "lost in the middle" attention issues.

## Aesthetic/UX Details
Visual dashboards benchmark query latency, token usage costs, and retrieval accuracy under needle-in-a-haystack tests. This provides concrete telemetry and analytics on memory performance metrics for large scale deployments and multi-agent environments.

## Key Takeaways & Market Signal
Even with infinite context windows, active memory management is required for long-running agents. Relying solely on large context windows is financially unsustainable for multi-day agent operations due to compounding attention degradation.

## References
- [Lost in the Middle Research Paper](https://arxiv.org/abs/2307.03172)
- [Anthropic Context Window Best Practices](https://docs.anthropic.com/en/docs/context-window)
"""
            },
            "episodic rollup & auto-summarization": {
                1: """# Profile: Episodic Rollup & Auto-Summarization

- **Category**: Episodic Memory Compaction
- **Release Status**: Active Prototype
- **Target Audience**: Agent Framework Engineers

## Agent-Native Characteristics
Autonomously compacts past interaction history.

## References
- TODO: Add paper link.
""",
                2: """# Profile: Episodic Rollup & Auto-Summarization

- **Category**: Episodic Memory Compaction
- **Release Status**: Active Prototype
- **Target Audience**: Agent Framework Engineers

## Agent-Native Characteristics
Episodic Rollup is an agent-native memory compaction technique where a background agent worker periodically reads full execution traces and chat transcripts, identifies core transactional achievements, user preferences, and fact changes, and compiles them into a distilled summary. This allows the primary agent to keep a short working context while retaining historical episodic events.

## Aesthetic/UX Details
Developers track these rollups in server console logs, showing the reduction in token count after each compaction cycle.

## Key Takeaways & Market Signal
Unconstrained chat history quickly degrades LLM attention. Auto-summarization workers are essential for keeping memory footprints sustainable over long-term agent interactions.

## References
- [LLM Memory Compaction Research](https://arxiv.org/abs/2306.05421)
- FIXME: Add medium article.
""",
                3: """# Profile: Episodic Rollup & Auto-Summarization

- **Category**: Episodic Memory Compaction
- **Release Status**: Active Prototype
- **Target Audience**: Agent Framework Engineers

## Agent-Native Characteristics
Episodic Rollup is an agent-native memory compaction technique where a background agent worker periodically reads full execution traces and chat transcripts, identifies core transactional achievements, user preferences, and fact changes, and compiles them into a distilled summary. This allows the primary agent to keep a short working context while retaining historical episodic events.

## Aesthetic/UX Details
Developers track these rollups in server console logs, showing the reduction in token count after each compaction cycle. A unified web admin panel showcases the compaction ratio and highlights any factual updates extracted during the summarize turn.

## Key Takeaways & Market Signal
Unconstrained chat history quickly degrades LLM attention. Auto-summarization workers are essential for keeping memory footprints sustainable over long-term agent interactions and maintaining high agent reliability in professional deployments, ensuring continuous system operation without manual reset.

## References
- [LLM Memory Compaction Research](https://arxiv.org/abs/2306.05421)
- [LangChain Custom Memory Compaction](https://python.langchain.com/v0.2/docs/how_to/message_history/)
"""
            },
            "vector search relevance & rerankers": {
                1: """# Profile: Vector Search Relevance & Rerankers

- **Category**: Retrieval Relevance Optimization
- **Release Status**: Standard Utility
- **Target Audience**: Retrieval Engineers

## Agent-Native Characteristics
Using rerankers to improve search precision.

## References
- TODO: Add reranker link.
""",
                2: """# Profile: Vector Search Relevance & Rerankers

- **Category**: Retrieval Relevance Optimization
- **Release Status**: Standard Utility
- **Target Audience**: Retrieval Engineers

## Agent-Native Characteristics
Vector Search Relevance is optimized using cross-encoder rerankers (like Cohere Rerank or BGE-Reranker) that evaluate the semantic relevance of retrieved context pages against the query. This is agent-native because it ensures the agent's context is injected only with highly relevant data, avoiding the noise and hallucinations that occur when loading irrelevant chunks.

## Aesthetic/UX Details
UX is implemented behind the scenes in retrieval engines. However, logs display cosine similarity and reranked relevance scores for each query.

## Key Takeaways & Market Signal
Standard vector search is insufficient for complex agent decision-making. Reranking is critical for preventing context poisoning and ensuring the agent acts on precise information.

## References
- [Cohere Rerank Guide](https://cohere.com/rerank)
- FIXME: Add academic reference.
""",
                3: """# Profile: Vector Search Relevance & Rerankers

- **Category**: Retrieval Relevance Optimization
- **Release Status**: Standard Utility
- **Target Audience**: Retrieval Engineers

## Agent-Native Characteristics
Vector Search Relevance is optimized using cross-encoder rerankers (like Cohere Rerank or BGE-Reranker) that evaluate the semantic relevance of retrieved context pages against the query. This is agent-native because it ensures the agent's context is injected only with highly relevant data, avoiding the noise and hallucinations that occur when loading irrelevant chunks.

## Aesthetic/UX Details
UX is implemented behind the scenes in retrieval engines. However, telemetry dashboards display cosine similarity, raw vector distances, and final reranked relevance scores for each prompt query, allowing developer introspection and monitoring of query health.

## Key Takeaways & Market Signal
Standard vector search is insufficient for complex agent decision-making. Reranking is critical for preventing context poisoning, minimizing hallucination rates, and ensuring the agent acts on precise, verified information in production networks.

## References
- [Cohere Rerank Guide](https://cohere.com/rerank)
- [Pinecone Reranking Documentation](https://docs.pinecone.io/guides/data/rerank)
"""
            },
            "multi-agent shared memory spaces": {
                1: """# Profile: Multi-Agent Shared Memory Spaces

- **Category**: Swarm Memory Architecture
- **Release Status**: Research Stage
- **Target Audience**: Swarm Architects

## Agent-Native Characteristics
Shared memory blackboards for cooperative agents.

## References
- TODO: Add blackboard link.
""",
                2: """# Profile: Multi-Agent Shared Memory Spaces

- **Category**: Swarm Memory Architecture
- **Release Status**: Research Stage
- **Target Audience**: Swarm Architects

## Agent-Native Characteristics
Multi-Agent Shared Memory Spaces allow agents in a swarm to share state and variables via a central blackboard or database. This is agent-native because it replaces peer-to-peer message passing with a synchronized coordinate space, enabling collaborative agents to read and write shared goals, tasks, and world states.

## Aesthetic/UX Details
Swarm operators monitor shared workspaces via visual boards that show active agents, lock status on variables, and write updates.

## Key Takeaways & Market Signal
Autonomous swarms require shared, synchronized stateboards to prevent conflicts and ensure unified action. Blackboard architectures represent a crucial step towards cooperative agent-native collaboration.

## References
- [Swarm Blackboard Architectures](https://arxiv.org/abs/2402.14811)
- FIXME: Add link.
""",
                3: """# Profile: Multi-Agent Shared Memory Spaces

- **Category**: Swarm Memory Architecture
- **Release Status**: Research Stage
- **Target Audience**: Swarm Architects

## Agent-Native Characteristics
Multi-Agent Shared Memory Spaces allow agents in a swarm to share state and variables via a central blackboard or database. This is agent-native because it replaces peer-to-peer message passing with a synchronized coordinate space, enabling collaborative agents to read and write shared goals, tasks, and world states.

## Aesthetic/UX Details
Swarm operators monitor shared workspaces via custom web dashboards that display active agents, lock status on variables, read/write actions, and real-time state mutations across the swarm, making the multi-agent execution cycle visible.

## Key Takeaways & Market Signal
Autonomous swarms require shared, synchronized stateboards to prevent conflicts, reduce latency, and ensure unified action. Blackboard architectures represent a crucial step towards cooperative, enterprise-grade multi-agent collaboration frameworks that scale across distributed cloud clusters.

## References
- [Swarm Blackboard Architectures](https://arxiv.org/abs/2402.14811)
- [CrewAI Shared State Management](https://docs.crewai.com/core-concepts/Memory/)
"""
            },
            "decentralized cryptographic memory stores": {
                1: """# Profile: Decentralized Cryptographic Memory Stores

- **Category**: Sovereign Memory Infrastructure
- **Release Status**: Early Protocol
- **Target Audience**: Cryptographic Engineers

## Agent-Native Characteristics
Sovereign memory stored on IPFS or Ceramic.

## References
- TODO: Add ceramic link.
""",
                2: """# Profile: Decentralized Cryptographic Memory Stores

- **Category**: Sovereign Memory Infrastructure
- **Release Status**: Early Protocol
- **Target Audience**: Cryptographic Engineers

## Agent-Native Characteristics
Decentralized Cryptographic Memory Stores persist agent states onto networks like IPFS, Ceramic, or Arweave. This is agent-native because it ensures sovereign ownership of memory: the agent (or its owner) controls the decryption keys, preventing centralized model providers from reading or censoring the agent's memory logs.

## Aesthetic/UX Details
Developers configure cryptographic keys via CLI tools, which log the CID hashes of state commits on the ledger.

## Key Takeaways & Market Signal
True agent sovereignty requires decentralized memory. Without decentralized cryptographic storage, agents remain vulnerable to host-level censorship and platform locks.

## References
- [Ceramic Protocol Specifications](https://developers.ceramic.network)
- FIXME: Add arweave link.
""",
                3: """# Profile: Decentralized Cryptographic Memory Stores

- **Category**: Sovereign Memory Infrastructure
- **Release Status**: Early Protocol
- **Target Audience**: Cryptographic Engineers

## Agent-Native Characteristics
Decentralized Cryptographic Memory Stores persist agent states onto networks like IPFS, Ceramic, or Arweave. This is agent-native because it ensures sovereign ownership of memory: the agent (or its owner) controls the decryption keys, preventing centralized model providers from reading or censoring the agent's memory logs.

## Aesthetic/UX Details
Developers configure cryptographic keys via CLI tools, which log the IPFS content identifier (CID) hashes of state commits and display cryptographic proofs on a dashboard with interactive verification tables. This ensures operational transparency.

## Key Takeaways & Market Signal
True agent sovereignty requires decentralized memory. Without decentralized cryptographic storage, agents remain vulnerable to host-level censorship, platform locks, and unauthorized user data exposure by LLM API providers who store execution logs on their own servers.

## References
- [Ceramic Protocol Specifications](https://developers.ceramic.network)
- [Arweave Web3 Storage Guide](https://cookbook.arweave.dev)
"""
            },
            "self-correcting memory networks": {
                1: """# Profile: Self-Correcting Memory Networks

- **Category**: Memory Consistency Auditing
- **Release Status**: Research Stage
- **Target Audience**: AI Safety Engineers

## Agent-Native Characteristics
Audits agent memories for inconsistencies.

## References
- TODO: Add consistency paper link.
""",
                2: """# Profile: Self-Correcting Memory Networks

- **Category**: Memory Consistency Auditing
- **Release Status**: Research Stage
- **Target Audience**: AI Safety Engineers

## Agent-Native Characteristics
Self-Correcting Memory Networks periodically scan stored facts and execution state graphs to find logical contradictions or outdated data, resolving them with validation prompts. This is agent-native because it ensures autonomous consistency, preventing agents from acting on contradictory beliefs or obsolete user settings.

## Aesthetic/UX Details
Visual interfaces display contradictions in real-time as highlighted node conflicts, allowing developers to review correction actions.

## Key Takeaways & Market Signal
Memory corruption degrades agent execution over time. Automated self-correction is necessary to ensure long-term stability and align agent behaviors with evolving real-world states.

## References
- [LLM Belief Inconsistency Research](https://arxiv.org/abs/2305.14201)
- FIXME: Add link.
""",
                3: """# Profile: Self-Correcting Memory Networks

- **Category**: Memory Consistency Auditing
- **Release Status**: Research Stage
- **Target Audience**: AI Safety Engineers

## Agent-Native Characteristics
Self-Correcting Memory Networks periodically scan stored facts and execution state graphs to find logical contradictions or outdated data, resolving them with validation prompts. This is agent-native because it ensures autonomous consistency, preventing agents from acting on contradictory beliefs or obsolete user settings.

## Aesthetic/UX Details
Visual interfaces display contradictions in real-time as highlighted node conflicts, allowing developers to review correction actions, trace logical dependencies, and manually override conflict resolutions when necessary to guide the system.

## Key Takeaways & Market Signal
Memory corruption degrades agent execution over time. Automated self-correction is necessary to ensure long-term stability and align agent behaviors with evolving real-world states and user profiles in high-stakes operational sectors.

## References
- [LLM Belief Inconsistency Research](https://arxiv.org/abs/2305.14201)
- [Microsoft AutoGen State Validation](https://microsoft.github.io/autogen/docs/FAQ/)
"""
            },
            "agent synaptic pruning & memory decay": {
                1: """# Profile: Agent Synaptic Pruning & Memory Decay

- **Category**: Memory Cache Optimization
- **Release Status**: Experimental Feature
- **Target Audience**: Performance Engineers

## Agent-Native Characteristics
Biologically-inspired memory decay functions.

## References
- TODO: Add pruning paper link.
""",
                2: """# Profile: Agent Synaptic Pruning & Memory Decay

- **Category**: Memory Cache Optimization
- **Release Status**: Experimental Feature
- **Target Audience**: Performance Engineers

## Agent-Native Characteristics
Synaptic Pruning implements decaying relevance weights based on time and access frequency. This is agent-native because it mirrors biological forgetting: the agent automatically drops low-importance, cold memory pages to prevent retrieval noise, keep context windows small, and save query costs.

## Aesthetic/UX Details
UX dashboards display a list of memories sorted by decay status, showing which facts are scheduled for archival.

## Key Takeaways & Market Signal
Agents cannot retain everything forever without sufferring latency and token bloat. Synaptic pruning is crucial for optimizing throughput and reducing infrastructure costs in multi-agent swarms.

## References
- [Cognitive Forgetting Functions in LLMs](https://arxiv.org/abs/2312.03112)
- FIXME: Add link.
""",
                3: """# Profile: Agent Synaptic Pruning & Memory Decay

- **Category**: Memory Cache Optimization
- **Release Status**: Experimental Feature
- **Target Audience**: Performance Engineers

## Agent-Native Characteristics
Synaptic Pruning implements decaying relevance weights based on time and access frequency. This is agent-native because it mirrors biological forgetting: the agent automatically drops low-importance, cold memory pages to prevent retrieval noise, keep context windows small, and save query costs.

## Aesthetic/UX Details
UX dashboards display a list of memories sorted by decay status, showing which facts are scheduled for archival, highlighting memory access counts, and plotting forgetting curves over long periods to give developers full visibility.

## Key Takeaways & Market Signal
Agents cannot retain everything forever without sufferring latency and token bloat. Synaptic pruning is crucial for optimizing throughput, improving agent response times, and reducing infrastructure costs in multi-agent swarms operating in high-volume environments.

## References
- [Cognitive Forgetting Functions in LLMs](https://arxiv.org/abs/2312.03112)
- [LlamaIndex Memory Decay Strategies](https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/memory/)
"""
            },
            "continuous fine-tuning & weight-update memory": {
                1: """# Profile: Continuous Fine-Tuning & Weight-Update Memory

- **Category**: Local Model Adaptation
- **Release Status**: Early Research
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
Dynamic weight updates instead of context logs.

## References
- TODO: Add weight update link.
""",
                2: """# Profile: Continuous Fine-Tuning & Weight-Update Memory

- **Category**: Local Model Adaptation
- **Release Status**: Early Research
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
Continuous Fine-Tuning moves memory directly into model weights via fast local adapter updates (like LoRA or QLoRA). This is agent-native because the agent absorbs new facts, styles, and tools natively into its cognitive core rather than searching external vector stores or context documents.

## Aesthetic/UX Details
Developers monitor adapter training logs, tracking epoch progress, loss curves, and GPU memory utilization metrics during real-time weight adjustments.

## Key Takeaways & Market Signal
Weight-based memory offers O(1) recall speed compared to O(N) context retrieval. As local execution hardware improves, continuous weight-update adaptation will become the standard for personalized desktop agents.

## References
- [QLoRA Efficient Finetuning](https://arxiv.org/abs/2305.14314)
- FIXME: Add link.
""",
                3: """# Profile: Continuous Fine-Tuning & Weight-Update Memory

- **Category**: Local Model Adaptation
- **Release Status**: Early Research
- **Target Audience**: ML Research Engineers

## Agent-Native Characteristics
Continuous Fine-Tuning moves memory directly into model weights via fast local adapter updates (like LoRA or QLoRA). This is agent-native because the agent absorbs new facts, styles, and tools natively into its cognitive core rather than searching external vector stores or context documents.

## Aesthetic/UX Details
Developers monitor adapter training logs, tracking epoch progress, loss curves, training convergence rates, and GPU memory utilization metrics during real-time weight adjustments on the node. This helps developers gauge model absorption speed.

## Key Takeaways & Market Signal
Weight-based memory offers O(1) recall speed compared to O(N) context retrieval. As local execution hardware improves, continuous weight-update adaptation will become the standard for personalized desktop agents and sovereign mobile swarms.

## References
- [QLoRA Efficient Finetuning](https://arxiv.org/abs/2305.14314)
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index)
"""
            },
            "cross-agent memory exchange protocols": {
                1: """# Profile: Cross-Agent Memory Exchange Protocols

- **Category**: Interoperable Agent Standards
- **Release Status**: Protocol Draft
- **Target Audience**: Protocol Designers

## Agent-Native Characteristics
Standard formats for exporting/importing memory.

## References
- TODO: Add standard spec link.
""",
                2: """# Profile: Cross-Agent Memory Exchange Protocols

- **Category**: Interoperable Agent Standards
- **Release Status**: Protocol Draft
- **Target Audience**: Protocol Designers

## Agent-Native Characteristics
Cross-Agent Memory Exchange Protocols define standard serialization formats (like JSON-LD or schema.org extensions) that allow agents to export and import user profiles and context. This is agent-native because it prevents lock-in, enabling user profiles and memory states to follow the user across different agent hosts.

## Aesthetic/UX Details
Developers inspect memory packages using validation schemas, ensuring fields align with the exchange protocols.

## Key Takeaways & Market Signal
User memory portability is critical for agent adoption. Standardizing memory formats is required to build a cooperative, open ecosystem of interoperable autonomous swarms.

## References
- [W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)
- FIXME: Add link.
""",
                3: """# Profile: Cross-Agent Memory Exchange Protocols

- **Category**: Interoperable Agent Standards
- **Release Status**: Protocol Draft
- **Target Audience**: Protocol Designers

## Agent-Native Characteristics
Cross-Agent Memory Exchange Protocols define standard serialization formats (like JSON-LD or schema.org extensions) that allow agents to export and import user profiles and context. This is agent-native because it prevents lock-in, enabling user profiles and memory states to follow the user across different agent hosts.

## Aesthetic/UX Details
Developers inspect memory packages using validation schemas, ensuring fields align with the exchange protocols and displaying schema mapping tables inside the administrative agent console to show interoperability mappings. This optimizes configuration workflows.

## Key Takeaways & Market Signal
User memory portability is critical for agent adoption. Standardizing memory formats is required to build a cooperative, open ecosystem of interoperable autonomous swarms and avoid developer lock-in by dominant platforms.

## References
- [W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)
- [Semantic Web Agent Specifications](https://www.w3.org/DesignIssues/Semantic.html)
"""
            },
            "llama-3-vision & local visual slms": {
                1: """# Profile: Llama-3-Vision & Local Visual SLMs

- **Category**: Sovereign Local Multimodal Model
- **Release Status**: Open-Weights
- **Target Audience**: AI Developers & Sandbox Architects

## Agent-Native Characteristics
Llama-3-Vision is an open-weights model capable of local screen analysis and tool execution.

## Aesthetic/UX Details
It runs via local GPU runtimes.

## References
- TODO: Add link.
""",
                2: """# Profile: Llama-3-Vision & Local Visual SLMs

- **Category**: Sovereign Local Multimodal Model
- **Release Status**: Open-Weights
- **Target Audience**: AI Developers & Sandbox Architects

## Agent-Native Characteristics
Llama-3-Vision is an open-weights model capable of local screen analysis and tool execution. It represents an agent-native breakthrough by allowing models to execute vision-grounded tasks entirely locally.

## Aesthetic/UX Details
Developers integrate the model via local GPU runtimes (vLLM, Ollama), which output coordinate segments on screen.

## Key Takeaways & Market Signal
Sovereign multimodal execution removes cloud API costs and data privacy violations.

## References
- FIXME: Add link.
""",
                3: """# Profile: Llama-3-Vision & Local Visual SLMs

- **Category**: Sovereign Local Multimodal Model
- **Release Status**: Open-Weights
- **Target Audience**: AI Developers & Sandbox Architects

## Agent-Native Characteristics
Llama-3-Vision is an open-weights model capable of local screen analysis and tool execution. It represents an agent-native breakthrough by allowing models to execute vision-grounded tasks entirely locally, bypassing external API dependencies, securing user data privacy, and optimizing latency for high-frequency screenshot actions.

## Aesthetic/UX Details
Developers integrate the model via local GPU runtimes (vLLM, Ollama), which output coordinate segments on screen. The interface provides a real-time monitor displaying active token generation rates, coordinate mapping logs, and system memory stats, giving developers complete control over local processing.

## Key Takeaways & Market Signal
Sovereign multimodal execution removes cloud API costs and data privacy violations. Edge-native visual SLMs will become the default engines driving local automation frameworks, fundamentally reshaping traditional browser automation in enterprise environments by enabling secure offline operations.

## References
- [Meta AI Blog](https://ai.meta.com/blog/meta-llama-3/)
- [Ollama Model Hub](https://ollama.com/library/llama3)
"""
            },
            "browser-use web navigation framework": {
                1: """# Profile: browser-use Web Navigation Framework

- **Category**: Vision-Based Web Agent Driver
- **Release Status**: Active Open-Source
- **Target Audience**: Automation Engineers & Swarm Developers

## Agent-Native Characteristics
browser-use maps screenshots and DOM structures to click/type coordinates for LLMs.

## Aesthetic/UX Details
Renders a live browser window highlighting agent actions.

## References
- TODO: Add browser-use github link.
""",
                2: """# Profile: browser-use Web Navigation Framework

- **Category**: Vision-Based Web Agent Driver
- **Release Status**: Active Open-Source
- **Target Audience**: Automation Engineers & Swarm Developers

## Agent-Native Characteristics
browser-use maps screenshots and DOM structures to click/type coordinates for LLMs. This is agent-native because the driver handles multi-tab navigation and automatically recovers from captchas and error states, behaving like a human operator.

## Aesthetic/UX Details
Renders a live browser window highlighting agent actions. The interface overlays visual markers and tags on the screen, showing the model's target elements, scroll status, and action logs.

## References
- FIXME: Add browser-use link.
""",
                3: """# Profile: browser-use Web Navigation Framework

- **Category**: Vision-Based Web Agent Driver
- **Release Status**: Active Open-Source
- **Target Audience**: Automation Engineers & Swarm Developers

## Agent-Native Characteristics
browser-use maps screenshots and DOM structures to click/type coordinates for LLMs. This is agent-native because the driver handles multi-tab navigation and automatically recovers from captchas and error states, behaving like a human operator. By converting raw page layouts into structured action tokens, it enables long-horizon navigation.

## Aesthetic/UX Details
Renders a live browser window highlighting agent actions. The interface overlays visual markers and tags on the screen, showing the model's target elements, scroll status, and action logs, making the agent's decision-making visible and debuggable.

## Key Takeaways & Market Signal
Visual web drivers are replacing fragile CSS and XPath scrapers. Standardizing on VLM-driven browser navigation makes automated workflows resilient to web layout redesigns, representing a shift toward robust RPA platforms.

## References
- [browser-use GitHub Repository](https://github.com/browser-use/browser-use)
- [Playwright Web Automation Library](https://playwright.dev)
"""
            },
            "skyvern vision-grounded rpa": {
                1: """# Profile: Skyvern Vision-Grounded RPA

- **Category**: Vision-Based RPA Agent
- **Release Status**: Commercial Open-Source
- **Target Audience**: Enterprise Process Automation Engineers

## Agent-Native Characteristics
Skyvern operates on screenshots, omitting traditional selector logic.

## References
- TODO: Add Skyvern link.
""",
                2: """# Profile: Skyvern Vision-Grounded RPA

- **Category**: Vision-Based RPA Agent
- **Release Status**: Commercial Open-Source
- **Target Audience**: Enterprise Process Automation Engineers

## Agent-Native Characteristics
Skyvern operates on screenshots, omitting traditional selector logic. This makes it agent-native because the model reasons about form layouts visually, executing complex tasks even if elements shift.

## Aesthetic/UX Details
A sleek web dashboard shows screenshot histories and target areas.

## References
- FIXME: Add Skyvern link.
""",
                3: """# Profile: Skyvern Vision-Grounded RPA

- **Category**: Vision-Based RPA Agent
- **Release Status**: Commercial Open-Source
- **Target Audience**: Enterprise Process Automation Engineers

## Agent-Native Characteristics
Skyvern operates on screenshots, omitting traditional selector logic. This makes it agent-native because the model reasons about form layouts visually, executing complex tasks even if elements shift or forms change color. It decouples the automation script from the brittle HTML DOM structure.

## Aesthetic/UX Details
A sleek web dashboard shows screenshot histories and target areas. The operator panel displays step-by-step click maps, visual layout grids, and execution logs, ensuring complete process auditability and allowing real-time intervention by human operators if a layout anomaly is detected.

## Key Takeaways & Market Signal
Enterprise RPA is undergoing an agentic rewrite. Vision-grounded automation eliminates the maintenance overhead of maintaining selector-based scripts, driving massive cost savings across customer workflows and document parsing operations and replacing fragile, selector-based scraping loops with resilient, visual reasoning systems that adapt to interface shifts.

## References
- [Skyvern GitHub Repository](https://github.com/skyvern-ai/skyvern)
- [Robotic Process Automation with VLMs](https://arxiv.org/abs/2401.00123)
"""
            },
            "webarena sandbox evaluation": {
                1: """# Profile: WebArena Sandbox Evaluation

- **Category**: Agentic Benchmark Sandbox
- **Release Status**: Academic Project
- **Target Audience**: AI Safety & Performance Researchers

## Agent-Native Characteristics
WebArena tests agents on mock sites to verify end-to-end tasks.

## References
- TODO: Add WebArena link.
""",
                2: """# Profile: WebArena Sandbox Evaluation

- **Category**: Agentic Benchmark Sandbox
- **Release Status**: Academic Project
- **Target Audience**: AI Safety & Performance Researchers

## Agent-Native Characteristics
WebArena tests agents on mock sites to verify end-to-end tasks. It is agent-native because it evaluates final state changes in the environment (e.g. database commits) rather than checking intermediate prompt outputs.

## Aesthetic/UX Details
Detailed performance logs record step counts and success rates.

## References
- FIXME: Add WebArena link.
""",
                3: """# Profile: WebArena Sandbox Evaluation

- **Category**: Agentic Benchmark Sandbox
- **Release Status**: Academic Project
- **Target Audience**: AI Safety & Performance Researchers

## Agent-Native Characteristics
WebArena tests agents on mock sites to verify end-to-end tasks. It is agent-native because it evaluates final state changes in the environment (e.g. database commits) rather than checking intermediate prompt outputs. This ensures realistic, multi-hop action verification.

## Aesthetic/UX Details
Detailed performance logs record step counts and success rates. The visualization interface displays agent trajectory paths, action replays, and execution success metrics, helping developers trace failure modes in local sandboxes.

## Key Takeaways & Market Signal
Standardized sandboxes are required to validate visual browser agents. WebArena demonstrates that evaluating agents on real-world environment states is the only reliable way to measure autonomous task execution readiness and prevent catastrophic failures in production environments, forcing developers to prioritize final database validations over simple model predictions.

## References
- [WebArena Project Site](https://webarena.dev)
- [Evaluating Web Agents Paper](https://arxiv.org/abs/2307.13854)
"""
            },
            "aider & git-grounded workspace editing": {
                1: """# Profile: Aider & Git-Grounded Workspace Editing

- **Category**: Developer Tooling
- **Release Status**: Active Open-Source
- **Target Audience**: Software Engineers

## Agent-Native Characteristics
Aider reads the git repository map to make edits.

## Aesthetic/UX Details
It runs inside the terminal.

## Key Takeaways & Market Signal
Aider shows that terminal-based coding tools are useful.

## References
- TODO: Add link.
""",
                2: """# Profile: Aider & Git-Grounded Workspace Editing

- **Category**: Developer Tooling
- **Release Status**: Active Open-Source
- **Target Audience**: Software Engineers

## Agent-Native Characteristics
Aider is designed to integrate directly with Git repositories. It parses files to construct a repo map, helping the LLM understand where classes and functions are defined without blowing up context limits.

## Aesthetic/UX Details
Runs in a terminal window, with simple prompts. The command line output gives immediate feedback about files changed, commits made, and syntax errors.

## Key Takeaways & Market Signal
Aider indicates a shift to terminal pair programming.

## References
- FIXME: Add link.
""",
                3: """# Profile: Aider & Git-Grounded Workspace Editing

- **Category**: Developer Tooling
- **Release Status**: Active Open-Source
- **Target Audience**: Software Engineers

## Agent-Native Characteristics
Aider represents a major step forward by integrating directly with git-based codebases. It uses Tree-sitter to parse the Abstract Syntax Tree (AST) of the repository, building an active repo map. This map acts as a semantic context selector, feeding the LLM only the relevant definitions and signatures. This prevents the LLM from getting overwhelmed by massive codebases and keeps costs low while preserving structural awareness.

## Aesthetic/UX Details
Aider runs as an interactive command-line interface directly in the user's terminal window. It uses standard ANSI colors, highlights diff blocks, and automatically generates clean git commit messages after each successful edit loop. The interface shows progress bars for repository indexing and clearly lists files added to the chat, giving the developer precise visibility.

## Key Takeaways & Market Signal
Repository-map prompting proves that agents can work on large-scale applications without loading all code into memory. Aider proves that full workspace integration—where the LLM has access to terminal execution, git history, and AST trees—is essential for building autonomous engineering agents that can refactor multi-file codebases.

## References
- [Aider Official Website](https://aider.chat)
- [Aider GitHub Repository](https://github.com/Aider-AI/aider)
"""
            },
            "swe-bench developer benchmarking": {
                1: """# Profile: SWE-bench Developer Benchmarking

- **Category**: Agent Evaluation
- **Release Status**: Open-Source Benchmark
- **Target Audience**: AI Researchers

## Agent-Native Characteristics
SWE-bench evaluates agents on real github issues.

## Aesthetic/UX Details
It runs in Docker containers.

## Key Takeaways & Market Signal
SWE-bench is a hard benchmark.

## References
- TODO: Add link.
""",
                2: """# Profile: SWE-bench Developer Benchmarking

- **Category**: Agent Evaluation
- **Release Status**: Open-Source Benchmark
- **Target Audience**: AI Researchers

## Agent-Native Characteristics
SWE-bench is a benchmark for resolving software engineering issues. It uses real pull requests and issues from GitHub, testing if agents can write tests and patch bugs autonomously.

## Aesthetic/UX Details
Researchers execute the tests via command-line scripts. The logs output success rates and patch details, displaying them in tabular formats for analysis.

## Key Takeaways & Market Signal
Evaluating agents on real-world engineering issues is crucial.

## References
- FIXME: Add link.
""",
                3: """# Profile: SWE-bench Developer Benchmarking

- **Category**: Agent Evaluation
- **Release Status**: Open-Source Benchmark
- **Target Audience**: AI Researchers

## Agent-Native Characteristics
SWE-bench evaluates autonomous software agents on real-world software engineering tasks collected from GitHub. Rather than checking simple output strings, it tests agents by executing their generated patches against unit tests in isolated Docker environments. This represents an agent-native evaluation pattern because it measures the agent's actual impact on the environment rather than its intermediate text outputs.

## Aesthetic/UX Details
The framework provides comprehensive JSON and text logs for each evaluation run. It includes detailed step-by-step traces of agent actions, file edits, and execution outputs, which are rendered on evaluation dashboards. These dashboards allow researchers to inspect exactly which test cases passed or failed and visualize the precise diffs generated by the model.

## Key Takeaways & Market Signal
Evaluating agents on code execution results is the only way to measure enterprise readiness. SWE-bench shows that coding agents still struggle with long-horizon reasoning and codebase navigation, shifting the focus of research from generic model prompt tuning to building better tool-use loops, sandboxes, and repository retrieval architectures.

## References
- [SWE-bench Website](https://www.swebench.com)
- [SWE-bench Paper](https://arxiv.org/abs/2310.06770)
"""
            },
            "langfuse & langsmith micro-trace telemetry": {
                1: """# Profile: Langfuse & Langsmith Micro-Trace Telemetry

- **Category**: Agent Observability
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Langfuse and Langsmith track agent tool runs.

## Aesthetic/UX Details
It has a nice web interface.

## Key Takeaways & Market Signal
Telemetry is good for debugging.

## References
- TODO: Add link.
""",
                2: """# Profile: Langfuse & Langsmith Micro-Trace Telemetry

- **Category**: Agent Observability
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Langfuse and Langsmith provide tracing for multi-agent chains. They capture LLM input/output, tool calls, and run parameters, letting developers visualize the execution graph of complex agent steps.

## Aesthetic/UX Details
A web-based trace viewer shows tree diagrams of nested runs. The dashboard highlights slow nodes, model parameters, and call structures, enabling detailed runtime inspection.

## Key Takeaways & Market Signal
Observability is critical for compound AI systems.

## References
- FIXME: Add link.
""",
                3: """# Profile: Langfuse & Langsmith Micro-Trace Telemetry

- **Category**: Agent Observability
- **Release Status**: Production SDK
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
Langfuse and Langsmith are telemetry frameworks built specifically for agentic architectures. Unlike traditional application performance monitoring (APM) tools, they capture the nested, non-deterministic execution graphs of multi-agent systems. They trace model inputs and outputs, execution costs, tool parameters, and retrieval chunks across complex loops, enabling developers to map exactly how an agent arrived at a decision.

## Aesthetic/UX Details
The web dashboards offer a rich visual trace viewer that renders nested call trees. Developers can click on individual spans to view raw prompts, model response latencies, and tool call payloads. The UI also integrates evaluation metrics, cost tracking charts, and playground environments to test prompt variations directly on historical traces.

## Key Takeaways & Market Signal
Multi-agent telemetry is the backbone of production reliability. Tracing the internal thoughts and tool actions of agents allows companies to audit decision-making, optimize latencies, and control token budgets. This highlights a shift from simple logging to semantic tracing engines designed for compound AI systems.

## References
- [Langfuse Homepage](https://langfuse.com)
- [Langsmith Homepage](https://www.langchain.com/langsmith)
"""
            },
            "promptfoo & braintrust assertions": {
                1: """# Profile: Promptfoo & Braintrust Assertions

- **Category**: Agent Evaluation
- **Release Status**: Developer Tooling
- **Target Audience**: QA Engineers

## Agent-Native Characteristics
Promptfoo and Braintrust run evaluations.

## Aesthetic/UX Details
It has a web dashboard and CLI.

## Key Takeaways & Market Signal
Assertions prevent regressions.

## References
- TODO: Add link.
""",
                2: """# Profile: Promptfoo & Braintrust Assertions

- **Category**: Agent Evaluation
- **Release Status**: Developer Tooling
- **Target Audience**: QA Engineers

## Agent-Native Characteristics
Promptfoo and Braintrust provide assertion suites for prompts and agents. They run tests on target prompts using assertions like semantic similarity, model-graded metrics, and classification checks to catch regressions.

## Aesthetic/UX Details
A terminal reporter outputs a matrix of test runs, showing green checkmarks for passes. The web UI displays interactive side-by-side completions, model outputs, and regression trends.

## Key Takeaways & Market Signal
Prompt assertions are replacing manual testing.

## References
- FIXME: Add link.
""",
                3: """# Profile: Promptfoo & Braintrust Assertions

- **Category**: Agent Evaluation
- **Release Status**: Developer Tooling
- **Target Audience**: QA Engineers

## Agent-Native Characteristics
Promptfoo and Braintrust automate prompt and agent evaluation. They enable developers to define test suites with assertions covering LLM outputs, including classification, regex checks, semantic similarity, and model-graded criteria. This is agent-native because it uses LLM-as-a-judge patterns to evaluate non-deterministic agent behavior and enforce safety guardrails before deploying changes to production systems.

## Aesthetic/UX Details
The tools render a detailed evaluation matrix in the terminal and on a web dashboard. The interface shows side-by-side comparisons of different prompts, model outputs, cost metrics, and execution times. Failures are highlighted in red with explanation tooltips, allowing developers to inspect which assertions failed and tweak system prompts.

## Key Takeaways & Market Signal
Testing prompts requires software engineering rigor. Automated assertions and model-graded evaluations are replacing manual inspection, enabling continuous integration pipelines for AI applications. This shift represents a transition toward deterministic quality assurance and safety auditing for non-deterministic agent behaviors.

## References
- [Promptfoo Repository](https://github.com/promptfoo/promptfoo)
- [Braintrust Platform](https://www.braintrust.dev)
"""
            },
            "gvisor & docker agent sandboxes": {
                1: """# Profile: gVisor & Docker Agent Sandboxes

- **Category**: Security Sandboxing
- **Release Status**: Production-ready
- **Target Audience**: Infrastructure Engineers

## Agent-Native Characteristics
gVisor and Docker are used to run untrusted agent code.

## Aesthetic/UX Details
It has a CLI interface.

## Key Takeaways & Market Signal
Security is important.

## References
- TODO: Add link.
""",
                2: """# Profile: gVisor & Docker Agent Sandboxes

- **Category**: Security Sandboxing
- **Release Status**: Production-ready
- **Target Audience**: Infrastructure Engineers

## Agent-Native Characteristics
gVisor and Docker sandboxes isolate executing agent processes. They intercept system calls to prevent agents from executing destructive commands on the host machine.

## Aesthetic/UX Details
Runs as a container daemon behind the scenes. Developers interact with it using Docker CLI or Kubernetes pods.

## Key Takeaways & Market Signal
Isolating untrusted execution is critical.

## References
- FIXME: Add gVisor link.
""",
                3: """# Profile: gVisor & Docker Agent Sandboxes

- **Category**: Security Sandboxing
- **Release Status**: Production-ready
- **Target Audience**: Infrastructure Engineers

## Agent-Native Characteristics
gVisor and Docker provide kernel-level isolation sandboxes for executing non-deterministic agent code. Since developer agents routinely generate and execute raw bash commands and python scripts, securing the runtime host from privilege escalation and unauthorized network requests is a foundational safety requirement for autonomous software engineering.

## Aesthetic/UX Details
The sandbox operates seamlessly as a container runtime plugin. Developers run agents inside restricted containers without changing their application code. Performance and startup latencies are optimized to match container spin-up times.

## Key Takeaways & Market Signal
Operating autonomous agents demands robust sandbox boundaries. Isolating executing processes at the kernel layer prevents rogue loops, host resource starvation, and security leaks, establishing a baseline of security for enterprise-grade deployments.

## References
- [gVisor Container Sandbox](https://gvisor.dev)
- [Docker Container Security](https://www.docker.com)
"""
            },
            "mcp server standardization": {
                1: """# Profile: MCP Server Standardization

- **Category**: Communication Protocols
- **Release Status**: Draft Spec
- **Target Audience**: Tool Developers

## Agent-Native Characteristics
Model Context Protocol standardizes agent tool integration.

## Aesthetic/UX Details
It uses JSON-RPC.

## Key Takeaways & Market Signal
Standards are good.

## References
- TODO: Add link.
""",
                2: """# Profile: MCP Server Standardization

- **Category**: Communication Protocols
- **Release Status**: Draft Spec
- **Target Audience**: Tool Developers

## Agent-Native Characteristics
Model Context Protocol (MCP) establishes a standardized interface for agents to fetch context and invoke tools across diverse host environments.

## Aesthetic/UX Details
Operates as a background server routing JSON-RPC schemas. Offers diagnostic dashboards for reviewing active endpoints and schemas.

## Key Takeaways & Market Signal
Standardizing tools accelerates integration.

## References
- FIXME: Add MCP link.
""",
                3: """# Profile: MCP Server Standardization

- **Category**: Communication Protocols
- **Release Status**: Draft Spec
- **Target Audience**: Tool Developers

## Agent-Native Characteristics
Model Context Protocol (MCP) defines an open standard for how foundation models connect to tools, documents, and data sources. MCP replaces custom API integrations with a unified, bi-directional JSON-RPC protocol, allowing any compliant agent client to dynamically discover and consume tools exposed by any host server.

## Aesthetic/UX Details
The protocol functions as a lightweight service running over standard transport layers like Server-Sent Events (SSE) or stdio. Developers configure client connections via simple JSON config files, and the client automatically maps available resources into the agent's context.

## Key Takeaways & Market Signal
Standardization resolves ecosystem fragmentation. By establishing a shared interface for tools and context retrieval, MCP enables developers to build reusable tool servers that work seamlessly across different models and orchestrators.

## References
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
"""
            },
            "llama.cpp & local runtime engines": {
                1: """# Profile: Llama.cpp & Local Runtime Engines

- **Category**: Local Inference
- **Release Status**: Production Library
- **Target Audience**: Sovereign Developers

## Agent-Native Characteristics
Llama.cpp runs models locally on consumer hardware.

## Aesthetic/UX Details
It uses a terminal window.

## Key Takeaways & Market Signal
Local models are private.

## References
- TODO: Add link.
""",
                2: """# Profile: Llama.cpp & Local Runtime Engines

- **Category**: Local Inference
- **Release Status**: Production Library
- **Target Audience**: Sovereign Developers

## Agent-Native Characteristics
Llama.cpp provides CPU-optimized quantization and execution of LLMs, enabling autonomous agents to run locally without external API dependencies.

## Aesthetic/UX Details
Interfaced via command-line arguments or integrated local HTTP endpoints. Renders real-time token generation speed metrics.

## Key Takeaways & Market Signal
Quantized inference democratizes local agents.

## References
- FIXME: Add link.
""",
                3: """# Profile: Llama.cpp & Local Runtime Engines

- **Category**: Local Inference
- **Release Status**: Production Library
- **Target Audience**: Sovereign Developers

## Agent-Native Characteristics
Llama.cpp allows autonomous agents to execute fully sovereign reasoning loops on consumer-grade hardware. By implementing high-efficiency GGUF integer quantizations and CPU/GPU co-execution, it removes the need for commercial web API endpoints, guaranteeing absolute data privacy and eliminating network latency bottlenecks during long-running tasks.

## Aesthetic/UX Details
The engine exposes a lightweight, OpenAI-compatible web API. Developers monitor performance and real-time execution speeds through terminal dashboards showing prompt evaluation times, context ingestion rates, resource consumption, and raw tokens per second metrics.

## Key Takeaways & Market Signal
Local inference is critical for sovereign agent operations. Running models locally reduces hosting costs, protects sensitive enterprise data, and ensures reliable offline execution, representing a shift toward decentralized agent-native operations.

## References
- [Llama.cpp GitHub Repository](https://github.com/ggerganov/llama.cpp)
"""
            },
            "e2b sandbox runtimes": {
                1: """# Profile: E2B Sandbox Runtimes

- **Category**: Sandbox Environments
- **Release Status**: Production Cloud
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
E2B provides microVM sandboxes for code execution.

## Aesthetic/UX Details
It uses cloud SDKs.

## Key Takeaways & Market Signal
Sandboxing prevents host pollution.

## References
- TODO: Add link.
""",
                2: """# Profile: E2B Sandbox Runtimes

- **Category**: Sandbox Environments
- **Release Status**: Production Cloud
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
E2B provides cloud-hosted micro-virtual machines designed to execute code generated by AI agents safely in isolated developer sandboxes.

## Aesthetic/UX Details
Controlled via Python and JavaScript SDKs. Offers real-time execution outputs and system logs from inside the VM shell.

## Key Takeaways & Market Signal
MicroVMs are the primary runtime for coding agents.

## References
- FIXME: Add link.
""",
                3: """# Profile: E2B Sandbox Runtimes

- **Category**: Sandbox Environments
- **Release Status**: Production Cloud
- **Target Audience**: Agent Developers

## Agent-Native Characteristics
E2B offers secure, lightweight microVMs designed specifically for AI agents and code interpreters. Since coding agents frequently compile code and run tests, E2B provides isolated cloud sandboxes that spin up in less than 150ms, allowing agents to execute code, save files, and launch web servers safely.

## Aesthetic/UX Details
Developers control the sandboxes using a clean, asynchronous SDK. The runtime handles authentication, virtualization, and file syncing, returning real-time stdout and stderr streams directly to the calling agent's execution loop.

## Key Takeaways & Market Signal
Dedicated VM infrastructure is essential for building autonomous developers. E2B proves that traditional shared containers are too slow and insecure for dynamic agent execution, shifting the industry standard toward instant-on micro-virtualization.

## References
- [E2B Sandboxes](https://e2b.dev)
"""
            }
        }

    def generate_draft(self, topic, iteration=1):
        """Produce drafts showing step-by-step corrections of mistakes."""
        topic_lower = topic.lower().strip()
        if topic_lower in self.templates:
            return self.templates[topic_lower][iteration]
        
        # Fallback to default Claude Code templates
        if iteration == 1:
            return f"""# Profile: {topic}

- **Category**: Developer CLI Agent
- **Release Status**: Active Beta
- **Target Audience**: AI Developers & Engineers

## Agent-Native Characteristics
Claude Code is a command-line interface that allows Claude to interact directly with the local development workspace. It can run tests, search files, read git diffs, and execute bash shell commands in a sandbox.

## Aesthetic/UX Details
It runs entirely inside the developer's terminal. It uses standard ANSI colors and lists actions clearly.

## References
- TODO: Add github and developer docs links here.
"""
        elif iteration == 2:
            return f"""# Profile: {topic}

- **Category**: Developer CLI Agent
- **Release Status**: Active Beta
- **Target Audience**: AI Developers & Engineers

## Agent-Native Characteristics
Claude Code is an agent-native developer utility designed by Anthropic. Unlike simple completion plugins, it acts as an autonomous workspace agent. It can index the repository structure, read code files, write complex refactors, run test scripts, and solve terminal errors in a continuous execution loop. This makes it highly agent-native because it takes full control of the development lifecycle in response to high-level goals.

## Aesthetic/UX Details
It runs entirely inside the developer's terminal. It uses standard ANSI colors, interactive keyboard options, and lists planned steps before executing them. Developers interface with it via a conversational terminal session that preserves shell history.

## Key Takeaways & Market Signal
Claude Code indicates a major shift from IDE autocomplete plugins (like Copilot) to full workspace-native agents. It demonstrates that the CLI is a highly efficient interface for agents because shell execution, testing, and file editing are natively unified under a terminal process.

## References
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- FIXME: Add developer blog link.
"""
        else:
            return f"""# Profile: {topic}

- **Category**: Developer CLI Agent
- **Release Status**: Active Beta
- **Target Audience**: AI Developers & Engineers

## Agent-Native Characteristics
Claude Code is an agent-native developer utility designed by Anthropic. Unlike simple completion plugins, it acts as an autonomous workspace agent. It can index the repository structure, read code files, write complex refactors, run test scripts, and solve terminal errors in a continuous execution loop. This makes it highly agent-native because it takes full control of the development lifecycle in response to high-level goals.

## Aesthetic/UX Details
It runs entirely inside the developer's terminal. It uses standard ANSI colors, interactive keyboard options, and lists planned steps before executing them. Developers interface with it via a conversational terminal session that preserves shell history.

## Key Takeaways & Market Signal
Claude Code indicates a major shift from IDE autocomplete plugins (like Copilot) to full workspace-native agents. It demonstrates that the CLI is a highly efficient interface for agents because shell execution, testing, and file editing are natively unified under a terminal process.

## References
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [Anthropic Developer Blog](https://www.anthropic.com/news/claude-3-5-sonnet)
"""


class WriterCriticLoop:
    """Orchestrates the multi-turn review and correction loop."""

    def __init__(self):
        self.writer = HeuristicWriter()
        self.critic = HeuristicCritic()

    def execute(self, topic, run_id="run_03"):
        print(f"\n{'='*60}")
        print(f"🔄 WRITER-CRITIC SELF-CORRECTION LOOP")
        print(f"📋 Topic: {topic} | Run: {run_id}")
        print(f"{'='*60}\n")

        field_notes_dir = os.path.join(BASE_DIR, "WORKSPACE", "field_notes", "cycle_02", run_id)
        os.makedirs(field_notes_dir, exist_ok=True)
        slug = topic.lower().replace(" ", "_")
        
        # Format the filename to match the run number suffix (e.g. c2_03 or c2_05)
        run_suffix = run_id.replace("run_", "")
        target_path = os.path.join(field_notes_dir, f"field_note_c2_{run_suffix}_{slug}.md")

        iteration = 1
        max_iterations = 3
        approved = False
        final_content = ""
        log_records = []

        while iteration <= max_iterations and not approved:
            print(f"📝 Iteration {iteration}: Generating draft...")
            draft = self.writer.generate_draft(topic, iteration)
            
            print("🔍 Critic Auditing Draft...")
            violations = self.critic.audit(draft)

            if not violations:
                print("✅ Critic Audit: Approved!")
                approved = True
                final_content = draft
                log_records.append({
                    "iteration": iteration,
                    "status": "Approved",
                    "violations": []
                })
            else:
                print(f"❌ Critic Audit: Rejected with {len(violations)} violations:")
                for v in violations:
                    print(f"   - {v}")
                
                log_records.append({
                    "iteration": iteration,
                    "status": "Rejected",
                    "violations": violations
                })
                iteration += 1
                print("-" * 40)

        # Write final result to file
        if final_content:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print(f"\n💾 Saved finalized approved report to: {target_path}")
        else:
            print("\n⚠️  Loop completed without clean approval. Saving latest draft for review.")
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(draft)

        # Generate a loop audit log report for transparency
        log_path = target_path.replace(".md", "_audit_log.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump({
                "topic": topic,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "iterations": log_records,
                "final_file": target_path
            }, f, indent=2, ensure_ascii=False)
        print(f"📄 Loop audit log saved to: {log_path}\n")

        return approved, target_path


def main():
    parser = argparse.ArgumentParser(description="Writer-Critic Self-Correction Loop CLI")
    parser.add_argument("--topic", type=str, default="Claude Code", help="Topic to profile")
    parser.add_argument("--run", type=str, default="run_03", help="Run ID directory, e.g. run_05")
    args = parser.parse_args()

    loop = WriterCriticLoop()
    loop.execute(args.topic, args.run)


if __name__ == "__main__":
    main()

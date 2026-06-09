# LangGraph by LangChain
> Ingested on: 2026-06-08 00:20:16
> Category: field_notes
> Index: 004

# Profile
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
- **Reference**: https://langchain.com/langgraph
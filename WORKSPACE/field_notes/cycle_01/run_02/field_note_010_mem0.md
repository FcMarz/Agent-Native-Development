# Mem0: Modular Intelligent Memory Layer
> Ingested on: 2026-06-08 00:31:06
> Category: field_notes
> Index: 010
> Phase: 01 | Run: 02

# Profile
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
- **Reference**: https://github.com/mem0ai/mem0
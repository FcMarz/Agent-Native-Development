# Profile: Letta (MemGPT) State Management

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

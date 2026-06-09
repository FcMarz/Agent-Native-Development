# Profile: Langfuse & Langsmith Micro-Trace Telemetry

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

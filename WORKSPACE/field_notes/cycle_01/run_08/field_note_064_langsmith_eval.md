# LangSmith: Agent Trajectory and Trace Evaluator
> Ingested on: 2026-06-08 01:41:22
> Category: field_notes
> Index: 064
> Phase: 01 | Run: 08

# Profile
- **Name**: LangSmith
- **Category**: Agent Trace Evaluation & Telemetry
- **Status**: Production-ready developer portal by LangChain

# Agent-Native Characteristics
- **Trace Evaluation**: Evaluates complete agent trajectories (sequence of steps, tool calls, and LLM responses).
- **Run Assertions**: Programmatically tests if the correct tools were invoked with the correct inputs.
- **Feedback Loops**: Collects user feedback scores and maps them back to trace records.

# Aesthetic/UX Details
- Visual trace execution tree; side-by-side prompt debugger.

# Key Takeaways & Market Signal
- **Signal**: Debugging agents requires tracing trajectories. Knowing what tool was called and why it failed is key to refining complex agent orchestrators.
- **Reference**: https://www.langchain.com/langsmith
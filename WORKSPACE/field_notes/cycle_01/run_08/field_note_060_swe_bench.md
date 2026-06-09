# SWE-bench: Benchmark for Codebase Resolution Agents
> Ingested on: 2026-06-08 01:41:22
> Category: field_notes
> Index: 060
> Phase: 01 | Run: 08

# Profile
- **Name**: SWE-bench
- **Category**: Coding Agent Benchmark
- **Status**: Standard evaluation platform for SWE agent research

# Agent-Native Characteristics
- **Real GitHub Issue Resolution**: Evaluates agent capabilities by tasking them to resolve real issues pulled from Python codebases.
- **Test-Suite Verification**: Measures task success by executing unit tests before and after agent edits.
- **Multi-File Context Complexity**: Challenges agents to find, read, and edit multiple related files.

# Aesthetic/UX Details
- Quantitative scoreboard ranking top open-source and commercial agents (SWE-agent, OpenHands, Devin).

# Key Takeaways & Market Signal
- **Signal**: The gold standard for code agents is verified execution. Success is measured by running test suites, not just code generation metrics (like BLEU/ROUGE).
- **Reference**: https://www.swebench.com
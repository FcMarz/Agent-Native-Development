# SWE-agent: Software Engineering Agent CLI
> Ingested on: 2026-06-08 01:00:17
> Category: field_notes
> Index: 025
> Phase: 01 | Run: 04

# Profile
- **Name**: SWE-agent
- **Category**: Autonomous Software Engineering Agent
- **Status**: Open-source, built by Princeton NLP Group

# Agent-Native Characteristics
- **Agent-Computer Interface (ACI)**: Uses a simplified shell-like environment specifically optimized for LLMs (offering paginated viewing, exact regex search, and targeted editing).
- **GitHub Issue Solver**: Resolves real repository bugs by checking out code, locating issues, testing changes, and submitting pull requests autonomously.
- **High Benchmark Performance**: Achieves top scores on SWE-bench (software engineering benchmark evaluation).

# Aesthetic/UX Details
- Controlled via terminal interface; logs step-by-step reasoning traces showing exact shell commands executed and target source diffs.

# Key Takeaways & Market Signal
- **Signal**: Standard human bash consoles are inefficient for LLMs. Designing bespoke Agent-Computer Interfaces (ACIs) is required to prevent agents from getting lost in large terminal outputs.
- **Reference**: https://github.com/princeton-nlp/SWE-agent
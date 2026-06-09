# Garak: LLM Vulnerability and Security Scanner
> Ingested on: 2026-06-08 01:41:22
> Category: field_notes
> Index: 061
> Phase: 01 | Run: 08

# Profile
- **Name**: Garak
- **Category**: Security and Red-Teaming Scanner
- **Status**: Open-source CLI vulnerability checker

# Agent-Native Characteristics
- **Prompt Injection Scanners**: Simulates adversarial inputs to detect jailbreaks, credential leaks, and data extraction.
- **Output Safety Auditing**: Detects toxic generation, hallucination triggers, and insecure code outputs.
- **Targeted Probing**: Automatically generates thousands of security test payloads against agent runtime API endpoints.

# Aesthetic/UX Details
- Simple CLI tool showing test progression logs and a structured vulnerability coverage report.

# Key Takeaways & Market Signal
- **Signal**: LLM APIs require automated vulnerability scanning. Garak acts as the OWASP-Zap for the LLM era, checking if agents leak system prompts or credentials.
- **Reference**: https://github.com/leondz/garak
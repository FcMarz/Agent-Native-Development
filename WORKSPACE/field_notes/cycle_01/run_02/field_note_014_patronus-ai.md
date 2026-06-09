# Patronus AI: Real-Time Hallucination Guardrails
> Ingested on: 2026-06-08 00:31:06
> Category: field_notes
> Index: 014
> Phase: 01 | Run: 02

# Profile
- **Name**: Patronus AI
- **Category**: AI Reliability & Evaluation Platform
- **Founders**: Anand Kannappan & Rebecca Qian (former Meta AI researchers)
- **Status**: Venture backed ($17M Series A in 2024, scaling in 2025/2026)

# Agent-Native Characteristics
- **Lynx Evaluator**: A proprietary, open-source model optimized specifically for detecting hallucinations in RAG outputs.
- **Patronus Protect**: An on-device or API-based guardrail engine that blocks non-compliant or inaccurate agent output.
- **Automated Red Teaming**: Generates adversarial test sets to stress-test agent boundaries at scale.

# Aesthetic/UX Details
- Provides test-suite dashboards showing model accuracy, compliance scoring, and regression tracking.

# Key Takeaways & Market Signal
- **Signal**: Evaluators must be LLMs themselves. Traditional keyword checks are useless for monitoring agent reasoning. Specialized evaluator models (like Lynx) are required to assure corporate compliance.
- **Reference**: https://www.patronus.ai
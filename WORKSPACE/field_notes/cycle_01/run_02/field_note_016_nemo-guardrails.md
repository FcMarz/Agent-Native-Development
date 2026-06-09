# NVIDIA NeMo Guardrails: Programmable LLM Control Flow
> Ingested on: 2026-06-08 00:31:06
> Category: field_notes
> Index: 016
> Phase: 01 | Run: 02

# Profile
- **Name**: NeMo Guardrails
- **Category**: Open-Source Semantic Guardrail Library
- **Creator**: NVIDIA
- **Status**: Open-source toolkit, highly adopted in enterprise pipelines

# Agent-Native Characteristics
- **Colang Syntax**: Uses a custom declarative language (Colang) to define specific dialogue paths, policies, and behavior limits.
- **Semantic Moderation**: Verifies the semantic topic of the prompt, steering the LLM back to the targeted domain if it starts drifting.
- **In-Memory Guardrails**: Runs alongside the model inside inference engines, adding negligible latency to the generation loop.

# Aesthetic/UX Details
- Highly code-centric, designed for integration into Python pipelines and NVIDIA Triton inference servers.

# Key Takeaways & Market Signal
- **Signal**: Programmable guardrails are necessary to bridge the gap between deterministic software rules and fuzzy LLM reasoning. Colang-style flow control keeps agents within compliance.
- **Reference**: https://github.com/NVIDIA/NeMo-Guardrails
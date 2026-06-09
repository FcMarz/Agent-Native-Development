# Swarm (OpenAI): Educational Agent Handoff Framework
> Ingested on: 2026-06-08 01:29:02
> Category: field_notes
> Index: 055
> Phase: 01 | Run: 07

# Profile
- **Name**: Swarm
- **Category**: Lightweight Swarm Framework
- **Status**: Experimental release by OpenAI Solutions team

# Agent-Native Characteristics
- **Routine and Handoff Pattern**: Standardizes handoffs where one agent hands execution back to the orchestrator to route to another.
- **Minimalist Design**: Avoids complex class setups; relies on basic python functions and direct LLM calls.
- **Context Variables**: Dynamically updates shared variables across handoff nodes.

# Aesthetic/UX Details
- Simple CLI chat loop displaying which agent is active at any given step.

# Key Takeaways & Market Signal
- **Signal**: Handoffs should be simple. The core agent architecture is consolidating around returning specialized agent sub-functions rather than heavy monolithic orchestrators.
- **Reference**: https://github.com/openai/swarm
# DSPy: Programming (Not Prompting) Foundation Models
> Ingested on: 2026-06-08 01:00:17
> Category: field_notes
> Index: 032
> Phase: 01 | Run: 04

# Profile
- **Name**: DSPy
- **Category**: Programmatic Prompt Compilation and Optimization
- **Status**: Stanford NLP, highly popular developer framework for structured LLM execution

# Agent-Native Characteristics
- **Declarative Modules**: Replaces hardcoded string prompts with reusable, typed code structures (e.g. `dspy.Predict`, `dspy.ChainOfThought`).
- **Prompt Compilers**: Automatically optimizes prompt instructions and few-shot examples based on small validation datasets.
- **Model Agnostic**: Compiles and compiles optimized outputs across different models (e.g. compiling prompts for local SLMs using outputs from GPT-4).

# Aesthetic/UX Details
- Pure code framework; console logging details the step-by-step compilation, evaluation iterations, and final optimized prompts.

# Key Takeaways & Market Signal
- **Signal**: Prompt engineering is dead. Programmatic compilation that optimizes prompts based on validation datasets is the only scalable way to manage agents across model updates.
- **Reference**: https://github.com/stanfordnlp/dspy
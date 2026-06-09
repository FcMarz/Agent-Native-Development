# Profile: Promptfoo & Braintrust Assertions

- **Category**: Agent Evaluation
- **Release Status**: Developer Tooling
- **Target Audience**: QA Engineers

## Agent-Native Characteristics
Promptfoo and Braintrust automate prompt and agent evaluation. They enable developers to define test suites with assertions covering LLM outputs, including classification, regex checks, semantic similarity, and model-graded criteria. This is agent-native because it uses LLM-as-a-judge patterns to evaluate non-deterministic agent behavior and enforce safety guardrails before deploying changes to production systems.

## Aesthetic/UX Details
The tools render a detailed evaluation matrix in the terminal and on a web dashboard. The interface shows side-by-side comparisons of different prompts, model outputs, cost metrics, and execution times. Failures are highlighted in red with explanation tooltips, allowing developers to inspect which assertions failed and tweak system prompts.

## Key Takeaways & Market Signal
Testing prompts requires software engineering rigor. Automated assertions and model-graded evaluations are replacing manual inspection, enabling continuous integration pipelines for AI applications. This shift represents a transition toward deterministic quality assurance and safety auditing for non-deterministic agent behaviors.

## References
- [Promptfoo Repository](https://github.com/promptfoo/promptfoo)
- [Braintrust Platform](https://www.braintrust.dev)

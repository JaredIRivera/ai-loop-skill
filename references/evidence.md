# AI Loop Skill: research context

The installed skill names several workflow guides and research directions. The primary sources below provide useful context for its design choices. They do not evaluate this repository or establish performance for a different model, task, or implementation.

| Source | Relevant point | Boundary |
|---|---|---|
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Describes evaluator-optimizer workflows and recommends clear criteria and measurable value from iteration | Architecture guidance does not supply an acceptance result for this package |
| [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | Studies repeated generation, feedback, and refinement without changing model weights | Its findings depend on the tasks, models, and evaluation design in the paper |
| [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) | Examines reasoning self-correction without external feedback and reports important limitations | It is evidence about the studied conditions, not a blanket claim about every present-day loop |

These sources were consulted while preparing the repository documentation on October 28, 2026. The full installed source's broader attributions are retained; this short list is not a comprehensive audit of each historical attribution.

The practical design recommendation is to choose validation appropriate to the task, define stopping conditions, and compare the resulting workflow against a strong baseline. Use [the benchmark protocol](benchmark-protocol.md) to establish evidence for the intended application.

# AI Loop Skill: release notes

Technical terms are defined in [the glossary](references/glossary.md).

## 1.0.0: portable repository package

Package the installed AI Loop Skill with a practical setup path, complete examples, a design brief, and inspectable local checks.

- Preserves the source's architecture selection, design procedure, prompt template, evaluator example, domain playbooks, anti-patterns, and evaluation guidance.
- Removes the installed file's stale vault-navigation link.
- Labels the core example as pseudocode, adds explicit initialization and positive iteration validation, and makes escalation a terminal path before success.
- Adds README, specification, glossary, research links, source provenance, and a benchmark protocol.
- Adds standard-library checks for package integrity and nine synthetic loop-control cases.
- Preserves `license: MIT` metadata without inventing a copyright notice or repository-wide license grant.

The [recorded local checks](references/preflight-2026-10-28.md) cover packaging and the documented example. No model comparison or production deployment is claimed. Original installed and vault files were not changed.

## Before a production release

- [ ] Confirm installation and discovery in the intended assistant.
- [ ] Define real inputs, permissions, data retention, expected failures, and acceptance criteria.
- [ ] Implement and test runtime timeouts, tool budgets, spending limits, approvals, and error handling.
- [ ] Compare a strong single-response baseline with the loop on representative and held-out cases.
- [ ] Record exact instructions, model settings, dates, repetitions, all calls, failures, time, and cost.
- [ ] Review evaluator disagreement, false passes, unsupported claims, and changes to original requirements.
- [ ] Resolve the complete license text and copyright attribution before broader redistribution.

Keep historical results and scoring rules intact. Add a focused regression case when a real failure is confirmed.

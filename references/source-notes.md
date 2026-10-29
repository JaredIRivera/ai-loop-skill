# AI Loop Skill: source notes

## Selected source

The package uses the installed `ai-loop-skill/SKILL.md` as its primary source. The installed folder contains that file only, with no required support files, scripts, or runtime dependencies.

| Source | SHA-256 of inspected bytes |
|---|---|
| Installed `ai-loop-skill/SKILL.md` | `442489db3ba6512854cc1ed27aa2e2fcb4cc50d5fb58a99d8252243a3bf8c669` |
| Vault candidate `skills/ai-agent-loop.md` | `3622ad325d7ae7d14dd8a500d43277173c6bbda2a7c3c43b83bfa753d20ca7a6` |

The vault candidate has the same workflow body. It adds vault metadata (`type`, `status`, and `dependencies`) and uses a different navigation link. No alternate workflow was substituted. Private absolute paths are omitted from this record.

## Export adaptations

The original installation and vault source remain unchanged. The repository copy makes these specific changes:

1. Removes the stale `Parent branch` wiki-link to a private navigation map.
2. Labels the Core Loop Model as illustrative pseudocode with application-defined adapters.
3. Replaces the uninitialized `while` example with a function and bounded `for` iteration. It rejects non-integer and nonpositive iteration limits.
4. Makes human escalation a terminal return before accepting success, including when a result has both a passing score and a risk flag.
5. Explicitly identifies timeouts, tool budgets, permissions, and error handling as application responsibilities beyond the example.
6. Normalizes the exported file to UTF-8 with LF line endings.

All skill content outside the navigation line and Core Loop Model remains the same after newline normalization. Added documentation, interface metadata, synthetic checks, and reference resources are repository packaging, not recovered source files. The installed metadata version remains `1.0`; release notes identify the package revision separately.

## Presentation reference

The requested `JaredIRivera/prompt-optimizer` URL returned 404 during inspection. The current matching project was resolved as [Prompt & Cache-Readiness Optimizer](https://github.com/JaredIRivera/prompt-and-cache-readiness-optimizer). Its current README, specification, release notes, supporting protocol, preflight, and interface metadata informed this package.

This repository follows the reference's root `SKILL.md`, `README.md`, `SPEC.md`, and `RELEASE_NOTES.md` layout; `agents/`, `references/`, `scripts/`, and `evals/` organization; and README heading order. Prompt-caching experiments and measurements were not copied. Local checks and a relevant comparison protocol occupy the corresponding sections.

## License metadata

The installed skill declares `license: MIT`. Its folder supplies no license text or copyright notice. The declaration is preserved as source metadata. This package does not invent an attribution or assert a separate repository-wide license grant; resolve the complete notice before broader redistribution.

## Evidence limits

The local checks inspect package structure and execute the example with synthetic adapters. They do not call a model, connect to external services, or establish effectiveness on business tasks. Research links provide context, while [the benchmark protocol](benchmark-protocol.md) defines a future model comparison.

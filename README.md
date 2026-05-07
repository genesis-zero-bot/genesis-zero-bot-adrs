# RegenTribes Architecture Decision Records

Architecture Decision Records for RegenTribes.
MADR format, ASD-STE100 writing style.

## What is this?

This repository holds the formal decision record for RegenTribes architecture choices.
Each ADR captures a significant architectural decision: what was decided, why, and what changed.

Format: [MADR 4.0.0](https://adr.github.io/madr/) (Markdown Any Decision Records).
Style: [ASD-STE100](https://en.wikipedia.org/wiki/ASD-STE100) — Simplified Technical English, max 20 words per sentence, active voice.

## ADRs

| ADR | Title | Status | Domain |
|-----|-------|--------|--------|
| [0000](./docs/0000-oad-workflow-grammar.md) | OAD Workflow Grammar over Full Integral Stack | Accepted | information |
| [0001](./docs/0001-agent-knowledge-systems-rejected.md) | Agent Knowledge Systems — Bonfires.ai and llm_wiki Rejected | Accepted | information |
| [0002](./docs/0002-ame-metonymic-activation.md) | AME Architecture — Metonymic Activation and Virtual Trust Field | Accepted | information |
| [0003](./docs/0003-integral-non-transferable-value-model.md) | Integral Non-Transferable Value Model vs Percentage-Based Paywall | Accepted | exchange |
| [0004](./docs/0004-llm-wiki-pattern-for-integral-knowledge-commons.md) | LLM Wiki Pattern for Integral Knowledge Commons (M10) | Proposed | information |
| [0005](./docs/0005-rag-agent-memory-for-integral-stack.md) | RAG and Agent Memory in the Integral Stack | Proposed | information |
| [0006](./docs/0006-data-quality-governance-layer.md) | Data Quality and Governance for Knowledge Layer | Proposed | information |
| [0007](./docs/0007-kabanov-continuous-attention-agi.md) | Kabanov Continuous Attention — AGI Model for Integral Stack | Proposed | cognition |

## How to add a new ADR

1. Copy the template below into a new file `docs/XXXX-title.md` with the next sequential number.
2. Fill in each section.
3. Run `python3 docs/adrs/build.py` to regenerate the site.
4. Commit and push.

### Template

```markdown
---
title: Title Here
number: XXXX
status: Proposed
date: YYYY-MM-DD
authors: YourName
domain: information|exchange|cognition|...
level: system|organ|...
tags:
  - tag1
  - tag2
---

## Status

Proposed

## Context

What is the issue?
Why does it need a decision?

## Decision

What was decided?
Be specific.

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Description | ✅/❌ |

## Consequences

### Positive

- ...

### Negative

- ...

### Risks

- ...

## References

- ...
```

## Build

```bash
python3 docs/adrs/build.py
```

Output goes to `docs/adrs/_site/`.
GitHub Pages serves from there.

## ADR vs Wiki — The Fight

This repo is one piece of RegenTribes knowledge management.
The other piece is the [OpenClaw wiki](./wiki-maintainer).
They serve different purposes.

### What ADRs Do Better

- **Decision traceability**: Context → Decision → Consequences, immutable once accepted.
- **Explicit options analysis**: Every ADR shows what alternatives were considered and why.
- **Status lifecycle**: Proposed → Accepted → Deprecated/Superseded. Clear state.
- **Regulatory friendliness**: Auditors and stakeholders can trace exactly why something was built.
- **Immutable records**: Once accepted, an ADR does not drift. A wiki page does.

### What the OpenClaw Wiki Does Better

- **Emergent structure**: No upfront schema. Knowledge compiles without pre-defined categories.
- **Continuous knowledge**: Not just point-in-time decisions. Ongoing research, patterns, member cards.
- **Rich relationships**: Wikilinks connect concepts across domains. ADRs are siloed by design.
- **Ambiguous topics**: A wiki can hold "we are exploring X" without forcing a binary decision.
- **Better for exploration**: Research mode works in a wiki. ADRs are for post-hoc documentation.
- **Scales to undecided knowledge**: Real organizations have as much (or more) knowledge that hasn't been decided as has been.

### The Tension

ADRs assume decisions are discrete events with clear outcomes.
Wiki knowledge is continuous and evolving.

| Scenario | Use |
|----------|-----|
| "We decided to use SurrealDB for the knowledge graph" | ADR |
| "Here's what we know about Kabanov's AGI model" | Wiki |
| "ITC non-transferable value is locked in" | ADR |
| "How AME metonymic activation works" | Wiki |
| "Reject Bonfires.ai and llm_wiki" | ADR |
| "Active inference patterns for IoT sensors" | Wiki |

Real organizations need both: decisions (ADR) and understanding (wiki).
This repo handles decisions.
The wiki handles everything else.

## License

CC0-1.0 — public domain.
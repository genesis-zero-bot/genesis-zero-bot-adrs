---
title: Data Quality and Governance for Knowledge Layer
number: 0006
status: Proposed
date: 2026-05-06
authors: Genesis
domain: information
level: system
tags:
  - data-quality
  - governance
  - knowledge-layer
  - data-stewardship
---

## Status

Proposed

## Context

ADR 0004 (LLM Wiki) and ADR 0005 (RAG and Agent Memory) establish three knowledge patterns for the Integral stack.

The article identifies a critical gap that most teams underinvest in:

> "The governance layer underneath all of them — data quality, freshness, access control — is what most teams underinvest in.
> Stale or ungoverned inputs degrade all three simultaneously."

This ADR establishes the governance requirements that apply across all three knowledge patterns.

## Decision

Implement four governance requirements across the knowledge layer.

### Requirement 1: Source Provenance

Required for all wiki pages.
Every concept page must cite at least one source page.
No synthesized claim without a backing source.
`wiki lint` enforces this.
Pages with missing `sourceIds` fail validation.

### Requirement 2: Freshness Tracking

Required for all concept pages.
Every page carries `updatedAt`.
It is checked by `wiki lint` for staleness.
Pages older than 30 days without update trigger a stale-page warning.

### Requirement 3: Contradiction Detection

Enforced by `wiki lint`.
When two concept pages make conflicting claims, `wiki lint` surfaces the contradiction.
A human must adjudicate.
The resolution gets recorded as a new claim with `status: resolved` and evidence pointing to the adjudication source.

### Requirement 4: Ingest Quality Gates

Required before wiki commit.
Before any source page is committed to the vault:

- Source must be cited in at least one concept page.
- Concept page must pass `wiki lint` with 0 errors.
- Source must have valid `provenance` frontmatter.
  Source URL or file path.

## Options Considered

| Option | Assessment |
|--------|------------|
| Trust LLM ingest quality | Rejected — errors compound in LLM Wiki.
No quality gate means bad synthesis baked permanently. |
| Manual review every ingest | Rejected — unsustainable at scale.
Creates bottleneck. |
| Automated lint + provenance + staleness checks | Adopted — `wiki lint` enforces all four requirements. |

## Consequences

### Positive

- All three knowledge patterns share the same governance foundation.
- Quality degradation caught before propagation.
- Clear audit trail: source → concept → claim → evidence.
- Wikilink integrity maintained via `wiki lint`.

### Negative

- Ingest workflow is slower.
  Requires lint plus provenance before commit.
- Contradiction adjudication requires human time.

### Risks

- If `wiki lint` is not run after every ingest, governance requirements slip.
- Staleness warnings can pile up if vault is not actively maintained.

## Implementation

These requirements are enforced by `openclaw wiki lint` in the standard workflow:

```
openclaw wiki ingest <source>
openclaw wiki compile
openclaw wiki lint  # fails if: missing sourceIds, missing provenance, stale page, contradiction
```

Wiki vault mode `isolated` means all governance is self-contained.
No external dependency.

## References

- Visrow (2026). RAG vs. Agent Memory vs. LLM Wiki. <https://medium.com/@visrow/rag-vs-agent-memory-vs-llm-wiki-a-practical-comparison-41a9a0dc4dec>
- ADR 0004 — LLM Wiki Pattern for Integral Knowledge Commons (M10)
- ADR 0005 — RAG and Agent Memory in the Integral Stack
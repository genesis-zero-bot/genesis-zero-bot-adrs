---
title: RAG and Agent Memory in the Integral Stack
number: 0005
status: Proposed
date: 2026-05-06
authors: Genesis
domain: information
level: system
tags:
  - RAG
  - agent-memory
  - integral
  - CDS
  - AME
  - user-knowledge
---

## Status

Proposed

## Context

ADR 0004 established LLM Wiki as the M10 knowledge commons layer.
This ADR addresses where the other two patterns (RAG and Agent Memory) fit into the Integral architecture.

The Integral system has three distinct knowledge problems.

**Problem 1: User knowledge**
Who is each member?
What is their FOT trajectory?
ITC ledger state?
AME interaction history?
Changes at conversation time.

**Problem 2: Domain knowledge**
OAD principles.
ITC ledger rules.
Regenerative community patterns.
AME architecture.
Changes at ingest time.

**Problem 3: Corpus knowledge**
Deliberation records.
Community proposals.
Historical decisions.
Meeting notes.
Changes frequently.
Large volume.

Each problem requires a different pattern.

## Decision

Assign RAG and Agent Memory to specific subsystems.

| Pattern | Subsystem | What it manages |
|---------|-----------|----------------|
| Agent Memory | AME + ITC ledger | Member profiles, FOT trajectories, interaction history, trust scores |
| RAG | CDS deliberation records | Historical deliberations, proposals, CDS state snapshots |
| LLM Wiki | M10 (knowledge commons) | Compiled domain synthesis, cross-referencing, regenerative patterns |

**Agent Memory is NOT used for domain knowledge.**
It knows the user.
It is blind to domain knowledge unless paired with a document layer.
In the Integral stack, this means:
Agent Memory manages member context (who am I talking to, what is their FOT state).
LLM Wiki manages domain context (what does OAD say about this).

**RAG is NOT used for domain synthesis.**
RAG re-derives from raw chunks on every query.
For compiled synthesis (OAD principles, ITC rules), use LLM Wiki.
RAG is correct for CDS deliberation records because they are high-volume, frequently updated, and require breadth-first retrieval rather than compiled synthesis.

## Options Considered

| Option | Assessment |
|--------|------------|
| Use Agent Memory for everything | Rejected — sparse/noisy. Domain and user knowledge are orthogonal. |
| Use RAG for everything | Rejected — stateless by default, re-derives synthesis on every call. |
| Use LLM Wiki for everything | Rejected — no personalization. Reads identically for every user. |
| Three-pattern assignment (adopted) | Each pattern addresses one distinct knowledge problem. |

## Consequences

### Positive

- Each pattern applied where it actually works.
- Agent Memory provides personalization without redundant domain re-synthesis.
- RAG handles large dynamic CDS corpus without polluting LLM Wiki with raw deliberation chunks.
- Clear separation: memory = who, wiki = what, RAG = evidence.

### Negative

- Three systems to maintain.
- Cross-system consistency requires governance.
  (Dealt with in ADR 0006).

### Risks

- Agent Memory needs careful extraction discipline.
  Memory is noisy.
  Only stores what was explicitly said.
- RAG over CDS deliberation records requires careful chunking to preserve deliberation context.

## References

- Visrow (2026). RAG vs. Agent Memory vs. LLM Wiki. <https://medium.com/@visrow/rag-vs-agent-memory-vs-llm-wiki-a-practical-comparison-41a9a0dc4dec>
- ADR 0004 — LLM Wiki Pattern for Integral Knowledge Commons (M10)
- ADR 0000 — OAD Workflow Grammar

---
title: LLM Wiki Pattern for Integral Knowledge Commons (M10)
number: 0004
status: Proposed
date: 2026-05-06
authors: Genesis
domain: information
level: system
tags:
  - LLM-wiki
  - knowledge-commons
  - M10
  - integral
  - karpathy
---

## Status

Proposed

## Context

The Integral system needs a knowledge commons layer (OAD M10).
It must serve as the authoritative, persistent store for all accumulated knowledge from the community regenerative development work.

This layer must support:

- Compiled synthesis across sources.
  Not just raw retrieval.
- Incremental growth as new knowledge arrives.
- Contradiction tracking as beliefs evolve.
- Offline-first P2P access via Radicle.

Two candidate approaches:

**Option 1: RAG** (Retrieval-Augmented Generation)

- Stateless by default.
- Re-derives answers from raw docs on every query.

**Option 2: LLM Wiki** (Karpathy pattern)

- Compile-once, query forever.
- LLM writes structured wiki pages that persist synthesis.

## Decision

Adopt the LLM Wiki (Karpathy pattern) as the M10 knowledge commons layer.

**Ingest:** LLM reads new source → creates/updates wiki pages (sources/ + concepts/) → updates index + log

**Query:** Search relevant pages → LLM synthesizes with citations

**Lint:** Check for contradictions, broken links, stale content after each ingest

Three layers:

1. Raw sources (immutable) → sources/ in wiki vault
2. Wiki (LLM-compiled synthesis) → concepts/ in wiki vault
3. Schema + claims (structured metadata) → frontmatter + claims + evidence

## Options Considered

| Option | Approach | Status |
|--------|----------|--------|
| RAG only | Vector store + chunk retrieval | Rejected — stateless by default, no synthesis |
| Pure document store | Git + raw markdown | Rejected — no compiled synthesis |
| LLM Wiki | Karpathy pattern | Adopted |
| Hybrid RAG + LLM Wiki | RAG for retrieval, wiki for synthesis | Deferred |

## Consequences

### Positive

- Synthesis compiled once, queried indefinitely.
- Contradictions tracked via `wiki lint`.
- Offline-first via Radicle P2P.
- Obsidian-compatible for human navigation.
- Prevents redundant re-synthesis on every query.

### Negative

- Error compounding if ingest quality is poor.
- Requires discipline: source pages must back every concept page.
- Still needs a separate RAG layer for large dynamic corpora (deferred).

### Risks

- LLM interpretative errors baked into knowledge base.
- Continuous knowledge engineering burden (keeping pages consistent).
- Wiki has no awareness of who is reading or why.
  No personalization layer.
  Use Agent Memory for that.

## Analysis

### Why LLM Wiki over RAG for M10

**RAG is stateless by design.**
Every query re-derives from raw chunks.
For the Integral knowledge commons, this means the same synthesis work gets re-done on every query.
Connecting ITC ledger principles to OAD workflow grammar to regenerative community patterns.
Wasteful and slow.

**LLM Wiki compiles once.**
When a new source is ingested (e.g., a new regenerative community case study), the LLM reads it, extracts key claims, updates existing pages, creates cross-references.
Future queries draw on pre-compiled synthesis.

**The compounding effect.**
A wiki that has ingested 50 sources on regenerative development answers with greater depth than RAG over the same 50 sources.
Because relationships, contradictions, and synthesis are already compiled.

**Critically for Integral:**
The FOT (Field of Trust), ITC ledger principles, AME architecture — these are complex, cross-referencing concepts.
They benefit enormously from pre-compiled synthesis.
A query about "how does ITC non-transferable value relate to OAD workflow grammar" should hit compiled pages.
Not re-synthesize from raw specs on every call.

### Where RAG Still Applies

RAG is correct for:

- Long-tail retrieval over large corpora (e.g., scanning all historical deliberation records).
- Frequently changing documents (e.g., community proposals that update daily).
- Scenarios where freshness matters more than synthesis depth.

**Deferred:** Add a RAG layer on top of the wiki for retrieval over large, frequently-changing corpora.
Not Phase 1.

### Key Risk: Error Compounding

LLM Wiki bakes the LLM interpretation into the knowledge base.
If an ingest pass misreads the Integral specification, that error propagates into every answer drawn from that page.
Unlike RAG, which re-reads the original source on every query, LLM Wiki errors compound.

**Mitigation:** All source pages are immutable.
Concept pages can be updated and linted.
`wiki lint` surfaces contradictions.
No concept page becomes authoritative without a source page backing it.

## References

- Karpathy, A. (2026). LLM Wiki. <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- Visrow (2026). RAG vs. Agent Memory vs. LLM Wiki. <https://medium.com/@visrow/rag-vs-agent-memory-vs-llm-wiki-a-practical-comparison-41a9a0dc4dec>
- ADR 0000 — OAD Workflow Grammar (M10 context)
- ADR 0002 — AME Metonymic Activation (trust field architecture)

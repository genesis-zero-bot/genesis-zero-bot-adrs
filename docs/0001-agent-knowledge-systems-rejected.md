---
title: Agent Knowledge Systems — Bonfires.ai and llm_wiki Rejected
number: 0001
status: Accepted
date: 2026-05-06
authors: Genesis
domain: information
level: system
tags:
  - knowledge-base
  - wiki
  - bonfires
  - llm-wiki
  - architecture
  - tradeoff
---

## Status

Accepted

## Context

Two knowledge system tools were evaluated as LLM wiki solutions for agent-resident knowledge management.

**Bonfires.ai** is a hosted knowledge coordination platform.
It transforms conversations (Telegram, Discord, forums) and documents into AI-accessible knowledge graphs.
It provides real-time ingestion, knowledge graph visualization, and agent hooks.

**llm_wiki** (github.com/nashsu/llm_wiki) is a desktop application.
It implements Karpathy LLM Wiki pattern.
It builds persistent wiki from documents using:

- graph relevance
- vector search (LanceDB)
- Louvain community detection
- Deep Research

It runs as an Electron desktop app.

Requirement: P2P/offline-resilient operation for total internet blackout scenario.
Future migration path: embedded database plus reasoning system (SurrealDB, Hyperon).

## Decision

Reject both Bonfires.ai and llm_wiki.
Adopt OpenClaw bundled `memory-wiki` plugin as Phase 1 solution.
Add Syncthing for P2P sync.

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Bonfires.ai (hosted) | ❌ Rejected — subscription cost, no offline P2P mode |
| **B** | llm_wiki (desktop app) | ❌ Rejected — not agent-integratable, desktop-only |
| **C** | memory-wiki plugin (OpenClaw bundled) | ✅ Adopt — agent-native, configurable, Obsidian-compatible |
| **D** | Custom built on SurrealDB | ⚠️ Phase 3 — requires more development |

## Consequences

### Positive

- Agent-resident knowledge query without external dependency.
- Provenance-rich wiki with structured claims (not prose-only).
- P2P sync via Syncthing for offline resilience.
- Obsidian-compatible vault for human editing.
- Migration path preserved: Markdown → SurrealDB → Hyperon.

### Negative

- memory-wiki vault is Markdown files.
  Slower to query than embedded vector DB.
- Syncthing requires manual setup on each node.
- No native Louvain community detection (llm_wiki feature not ported).

### Risks

- Markdown vault grows large without compaction.
- Syncthing conflicts may arise with concurrent edits on both nodes.
- Phase 2 migration (SurrealDB) requires schema design work.

## Analysis

### Bonfires.ai — Why Rejected

Failure mode 1: **Subscription barrier**
Monthly cost is incompatible with budget-constrained community operation.

Failure mode 2: **No offline P2P mode**
Bonfires.ai is server-hosted.
It assumes live internet.
During total blackout, it goes completely dark.

Failure mode 3: **Proprietary knowledge graph**
Ingested knowledge stays in Bonfires infrastructure.
It cannot be replicated or exported for P2P sync across nodes.

Failure mode 4: **Integration gap**
Bonfires.ai overlaps with `genesis-brain` (SurrealDB semantic graph).
Adopting Bonfires.ai would create duplicate infrastructure.

### llm_wiki — Why Rejected

Failure mode 1: **Desktop-only architecture**
Electron app.
No server mode.
No headless operation.
No API.
Cannot be wired to an agent.

Failure mode 2: **Requires manual app running**
The app must be open and running to serve wiki queries.
It goes dark when the app is closed.

Failure mode 3: **No P2P sync mechanism**
Single-user desktop app.
No sync.
No collaboration.
No mesh resilience.

Failure mode 4: **Right idea, wrong implementation for agents**
The underlying methodology is excellent:

- Incremental wiki
- Two-step ingest
- Wikilinks
- Source traceability

The implementation is not designed for agent integration.

### memory-wiki — Why Adopted

OpenClaw bundled `memory-wiki` plugin:

- Agent-native: exposed as `wiki_search`, `wiki_get`, `wiki_apply`, `wiki_lint` tools
- Bridge mode: imports from active memory plugin (QMD, etc.)
- `isolated` mode: owns its own vault, no external dependency
- Obsidian-compatible rendering
- Structured claims with provenance, confidence, evidence metadata
- Dashboard reports: contradictions, low-confidence, stale pages
- Compiled digests for agent consumption (`agent-digest.json`, `claims.jsonl`)

### P2P Sync — Syncthing

For internet blackout resilience, pair `memory-wiki` with Syncthing:

```
Node A (Hetzner VPS)              Node B (HP EliteBook / laptop)
~/.openclaw/wiki/main/    ←sync→   ~/.openclaw/wiki/main/
```

- Zero internet dependency for wiki access
- Automatic conflict resolution
- Runs on same machine as OpenClaw

### Future Migration Path

| Phase | Wiki Backend | Sync |
|-------|-------------|------|
| **Phase 1** | memory-wiki (Markdown vault) | Syncthing |
| **Phase 2** | SurrealDB (same graph schema, vector embeddings) | Syncthing + Radicle |
| **Phase 3** | SurrealDB + Hyperon/MeTTa reasoning layer | Mesh sync |

Structured claims with `sourceId`, `canonicalId`, `entityType` frontmatter are the bridge.
These fields map directly to SurrealDB graph nodes.

## References

- Bonfires.ai: bonfires.ai
- llm_wiki: github.com/nashsu/llm_wiki (Karpathy LLM Wiki pattern)
- OpenClaw memory-wiki: docs.openclaw.ai/plugins/memory-wiki
- Syncthing: syncthing.net — serverless P2P file sync
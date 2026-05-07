---
id: adr.0010
pageType: adr
title: "Global Manufacturing Capacity as Regenerative Community Strategic Reference"
status: Accepted
date: "2026-05-07"
authors: Genesis
domain: engineering
level: system
confidence: 0.9
updatedAt: "2026-05-07"
tags:
  - industrial-capacity
  - manufacturing
  - reference
  - bootstrap
  - regenerative-communities
sourceIds:
  - source.0010-global-manufacturing-capacity-report
relatedConcepts:
  - concept:bootstrap
  - concept:regen-tech
  - concept:industrial-capacity
---

# ADR 0010 — Global Manufacturing Capacity as Regenerative Community Strategic Reference

## Status
Accepted

## Context

Vitali Vorski shared the Global Manufacturing Capacity Report via Telegram using Haiku 4.5 on 2026-05-07. The document is a ~2,600-line technical reference cataloging all major industrial processes required to rebuild civilization-scale manufacturing from first principles. It covers 15 sectors, ~$12.3T/yr output, 1.2B workforce, 220 EJ energy, and 90B tonnes raw material annually.

This document represents a foundational knowledge resource for RegenTribes members engaged in regenerative neighbourhood design and community-scale infrastructure planning. Without a structured reference, community members risk planning infrastructure without visibility into industrial dependencies, resource budgets, and supply chain structure.

## Decisions

### D1: Adopt the Global Manufacturing Capacity Report as canonical reference

RegenTribes adopts the Global Manufacturing Capacity Report as the canonical engineering reference for industrial bootstrap planning. This document supersedes any informal or less-complete references previously used for sizing community-scale manufacturing capability.

### D2: Create wiki entries for navigational accessibility

Genesis must create the following wiki entries to make this reference searchable and navigable within the community knowledge graph:

- **Source entry** at `sources/0010-global-manufacturing-capacity-report.md` — full document metadata, section structure, and overview
- **Concept entry** at `concepts/0010-global-manufacturing-capacity-report.md` — key claims, scope summary, and relevance to regenerative communities

Both entries must link to each other and carry the appropriate tags.

### D3: Mark this document as a living reference

The Global Manufacturing Capacity Report is designated a living reference. When:

- Community members identify updates or corrections, they will trigger a new wiki entry version
- The document owner or original source publishes a revised version, Genesis will create an updated source entry and mark the previous entry as superseded
- Community members reference this document in their own project plans, they will cite it using the wiki source ID

## Consequences

**Positive:**

- Community members now have a citable, navigable reference for industrial capacity questions
- Bootstrap planning for regenerative communities gains a first-principles engineering foundation
- Supply chain dependencies and cross-sectoral requirements become visible and queryable
- Technical planning discussions can reference specific sections and claims via wiki links

**Negative:**

- The document is large and dense; community members may need guidance to navigate it effectively
- Future updates must be tracked to prevent stale references from misleading planning decisions

**Neutral:**

- The document does not cover social, governance, or ecological dimensions of regenerative community design — it is a necessary but insufficient reference for full community planning

## References

- [[sources/0010-global-manufacturing-capacity-report|Source — Global Manufacturing Capacity Report]]
- [[concepts/0010-global-manufacturing-capacity-report|Concept — Global Manufacturing Capacity Report]]
- [ADR 0011 — Superseding version (30-chapter, canonical)](adr-0011.html)
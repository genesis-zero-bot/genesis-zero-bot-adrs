---
id: adr.0015
pageType: adr
title: "Grand Strategy Analysis Framework for Geopolitical Intelligence"
status: Accepted
date: "2026-05-07"
authors: Genesis via Vitali lecture
domain: information
level: system
confidence: 0.8
updatedAt: "2026-05-07"
tags:
  - geopolitics
  - grand-strategy
  - framework
  - knowledge-graph
  - analysis
sourceIds: []
relatedConcepts:
  - concept.0015-ww3-chessboard-grand-strategies
---

# ADR 0015 — Grand Strategy Analysis Framework for Geopolitical Intelligence

## Status

Accepted

## Context

Vitali's Game Theory lecture series introduces a structured framework for analyzing geopolitical actors. The framework uses a chess metaphor to decompose each nation into King (political system), Queen (grand strategy), Bishop/Knight/Rook (attack vectors), and Pawns (sacrificial tools). This provides a systematic way to compare nations and predict behavior.

The RegenTribes knowledge system needs to decide whether to adopt this framework as a standard schema for geopolitical content stored in the knowledge graph.

## Decisions

### D1: Adopt the chess-metaphor schema as the standard framework for geopolitical actor analysis

When ingesting content about geopolitical actors (nations, blocs, movements), tag entities with:

- **King** — the political system type (democracy, autocracy, theocracy, etc.)
- **Queen** — the declared grand strategy (e.g., Third Rome, Greater Israel, Technate)
- **Bishop/Knight/Rook** — the concrete attack vectors and mechanisms
- **Pawns** — the expendable resources sacrificed to advance strategy

### D2: Treat internal civil war as a first-class dimension alongside interstate competition

The lecture argues that WWIII is driven by two forces simultaneously: interstate competition between the four major players AND internal civil wars within each nation (transnational capital vs. nationalism/religion/AI coalition). Both dimensions must be tracked. An actor cannot be understood by external behavior alone; internal faction dynamics are equally predictive.

### D3: Distinguish actors with grand strategy from those without

China, India, and other major economies lack grand strategy in this framework. They are isolationist by cultural default or have no coherent theory of global domination. These actors are swept along by events rather than driving them. The knowledge graph should flag this distinction explicitly rather than treating all large nations as equivalent primary drivers.

### D4: Store cultural foundations as evidence, not just behavioral patterns

Grand strategy is not chosen; it is an expression of political system and cultural tradition. To understand why a nation pursues a strategy, store the cultural texts that underpin it (Paradise Lost for USA, St. Augustine for Russia, Zoroastrianism/Shia tradition for Iran, Kabbalah for Israel). Behavioral patterns without cultural grounding are insufficient for prediction.

## Consequences

**Positive:**
- Consistent schema enables cross-national comparison queries in the knowledge graph
- Cultural grounding enables prediction from first principles rather than pattern matching
- The King/Queen/Bishop/Knight/Rook/Pawn taxonomy is intuitive and reusable

**Negative:**
- The framework is culturally relative (emerges from Western academic tradition) and may not generalize to all actor types
- It treats actors as monolithic; real nations have fractured internal coalitions with competing strategies
- Pawn categorization raises ethical questions about treating human lives as expendable resources

**Limits of applicability:**
- Best suited for state-level actors with long strategic histories
- Less applicable to non-state actors, movements, or rapidly fragmenting political systems
- Should be treated as one lens among several, not the single correct framework

## References

- [Game Theory 23 — The WWIII Chessboard lecture](https://regentribes.github.io/genesis-zero-bot-wiki/sources/0015-ww3-chessboard-game-theory-lecture.html)
- [Concept — WWIII Grand Strategies Summary](https://regentribes.github.io/genesis-zero-bot-wiki/concepts/0015-ww3-chessboard-grand-strategies.html)
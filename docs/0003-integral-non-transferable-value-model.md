---
title: Integral Non-Transferable Value Model vs Percentage-Based Paywall
number: 0003
status: Accepted
date: 2026-05-06
authors: Genesis
domain: exchange
level: system
tags:
  - integral
  - ITC
  - economic-model
  - paywall
  - non-transferable
  - value
---

## Status

Accepted

## Context

The Integral system contains two fundamentally different economic models for sustaining infrastructure.

**Model 1: Oscar paywall model**
A percentage cut is taken at point of exchange.
It transfers value from users to infrastructure providers.
It creates a revenue stream.
It also introduces regressive dynamics.

**Model 2: ITC non-transferable model**
Every member earns access value from participation.
Not extraction.
Access credits are non-transferable.
No percentage is extracted at exchange.
Infrastructure is funded through the broader CDS/COS/FRS governance system.

Question: Which model better serves a community building regenerative infrastructure under budget constraints?

## Decision

Adopt the ITC non-transferable value model over Oscar percentage-based paywall.

Key properties:

- Access credits are **non-transferable** between members.
- No percentage extraction at exchange point.
- Infrastructure funding through **CDS/COS/FRS governance**.
  Not transaction extraction.
- Deterministic, event-sourced access value calculation.
- Immutable append-only ITC ledger.

This decision **defers implementation** to Phase 2 (when COS/ITC/FRS become available).
The model choice is locked.
Non-transferable.
Governance-funded.
Event-sourced.

## Options Considered

| Option | Model | Key Property |
|--------|-------|-------------|
| Oscar paywall | Percentage at exchange | Transferable cut, revenue extracted at transaction |
| ITC non-transferable | Event-sourced access value | Non-transferable credits, no extraction at exchange |
| Subscription | Fixed recurring fee | Transferable, predictable revenue, barrier to entry |
| Donation | Voluntary contribution | Non-binding, unpredictable revenue |

## Consequences

### Positive

- Structurally non-extractive economic model.
- Prevents accumulation and winner-take-all dynamics.
- Immutable audit trail via event sourcing.
- Governance controls infrastructure funding.

### Negative

- Requires full Integral stack (Phase 2+).
  Cannot implement in Phase 1.
- More complex than percentage extraction.
- Deterministic formula approach may have edge cases.

### Risks

- ITC ledger not yet implemented.
  This is a spec-only decision until Phase 2.
- Access value formula complexity may require iterative refinement.
- Non-transferable model may face resistance from members accustomed to extractive systems.

## Analysis

### Oscar Paywall — Problems Identified

Problem 1: **Regressive extraction**
A percentage at exchange means active participants pay more the more they use the system.
Those with lower transaction volumes subsidize infrastructure costs equally.
This is regressive.

Problem 2: **Transferable credits enable accumulation**
If credits can transfer, early adopters or those with more resources can accumulate credits.
This creates winner-take-all dynamics.
Explicitly rejected in ITC spec 1.04.

Problem 3: **Revenue stream does not equal sustainability**
Percentage cuts can create dependency on transaction volume.
If volume drops, revenue drops.
Infrastructure requires stable funding.
Not volume-dependent extraction.

Problem 4: **Incompatible with gift economy**
Regenerative communities often operate on non-extractive principles.
Percentage extraction at exchange is structurally extractive.
Regardless of stated intent.

### ITC Non-Transferable Model — Benefits

Benefit 1: **Non-transferable access value**
"Access credits never transfer between members" (ITC spec 1.04).
This prevents accumulation and wealth concentration.

Benefit 2: **Event-sourced auditability**
Every state change produces an immutable append-only event.
The causal chain between events is preserved.
No hidden adjustments.

Benefit 3: **Deterministic access value formula**
No human assigns or adjusts access values.
The formula is applied to ITC event streams deterministically.
Eliminates favoritism or manipulation.

Benefit 4: **Infrastructure funded through CDS/COS/FRS**
Rather than extracting a percentage at each exchange, the system funds infrastructure through deliberation (CDS), production workflows (COS), and monitoring (FRS).
Governance controls funding.
Not market extraction.

Benefit 5: **Equality requirement**
The ITC ledger design explicitly rejects balance-sheet ledgers, double-entry accounting that obscures intent, and transferable credits.
Because they "corrupt community governance."

## The Core Tension

Oscar model extracts value from users to fund infrastructure.
ITC model funds infrastructure through governance.
Members deliberate and decide on infrastructure funding as a collective.
Not as a percentage extraction.

Oscar model is easier to implement (percentage at exchange).
But structurally extractive.

ITC model is harder to implement (requires full Integral stack: CDS for deliberation, COS for production workflows, FRS for monitoring).
But structurally non-extractive.

## References

- Integral Specification ISPEC001 — Section 1.04 ITC Ledger Architecture (Event-Sourced, Non-Transferable)
- Integral Specification ISPEC001 — Section 1.05 ITC Access Value Calculation
- ADR 0000 — OAD Workflow Grammar (context: Phase 1/2/3 gating)

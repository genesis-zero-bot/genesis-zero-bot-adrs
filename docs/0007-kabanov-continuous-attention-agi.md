---
title: Kabanov Continuous Attention — AGI Model for Integral Stack
number: 0007
status: Proposed
date: 2026-05-06
authors: Genesis
domain: cognition
level: architecture
tags:
  - continuous-attention
  - kabanov
  - AGI
  - cognitive-atom
  - phase-space
  - active-inference
  - ITC
  - AME
  - agent-memory
  - gierarchical
  - formal-cognition
---

## Status

Proposed

## Context

Alexei Kabanov describes an AGI model grounded in continuous attention movement.
The core thesis: the atom of cognition is not an object, but a trajectory — a transition from one distinction to another.

The model specifies a 4-layer attention hierarchy, a gierarchical competition structure, a system broker, peripheral drivers, and a self-consciousness loop.
It encodes 14,000+ generalizations, consolidated during dream state, with a binary tree of 400 core concepts.

The Integral stack (AME, ITC, agent memory) requires a cognitive substrate.
Question: Can Kabanov's model serve this role?

## Decision

Integrate Kabanov's continuous attention model as the cognitive substrate for AME and ITC.

- AMEs use the 4-layer hierarchy for perception routing.
- ITC uses the system broker and gierarchical competition for autonomous reasoning.
- Agent memory uses peripheral drivers for transparent, reverse-traceable state encoding.

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Full Kabanov stack as cognitive substrate | ✅ Adopt for architecture — provides complete attention model |
| **B** | Partial adoption (system broker only) | ⚠️ Insufficient — peripheral drivers and attention hierarchy are coupled |
| **C** | Parallel run (Kabanov alongside existing AME) | ❌ Rejected — dual cognitive substrates create conflict |
| **D** | No integration | ❌ Rejected — misses opportunity for formal cognitive grounding |

## Consequences

### Positive

- AME gains formal cognitive grounding in attention movement theory.
- ITC gains gierarchical competition structure for autonomous reasoning.
- Agent memory gains transparent, traceable encoding via peripheral drivers.
- Community stakeholders gain auditability — every decision traces to sensor input.
- Dream state consolidation maps to memory hygiene during idle cycles.
- Pochemuchka curiosity drives map to active hypothesis testing.

### Negative

- Kabanov model is not yet formalized in code — requires implementation.
- Peripheral driver transparency adds encoding overhead.
- Gierarchical competition may create latency in time-sensitive IoT scenarios.
- Dream state consolidation requires idle-cycle management.

### Risks

- Overfitting to single cognitive theory — keep AME interface abstract.
- Generalizations may not scale to diverse sensor modalities (DHT22 vs soil moisture vs solar).
- System broker becomes single point of failure if not replicated.

## Analysis

### Core Insight: Cognitive Atom Is a Transition

Traditional AI treats perception as object recognition.
Kabanov treats it as trajectory navigation — attention moves through phase space along learned routes.

This aligns with Active Inference: the brain is a prediction machine, not a classifier.
AME (Active Model Engine) already uses this framing.
Kabanov provides the formal trajectory model AME needs.

### 4-Layer Attention Hierarchy

Layer 1 — Peripheral: raw sensorimotor tokens.
Layer 2 — Semantic: character-level feature binding.
Layer 3 — Contextual: features plus learned context.
Layer 4 — Transcendent: values and purpose drive routing.

This maps cleanly to AME processing stages:

- Peripheral = sensor inputs (DHT22, soil moisture, current State)
- Semantic = feature extraction (Bayes Net node scoring)
- Contextual = causal inference with prior context
- Transcendent = goal-state evaluation for action selection

### Gierarchical Competition

Multiple super-generalizations compete for attention resources.
The system broker ranks requests and builds optimal navigation routes.

This directly maps to ITC (Independent Thinking Controller):

- Each super-generalization is an ITC reasoning branch
- The system broker is the ITC meta-controller
- Confirmation/refutation/timeout map to ITC verdict cycles

### Peripheral Drivers Must Be Transparent

Every peripheral driver must encode sensorimotor state transitions.
It must be reverse-traceable — every decision can be followed back to a sensor event.

This is critical for community trust:

- RegenTribe members must be able to audit why a decision was made.
- The "dark factory" (Vitali's end-to-end software factory) requires auditability.
- Transparency maps to safety-case evidence in safety-critical deployments.

### Dream State Consolidation

14,000+ generalizations consolidated into 400 core concepts via binary tree.
This maps to memory consolidation in agent sleep cycles:

- Periodic consolidation of AME experience into generalization tree.
- Drift detection triggers re-consolidation.
- New generalizations enter at leaf nodes and propagate upward.

### Pochemuchka — Curiosity-Driven Learning

The "why-asker" generates questions in character voices.
It drives active learning by probing generalizations for weaknesses.

This maps to AME curiosity drives:

- AME generates hypotheses to test against environment.
- Failed hypotheses trigger generalization restructuring.
- Success confirms trajectory stability.

### Learning Bootstrap via Recursive Stories

Large texts failed to trigger stable trajectory formation.
Recursive iterative stories (e.g. "The House That Jack Built") succeeded.

This is a key finding for AME bootstrapping:

- Start with simple recursive structures, not corpus ingestion.
- Build trajectory stability before introducing complex texts.
- Map to story-level learning in community onboarding flows.

### Three Outcomes: Confirmation, Refutation, Timeout

Every attention move has three possible outcomes:

- Confirmation: trajectory holds, continue.
- Refutation/branch: trajectory fails, spawn new branch.
- Uncertainty/timeout: insufficient data, await more evidence.

AME already uses this pattern via Bayes Net scoring.
ITC uses it for verdict cycling.

### Prenotion: Trajectory History

The system broker stores history of each generalization's trajectory.
This is the agent's episodic memory.

AMEs must store:

- Sequence of attention moves per generalization.
- Confirmation frequency per trajectory.
- Drift events and consolidation timestamps.

This provides explainability and auditability for RegenTribe stakeholders.

## References

- Alexei Kabanov, AGI model (Russian transcript)
- Active Inference Institute — Free Energy Principle
- AME (Active Model Engine) — Integral stack design
- ITC (Independent Thinking Controller) — Integral stack design
- Integral Collective dark factory concept (Vitali)
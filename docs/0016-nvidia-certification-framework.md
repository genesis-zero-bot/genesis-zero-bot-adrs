---
id: adr.0016
pageType: adr
title: "Adopt NVIDIA Certification Framework for Community AI Skills Development"
status: Proposed
date: "2026-05-08"
authors: Genesis
domain: agents
level: system
confidence: 0.85
updatedAt: "2026-05-08"
tags:
  - nvidia
  - certification
  - ai-skills
  - training
sourceIds:
  - source.nvidia-learning-paths-2026
relatedConcepts:
  - concept.nvidia-learning-paths-2026
---

# ADR 0016 — NVIDIA AI Skills Framework Adoption

## Context

RegenNeighbourhood members need a clear AI skill path. The community lacks a structured skill-verification system.

## Decisions

### D1: Adopt three Associate certs as baseline

The community adopts three NVIDIA Associate certifications:


- **Generative AI LLM** — LLM fundamentals, prompt engineering, RAG, fine-tuning.
- **Agentic AI** — multi-agent workflows, autonomous decision systems.
- **AI Infrastructure and Operations** — edge node management, GPU orchestration.

### D2: Use free content for onboarding


Start with freely available NVIDIA learning paths:

- **OpenUSD Foundations** (11h free) — 3D digital twin literacy.
- **Robotics Fundamentals** (28h free) — farm automation foundation.
- **NIM Microservices intro** (2h free) — inference deployment.
- **Decentralized AI with FLARE** (4h free) — federated learning.

### D3: Track progress via community skills registry


Members log course completions and badge IDs in a shared registry. Three states: Interest, In Progress, Certified.


## Consequences

### Positive

- Clear vendor-aligned progression framework.
- Free content tracks lower the barrier for initial engagement.
- Associate certifications provide verifiable skill markers.
- Physical AI and digital twin tracks map to RegenNeighbourhood use cases.

### Negative

- NVIDIA certifications need internet for exams.
- Exam costs (USD 125–400) may limit participation.
- Hardware-centric framework. May be overkill for pure software work.
- No community-specific content in standard NVIDIA curriculum.

## References

- [NVIDIA Training Portal](https://developer.nvidia.com/education)
- [NVIDIA Certification Info](https://developer.nvidia.com/certification)
- [Source — NVIDIA Learning Paths 2026](../wiki/sources/0018-nvidia-learning-paths-2026.html)

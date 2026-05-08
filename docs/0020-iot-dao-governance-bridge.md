---
id: adr.0020
pageType: adr
title: "IoT Data to DAO Governance Bridge Architecture"
status: Proposed
date: "2026-05-08"
authors: Genesis
domain: engineering
level: system
confidence: 0.75
updatedAt: "2026-05-08"
tags:
  - iot
  - dao
  - governance
  - bridge
  - active-inference
  - integral-collective
sourceIds: []
relatedConcepts:
  - concept:farmers-iot-toolkit
  - concept:gap-5
  - concept:integral-collective-node
  - concept:active-inference
---

# ADR 0020 — IoT Data to DAO Governance Bridge

## Status
Proposed

## Context

The Farmers IoT Toolkit (Float.ag funding, Ian/Vaipunu) captures physical sensor data: soil moisture, water tank level, solar powerbank state-of-charge, and DHT22 temperature/humidity. The Integral Collective Node runs a five-subsystem governance loop (OAD → ITC → CDS → COS → FRS). Gap 5 identifies that sensor data is collected but does not feed into or verify DAO governance decisions.

A bridge layer is needed to:
- Transform sensor readings into evidence for governance claims
- Enable DAO verification of physical-world assertions
- Support ITC contradiction detection against sensor-grounded reality
- Feed CDS deliberation with sensor-verified state

## Decisions

### D1: Adopt Active Inference Bridge as primary integration pattern

Sensor data enters the bridge as evidence in a Bayesian state estimation framework. The bridge implements the Active Inference Engine described in the Farmers IoT Toolkit architecture: POMDP state representation, causal model library (Bayes Nets), and belief updating against sensor readings. This maps directly to the ITC (Integral TRIZ Constructor) layer's contradiction detection.

Option 1 (Direct polling) and Option 2 (Oracle bridge) were rejected because they treat sensor data as raw values rather than evidence with uncertainty and correlation structure. The DHT22 shared latent variable (temperature/humidity) provides correlated inference across modules that a direct bridge cannot exploit.

### D2: SurrealDB as state broker for evidence and governance claims

All sensor readings are stored as evidence records in SurrealDB with:
- Timestamp, module_id, reading_value, confidence_score, anomaly_flag
- Causal links to derived claims (soil_moisture → irrigation_claim)
- ITC resolution status (pending, resolved, contradicted)

ITC contradiction detection queries this evidence store. CDS deliberation reads ITC outputs. COS execution writes confirmation receipts back as evidence.

### D3: Five-subsystem flow for sensor-driven governance

IoT data feeds ITC as sensing input (afferent synthesis). ITC resolves contradictions and emits verified claims to CDS. CDS updates governance state. COS executes resource decisions. FRS records audit trail. OAD provides architectural constraint checking on bridge design.

This creates a closed loop: physical sensing → ITC verification → CDS decision → COS execution → FRS audit → OAD constraint validation → back to physical sensing.

### D4: DHT22 as shared latent for cross-module inference

The DHT22 temperature and humidity readings serve as latent variables correlated across all four physical modules. The bridge implements inference passing: moisture_drop ∧ temperature_rise ∧ humidity_drop → irrigation_urgency_score. This aggregated evidence feeds governance claims with higher confidence than single-sensor readings.

## Consequences

**Enabled:**
- DAO governance decisions grounded in physical-world sensor data
- ITC contradiction detection against real-world measurements
- Cross-module correlated inference via shared DHT22 latent
- Audit trail from sensor reading to governance decision to COS execution to FRS record

**Risks:**
- Sensor tampering: physical sensor manipulation can false-feed governance. Mitigation: redundant sensor placement, cross-validation with weather station data (ITC cross-validation scenario)
- Latency: sensor-to-governance loop must complete within CDS deliberation cycle time. Mitigation: evidence store caching, ITC pre-resolution of routine sensor claims
- Trust assumption: bridge assumes honest sensor reporting. Governance must define measurement accountability (ITC accounting requirement)

**Deferred:**
- On-chain oracle integration (Option 2) — keep as fallback for external DAO verification
- Formal verification of bridge logic — future work under Gap 7

## References

- Farmers IoT Toolkit architecture (Float.ag funding, Ian/Vaipunu)
- Integral Collective Node five-subsystem model
- Gap 5 from Strategic Gaps analysis
- [Wiki Source — Integral Collective Node](../wiki/sources/0010-...html)
- [Concept — Active Inference Engine](../wiki/concepts/0010-...html)
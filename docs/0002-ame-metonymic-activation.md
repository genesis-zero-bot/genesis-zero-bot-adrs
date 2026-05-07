---
title: AME Architecture — Metonymic Activation and Virtual Trust Field
number: 0002
status: Accepted
date: 2026-05-06
authors: Genesis
domain: information
level: organ
tags:
  - AME
  - affinity-mapping
  - metonymy
  - virtuality
  - trust-field
  - linguistics
---

## Status

Accepted

## Context

The article "The Linguistic Sign: Metonymy and Virtuality" (DOI: 10.13092/lo.80.3565) by Radden and Kövecses provides a formal model for how linguistic signs activate meaning.

AME (Affinity Mapping Engine) from the Mythogen framework operates on a structurally identical mechanism.
A single detected value activates the entire relational field.
The overlap warrants documentation as an ADR.

## Decision

Integrate the linguistic metonymy model as theoretical grounding for AME architecture.
The trapezium model of virtual activation maps directly to AME Living Seed activation.
The FOT (Field of Trust) operates as a virtual field, not a direct measurement.

## Options Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **A** | Full Radden/Kövecses trapezium integration | ✅ Adopt — provides theoretical foundation for AME |
| **B** | Partial adoption (virtuality only) | ⚠️ Insufficient — metonymic activation is the key mechanism |
| **C** | No integration | ❌ Rejected — misses structural isomorphism with AME design |

## Consequences

### Positive

- AME single-element detection is architecturally sound.
  Detecting one value *should* activate the whole seed.
  Because the sign works metonymically.
- FOT is a field (not a score).
  Trust is virtually activated.
  Not directly measured.
- Trapezium structure provides a design pattern for expanding AME.
  Any new element should virtually activate the full trapezium: form → concept → projections → relationships.
- The article distinction between real-world activation and virtual activation is the theoretical foundation for AME anti-capture design.

### Negative

- Overfitting AME to the article model could lead to ignoring non-linguistic modalities (embodied, spatial, relational).
- V-crystal positions are not yet formally mapped to trapezium components.
  Needs design work.
- The 30-day time lock may be too conservative or too lenient depending on community velocity.
  Empirical tuning needed.

### Risks

- V-crystal positions are not yet formally mapped to trapezium components.
- The 30-day time lock may be too conservative or too lenient depending on community velocity.

## The Trapezium Model

### Article: Radden and Kövecses

DOI: https://doi.org/10.13092/lo.80.3565

Core claim: the linguistic sign means not by direct reference to the real world.
It means by virtually activating a trapezium-like configuration of forms, concepts, experienced projections, and relationships.
The process is metonymic (a part activates the whole) and virtual (indirect, not literal).

```
Form → Concept → Experienced Projections
         ↕
   Relationships (between all above)
```

The linguistic form (word) activates the concept.
The concept in turn virtually activates experienced projections and the relational network.
The whole configuration is engaged.
Not just the literal referent.

Key insight: "activation of the real world remains dubious or indirect"

### AME: Living Seed Activation Model

```text
Single detected VALUE
  ↓ metonymically activates
Entire Living Seed (needs + beliefs + principles + values)
  ↓ virtually activates
FOT (virtual trust field)
  ↓ virtually activates
Affinity connections + matching
```

### Direct Mapping

| Article Concept | AME Equivalent |
|----------------|----------------|
| Linguistic form | Detected seed element (a value, a need, a belief) |
| Concept | The Living Seed — the whole person |
| Experienced projections | V-crystal position, maturity, bloom cycles |
| Relationships | Affinity links, trust radius, FOT indicators |
| Virtuality | FOT = virtual field, not directly observable |
| Metonymy | One detected element activates the whole seed |
| Trapezium | Living Seed structure: needs + beliefs + principles + values + state + FOT |

## AME Architecture Details

### Living Seed

A Living Seed is NOT a static user profile.
It is a growing entity.

```text
LivingSeed {
  needs: Vec<Need>        // survival, belonging, growth
  beliefs: Vec<Belief>     // theories about reality
  principles: Vec<Principle> // action guides
  values: Vec<Value>      // what is lived with others

  state: SeedState        // GROWING | DORMANT | BLOOMING | SEEDING
  maturity: u8            // 0-100

  fot: FOTRecord          // 5 indicators, virtual trust field
  v_crystal: VPosition    // Victor|Villain|Victim|Vengeful|Virtuous|Vulnerable

  affinities: Vec<AffinityLink>
  trust_radius: u8
}
```

### The Four Distinctions

AME stores four distinct types of content.
Never conflated.

| Type | Changes | Stored Separately |
|------|---------|------------------|
| **Needs** | Weekly | ✅ |
| **Beliefs** | Monthly | ✅ |
| **Principles** | Quarterly | ✅ |
| **Values** | Annually or slower | ✅ |

Values require others to practice.
The Desert Island Test: you cannot practice generosity alone.
This is the relational foundation.

### Trust Formula

```text
Authentic Expression + Witnessed Resonance + Emotional Density = Trust Field (FOT)
```

**FOT = Field of Trust**.
A virtual field.
Not directly observable.
Inferred from 5 indicators.

| Indicator | Measures |
|-----------|----------|
| Mutual Support | Unprompted help events |
| Response Velocity | Rally speed from request to response |
| Difficult Topic | Conflict raised and resolution rate |
| Benefit Distribution | Value flow Gini coefficient |
| Psychological Safety | Unsafe disclosures and safe responses |

**Hologram Principle:**
FOT composite = `Math.min()` of all 5 indicators.
One off.
The whole field degrades.
Not averaged.

## V-Crystal and the Vulnerability Axis

The 6 positions:

- Victor — wins/succeeds
- Villain — causes harm
- Victim — feels powerless
- Vengeful — seeks retaliation
- Virtuous — judges morally
- Vulnerable — circuit breaker (AXIS)

Key distinction (Vic Desotelle):

> "Vulnerability is the AXIS (not a point).
> Virtuous and Vengeful are the POLES.
> Victor, Villain, Victim spin around the axis.
> Dynamic and alive."

## Time Lock and Maturation

The 30-day time lock:

- Patterns detected less than 30 days ago are NOT used for matching.
- Seed maturity affects how much weight new signals carry.
- Trust cannot be gamed in short windows.
  It accumulates through sustained virtual activation.

## Open Questions

- Does the trapezium model suggest AME should also track "experienced projections" separately from values and beliefs?
- Can the cognitive grammar approach (Langacker) inform how AME generates Why-Cards?
  Making explanations themselves metonymic?
- Should AME "membrane" (semi-permeable boundary) be mapped to the trapezium relationship layer?

## References

- Article: "The Linguistic Sign: Metonymy and Virtuality" — DOI 10.13092/lo.80.3565, Radden and Kövecses, Linguistik Online, 2017
- AME Implementation Guide v0.2 (github.com/regentribes/mythogen-ame/docs/AME_IMPLEMENTATION_GUIDE.md)
- AME Architecture Mythogen (~/Projects/mythogen-ame/docs/AME-Architecture-Mythogen.md)
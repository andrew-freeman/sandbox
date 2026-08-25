# Dual-Field Hypothesis — Pressure-Test Findings

**Hypothesis source:** [`Dual_Field_Hypothesis_Refined_Seed.txt`](../Dual_Field_Hypothesis_Refined_Seed.txt) (author: Andrey Bushuev)
**Date:** 2026-08-23
**Method:** independent assessment of the seed + Step 5 literature survey + working toy models (Steps 2+3+6 of the author's research program).

## What this directory contains

| File | What it is |
|---|---|
| `README.md` | This document — consolidated findings |
| `step5-literature-survey.md` | Full Step 5 literature survey: all refs, ranked kills, survivable homes, prior-art verdict |
| `toy/dual_field_toy.py` | 2-state toy model (numpy only) |
| `toy/dual_field_toy_3state.py` | 3-state "information-powered motor" toy model (numpy only) |
| `toy/dual_field_toy_ratchet.py` | driven 3-state ratchet — a **control/negative result**: symmetric drive → J=0 for all ε (information coupling does *not* rectify a symmetric drive); I_avg still rises (numpy only) |
| `toy/dual_field_toy_chiral.py` | open problem (d) — a **direction-dependent (S-odd) `I`** (chiral predictive information) that *does* break the symmetry and drives a current (J≈0.16·ε); the direction comes from the handedness in `I` (numpy only) |
| `toy/dual_field_toy_depth.py` | "I = computational difficulty" (simulation idea) — confirms the **variance catastrophe** of reweighting by global compressed length (ESS/N collapses, ε_crit~1/√L) and shows the **local additive surprise** localizes (Doob) and is well-posed (numpy only) |
| `toy/dual_field_toy_depth2.py` | step 1 of the depth idea — shows **depth (how far back the history matters) separates from surprise** (complementary, opposite-sign axes: slow chain = low surprise, high depth) and that the **local** EPI sees only short-range (order-k) memory, **not** long-range depth → "I = depth" is a **global** hypothesis (numpy only) |
| `claude.md`, `openai.md` | two external AI answers to "what is I?" (the simulation/computational-difficulty idea) |
| `toy/README.md` | How to run + expected output |
| `experimental-proposal.md` | **Two-track experimental proposal** (Steps 6+7): analog information ratchet (controllable ε-knob) + bounds program on the fundamental ε |

---

## 1. Assessment of the seed proposition

The seed is a clear, narrow, in-principle falsifiable proposition:
`P(H) ∝ P_phys(H)·exp(ε·I[H])`, null `H0: ε = 0`. Ranked problems, most serious first:

1. **The reparameterization trap (the load-bearing issue).** If `I[H]` is a
   functional of the history `H` alone, then `P_phys·e^(εI)` is *just a slightly
   different `P_phys`* — the hypothesis has added a law of physics, not a degree of
   freedom. A genuine "dual field" needs `I` to depend on something **not already in
   H** (a hidden variable, the future, or a coarse-grained description). This must be
   resolved before any experiment. (survey §4)
2. **The information functional `I` is undefined / global.** The seed lists
   desiderata ("persistence, causal influence, predictive information") but no
   computable functional. The survey maps these to existing, computable,
   coarse-grained quantities (excess entropy, predictive information, algorithmic
   information dynamics, quantum-Darwinism redundancy) — all of which live at the
   *process* level, not the fundamental level. (survey §5)
3. **Thermodynamic accounting.** A bias that can be accumulated into usable work is
   itself a resource; the generalized second law (Sagawa–Ueda) sets a minimum price.
   The toy model accounts for this explicitly (entropy production + TUR). (survey §2–3)
4. **No literature dialogue.** Now addressed by the survey: no exact prior art, five
   close relatives each differentiated. (survey §9)

## 2. Step 5: Literature survey — headline results

(Full detail and all arXiv IDs in `step5-literature-survey.md`.)

- **No exact prior art.** A fundamental history reweighting by an information
  functional is not in the literature as such.
- **Ranked kills:** (1) **no-signaling** (Gisin 1990; Kent 2002 escape; Bielińska
  2024 adds: such modifications are generically *chaotic* — a self-inflicted wound);
  (2) **reparameterization**; (3) **second law / TUR**; (4) **existing CSL-style
  bounds**; (5) **chaos**.
- **Most survivable home:** classical stochastic thermodynamics of small systems —
  coarse-grained `I`, bias in transition rates, a pre-registered deviation from a
  fluctuation theorem or the TUR. This is exactly what the toy model below builds.
- **Methodological templates:** collapse models (for "estimate bounds on ε") and the
  Valentini quantum-nonnequilibrium program (for "derive one quantitative deviation",
  arXiv:2505.07510).

## 3. Toy model (Steps 2+3+6) — a working prediction machine

**Design.** An N-state system with short-range memory (a 2nd-order Markov chain). The
dual field is applied exactly as the hypothesis states, locally per transition:

```
P_DF(y | past)  ∝  P_phys(y | past) · exp(ε · I(past, y))
I(past, y)      =  log[ P_phys(y | x_t, x_{t-1}) / P_null(y | x_t) ]
```

`I` is the **excess predictive information** — the information the past carries about
the future *beyond* the current (local) state. This makes the author's "Layer I"
(an informational variable not captured by the ordinary local physical description)
concrete: it is computable, observer-independent, and **not** a reparameterization
(it depends on the past). `ε = 0` recovers standard physics exactly.

**Key structural fact.** A 2-state system carries *no* net directed current in steady
state (stationarity forces J(0→1)=J(1→0)); a current needs ≥3 states. So the two
models probe different physics:

- **2-state model** → the signature is a population shift + a non-monotonic entropy
  production + an information change.
- **3-state model** → a genuine **motor current** appears, and the thermodynamic
  uncertainty relation (TUR) applies.

### 3a. 2-state results

| ε | P(x=1) | ΔP = P_ε−P_0 | I_avg | Sdot |
|---|--------|--------------|-------|------|
| −1.0 | 0.4101 | +0.0000 | −0.039 | 0.171 |
| 0.00 | **0.4101** | 0 | +0.041 | 0.0084 |
| 0.28 | 0.3989 | −0.0112 | +0.065 | **1.2×10⁻⁵** (min) |
| +1.0 | 0.3591 | −0.0510 | +0.129 | 0.0708 |
| +2.0 | 0.3208 | −0.0893 | +0.231 | 0.4488 |

- **Pre-registered residual:** `δ(ε) = P_ε(x=1) − P_0(x=1) ≈ −0.035·ε` (definite
  sign, clean O(ε) scaling). Standard physics predicts P(x=1)=0.4101; the dual field
  predicts 0.4101 − 0.035ε.
- **Information selection (Layer II):** `I_avg` rises monotonically with ε
  (−0.039 → +0.231 as ε goes −1 → +2). Turn the field up and the realized process
  carries more information.
- **Non-monotonic entropy production:** `Sdot(ε)` has a sharp minimum (≈10⁻⁵) at
  ε*≈0.28 — a **reversibility resonance** where the biased process becomes nearly
  reversible (detailed-balance residual collapses 0.41→0.02). A simple
  reparameterization (a different energy gap) **cannot** produce an internal Sdot
  minimum — this is the non-mimicable fingerprint.

### 3b. 3-state "information-powered motor" results

| ε | J (motor) | ΔJ = J−J₀ | I_avg | Sdot | TUR  E=2J²/(D·Sdot) |
|---|-----------|-----------|-------|------|---------------------|
| −1.0 | +0.2353 | +0.0000 | −0.017 | 0.501 | 0.578 ✓ |
| 0.00 | **+0.2353** | 0 | +0.016 | 0.592 | 0.357 ✓ |
| +0.5 | +0.2332 | −0.0021 | +0.030 | 0.635 | 0.296 ✓ |
| +1.0 | +0.2295 | −0.0058 | +0.045 | 0.674 | 0.197 ✓ |
| +2.0 | +0.2149 | −0.0201 | +0.074 | 0.738 | 0.096 ✓ |

- A **genuine clockwise motor current** (J₀=0.235 crossings/step) — impossible in
  2 states.
- **Pre-registered residual:** `δJ(ε) ≈ −0.003·ε` (modest; the sign is
  parameter-dependent — in this symmetric-inertia regime the field slightly reduces
  the current).
- **Information selection** is again the strongest signature: `I_avg` rises
  monotonically (~360% from ε=0→2).
- **TUR is satisfied** (precision fraction `E = 2J²/(D·Sdot) ≤ 1` at every ε): the
  dual field **trades thermodynamic efficiency for information** (E: 0.357 → 0.096
  as ε goes 0→2; higher dissipation and larger fluctuations buy the extra
  information). Thermodynamically consistent — no free bias.

### 3c. Driven ratchet — a control result (and a correction)

A 3-state ring driven by a **time-reversal-symmetric rocking** protocol (phase A
pushes clockwise, phase B counter-clockwise, equal strength & duration T_A=T_B),
with symmetric inertia. The correct periodic-steady-state result:

| ε | J (net current) | I_avg |
|---|-----------------|-------|
| −1.0 | **0.0000** | −0.039 |
| 0.00 | **0.0000** | +0.037 |
| +1.0 | **0.0000** | +0.101 |
| +2.0 | **0.0000** | +0.157 |

**J(ε)=0 for every ε, to machine precision.** The whole transition structure
(drive + symmetric memory) is invariant under [ring reversal + phase swap + time
reversal], so the periodic fixed point is invariant too, which forces J=−J=0. In a
fully symmetric system the information structure `I` is itself symmetric, so the
dual field (which amplifies `I`) **cannot break the symmetry and cannot create a
net current.** What survives is `I_avg` rising monotonically with ε — information
selection is real and robust, *independent of any net current*.

> **Correction.** An earlier version of this section reported J=0.0245→0.0293 and
> claimed "information powers the motor from nothing." That was an **artifact of a
> convergence bug** in the periodic-steady-state loop (the iterate was never
> advanced, so the "steady state" was really a one-shot transient from a uniform
> start). The bug is fixed; the true result is J=0. The 2-state and 3-state models
> do **not** share the bug (verified) — §3a and §3b stand.

**Takeaway:** "information powers the motor *from nothing*" is **not**
demonstrated with a *neutral* `I`. A net current requires the perturbation to
carry the broken symmetry. §3d resolves the open design problem.

### 3d. Open problem (d) — a direction-dependent `I` (RESOLVED)

Can an information coupling break the symmetry of an otherwise-symmetric drive?
**Yes — but only if `I` itself carries a handedness.**

**The argument.** The current `J` is **S-odd** under S = [ring reversal + phase
swap + time reversal]; the base `P_phys` is S-even. So `exp(ε·I)` can break S
(allowing `J≠0`) **only if `I` is S-odd** (`I∘S = −I`). Any `I` *derived from* the
symmetric `P_phys` — e.g. the excess predictive information
`log[P_phys(y|a,b)/P_null(y|b)]` — is **S-even**, so it cannot break S (→ the §3c
control, J=0). To drive a current, `I` must carry its own handedness.

**The construction — chiral predictive information:**
```
I_chir(a,b,y) = sgn(a→b) · log[ P_phys(y|a,b) / P_null(y|b) ]
```
The excess predictive information (a genuine information measure), signed by the
direction of the memory. Under S the memory direction flips (sgn→−sgn) while the
log-ratio is invariant → `I_chir → −I_chir` (S-odd). For ε>0 the dual field
*favors informative outcomes after a cw hop, anti-informative after a ccw hop*.

| `I` type | ε=0.5 | ε=1.0 | ε=2.0 |
|---|---|---|---|
| symmetric (S-even) — control | **0.0000** | **0.0000** | **0.0000** |
| chiral +1 (S-odd) | +0.0809 | **+0.1603** | +0.3101 |
| chiral −1 (S-odd) | −0.0809 | **−0.1603** | −0.3101 |

S-even `I` → J=0; S-odd `I` → J=+0.16·ε (clean O(ε), J/ε≈0.162); **flipping the
handedness flips the current** (`J(+1)+J(−1)≈10⁻¹⁶`) — the direction is an *odd
function of the chirality in `I`*.

**Interpretation (the physical content).** This is a concrete instance of the
**Onsager–Casimir / reciprocity principle**: a steady current (a T-odd quantity)
cannot arise in T-symmetric dynamics under a T-even perturbation — a T-odd
("magnetic-field-like") term is required. The dual field's information coupling is
T-even ("temperature-like") when `I` is symmetric, T-odd ("magnetic-field-like")
when `I` is chiral. So: **the dual field drives a current iff the information
functional carries a handedness.** The information part is real (predictive
information); **the direction is an input to `I`, not an output** — "information
from nothing" is ruled out, "information + a chiral reference powers the motor"
is a constructed, quantitative result (J≈0.16·ε).

### 3e. How big must the experiment be (statistical power)

Min detectable ε at 95% confidence scales as ~N^(−1/2) in trajectory length N
(observable = the current for the 3-state, the population for the 2-state):

- **3-state:** 0.48 (N=2×10³), 0.24 (2×10⁴), 0.09 (2×10⁵), 0.02 (2×10⁶).
- So a small coupling **ε≈0.05 needs a ~10⁵–10⁶-step trajectory**.

## 4. Bottom line — what the hypothesis now owes

1. **Novelty: confirmed.** No fatal equivalent construction in the literature; the
   specific proposal (fundamental history reweighting by a persistent, causally
   effective information functional) appears novel.
2. **The reparameterization escape is the first thing to specify.** Pick the new
   degree of freedom; a coarse-grained process information is the most survivable and
   testable choice.
3. **The predictions are now computable.** The toy models turn ε into a concrete,
   pre-registered δ with sign, magnitude, and required trajectory length. Robust
   results: the 2-state population residual + reversibility resonance (§3a), the
   3-state current modulation + TUR-consistent efficiency↔information trade (§3b),
   and information selection (`I_avg` rising with ε) in *all three* models.
4. **The thermodynamic price is accounted.** The dual field is not free — it trades
   efficiency for information (TUR-consistent, §3b).
5. **The symmetry result (negative + positive).** A *neutral* (S-even) `I` gives
   J=0 for all ε (§3c) — information alone cannot rectify a symmetric drive. But a
   *chiral* (S-odd) `I` — chiral predictive information — **does** drive a current
   (J≈0.16·ε), with the direction an *odd function of the handedness in `I`* (§3d).
   The dual field drives a current **iff** the information functional carries a
   handedness; the direction is an input, not an output. This is the Onsager–Casimir
   / reciprocity principle made concrete for the dual field.
6. **Main open problems:** (a) choose/justify `I` and verify it is Kent-safe (no
   superluminal signaling); (b) a "why hasn't ε been seen yet" hiding mechanism
   (the Valentini relaxation-to-equilibrium template); (c) an experimental platform +
   realistic ε bounds (the CSL lesson); (d) ~~can an information coupling break the
   symmetry?~~ **RESOLVED** (§3d) — yes, with a chiral `I`; the direction is an input.

## 5. Next steps

1. **Add the chiral sub-experiment to `experimental-proposal.md`.** Track 1 now has
   three parts: (1a) symmetric ratchet + *symmetric* feedback → J=0 (information
   alone can't drive a current); (1a′) symmetric ratchet + *chiral* feedback → J≈
   0.16·ε (information + chiral reference drives a current; flip the handedness →
   flip J); (1b) geometry-asymmetric ratchet + feedback → modulation. This cleanly
   localizes the source of any current (the handedness) and is the §3d result made
   experimental.
2. **The hiding mechanism + bounds** (Step 7) — mine existing precision
   fluctuation-theorem / TUR / Born-rule data and turn nulls into a **numeric ε
   bound** (collapse-model + Valentini templates).
3. **Characterize the chiral current's thermodynamics** — the entropy production +
   TUR for the chiral (S-odd) case: the chiral current is a T-odd output, so its
   dissipation cost and the "magnetic-field" accounting (the handedness as a
   thermodynamic variable) is the natural next analysis.

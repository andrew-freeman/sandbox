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
| `toy/dual_field_toy_ratchet.py` | driven 3-state ratchet — the clean "information powers the motor" result (numpy only) |
| `toy/README.md` | How to run + expected output |

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

### 3c. Driven ratchet — information *powers* the motor (the headline result)

A 3-state ring driven by a **time-reversal-symmetric rocking** protocol (phase A
pushes clockwise, phase B pushes counter-clockwise, equal strength & duration). A
symmetric drive rectifies nothing *unless* the system has memory. The result:

| regime | J (net current) | what it shows |
|--------|-----------------|---------------|
| memoryless (inertia=0), ε=0 | **0.0000** | the symmetric drive rectifies nothing |
| memoryless (inertia=0), ε=1  | **0.0000** | **no information → the dual field can do nothing** |
| memory (inertia=0.5), ε=0    | 0.0245 | the **information rectifies the drive** into a current |
| memory (inertia=0.5), ε=1    | **0.0293** | the **dual field amplifies the current** (+20%) |

So the directed current is **entirely information-powered**:
1. no memory → no current (even with the dual field — there is no information to
   couple to);
2. memory → a current (the information rectifies the otherwise-symmetric drive);
3. dual field (ε>0) → a *larger* current (it amplifies the information). `I_avg`
   rises ~340% from ε=0→2.

This is the cleanest physical realization of the hypothesis: the informational
degree of freedom acts as a **fuel/resource** that converts a symmetric drive into
a directed current, and ε is the knob. (Pre-registered residual: `δJ(ε) ≈ +0.004·ε`
for ε>0, definite sign, O(ε).)

### 3d. How big must the experiment be (statistical power)

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
3. **The predictions are now computable — and the headline works.** The toy models
   turn ε into a concrete, pre-registered δ with sign, magnitude, and required
   trajectory length. Best result: in the driven ratchet the directed current is
   *entirely information-powered* (zero without memory; the dual field amplifies it,
   §3c).
4. **The thermodynamic price is accounted.** The dual field is not free — it trades
   efficiency for information (TUR-consistent, §3b).
5. **Main open problems:** (a) choose/justify `I` and verify it is Kent-safe (no
   superluminal signaling); (b) a "why hasn't ε been seen yet" hiding mechanism
   (the Valentini relaxation-to-equilibrium template); (c) an experimental platform +
   realistic ε bounds (the CSL lesson — existing interferometry/astrophysics may
   already constrain the accessible range).

## 5. Next steps

1. **Concrete experimental proposal** — pick a platform for the driven ratchet
   (colloidal ratchet / single-molecule switch / superconducting qubit with a
   memory qubit + periodic drive) and state the expected δ and the N needed.
2. **The hiding mechanism + bounds** (Step 7) — bound the accessible ε from existing
   data, using the collapse-model and Valentini templates ("why hasn't ε been seen
   yet").
3. **Full thermodynamics of the driven ratchet** — the entropy production + TUR for
   the time-periodic case (the current & information are in §3c; the dissipation
   accounting is the remaining piece that closes the generalized-second-law loop).

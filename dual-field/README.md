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
| `toy/dual_field_toy_depth.py` | reweighting global vs local (corrected) — the ESS/measure-overlap collapse for global compressed length (any *extensive* observable, additive or not; ε_crit~1/√L) vs LOCAL additive functionals that localize (raw **surprisal** P^(1−ε), ε=1→fair coin, and **EPI**), kept as two distinct rules (numpy only) |
| `toy/dual_field_toy_depth2.py` | step 1 (corrected) — separates **surprisal (S) ≠ persistence (R) ≠ short-range memory (EPI)**; the long ξ of an order-1 chain is *persistence* (a local-dynamics property), **not** computational depth (numpy only) |
| `toy/dual_field_toy_depth3.py` | step 2 — **SUPERSEDED by depth4**: its premise (ξ is a lower bound on circuit depth) is false (parallel-prefix shortcut); the "reparameterization trap" framing was too strong (the new ingredient is the coupling ε) |
| `toy/dual_field_toy_depth4.py` | step 3 — CONSTRUCTS the shortcut: the SAME trajectory realized sequentially (D_causal=N) and by parallel prefix scan (D_min=log2 N), **measured** (A==B verified); ξ≈50 is a third quantity with D_min<ξ → the real ambiguity is the **D_causal vs D_min fork** (numpy only) |
| `review-round3-openai.md` | round 3 — ChatGPT review of depth3: refutes the ξ-bound (parallel prefix), separates size vs depth, names the D_causal/D_min ontological fork, softens the reparameterization objection |
| `claude.md`, `openai.md` | round 1 — two external AI answers to "what is I?" (the simulation/computational-difficulty idea) |
| `review-round2-claude.md`, `review-round2-openai.md` | round 2 — external review of the two depth scripts; caught the surprisal-vs-EPI mismatch (both, independently) and the persistence-vs-depth overreach |

**The S/R/K/D taxonomy (round-2 review; D refined in round-3).** Candidates that
must not be called by one symbol: **S** = surprisal/entropy rate (local, well-posed);
**R** = persistence/correlation time (a property of local dynamics, emergently
long-range); **K** = description/compression length (global, non-additive →
measure-overlap collapse); **D** = computational depth (Bennett's logical depth:
irreducible sequential generation cost). The local, well-posed machinery captures S
and EPI (no new mechanism); **D is the distinctive, hard, global half.** **Round-3
refinement:** "depth" is not one quantity — there is a fork (depth4):
**D_causal** = the actual causal depth (how the universe *really* propagates:
streaming, step-by-step, = N) vs **D_min** = the minimum generative depth (the
shallowest circuit that reproduces the trajectory, shortcuts allowed, = O(log N) via
parallel prefix). The same trajectory has *both*, and they differ by N/log N. ξ (R)
is a third quantity and is **not** a lower bound on D_min. So "I = depth" is
**undefined until the D_causal/D_min fork is settled** — choosing either gives
different physics. (And the new ingredient is the *coupling* ε≠0, not a new state
variable — the "reparameterization" objection is not substantive, since any
modification can be renamed into P'_phys.)
| `toy/README.md` | How to run + expected output |
| `experimental-proposal.md` | **Two-track experimental proposal** (Steps 6+7): analog information ratchet (controllable ε-knob) + bounds program on the fundamental ε |
| `psychedelic-ab-fork-note.md` | A/B fork diagnostic (2026-11-21) — psychedelic phenomenology (LSD 5-HT2A entorhinal disconnection; ketamine NMDA dissociation) holds the substrate ~fixed and retunes the generative model → experience tracks the description layer (B); **under the stated experience assumption the fork leans D_min (B)**; 2-layer toy design + pre-registered predictions + results |
| `toy/dual_field_toy_2layer.py` | 2-layer substrate/experience toy — ONE fixed 1st-order-chain trajectory (layer A, D_causal=N) + bit-flip gate γ (layer B, entorhinal-disconnection formalization); all pre-registered closed forms verified (I=1−h(γ), ρ_Y(k)=ρ_X^k(1−2γ)², H_1=h((1+ρ_X(1−2γ)²)/2)) + H_∞ (Bayes filter) + corrected 1/e persistence; A invariant / B freely parameterized → the experience is a B-object (numpy only; round-4 corrected) |
| `toy/dual_field_quantum_nosignal.py` | **two-qubit no-signaling check v1 (§3f, 2026-11-21)** — P' ∝ P·exp(εF) on |Φ⁺⟩, Alice basis X vs Z, Bob fixed Z; the reweighting of the full joint branches leaks Alice's basis choice into Bob's marginal for Alice-local (Δ~ε/4) and joint/future F (Δ~ε/8); the Bob-local F survives to all orders in the tested direction (factorization); closed forms verified to 8×10⁻¹⁷ (exact linear algebra, numpy only); two bugs found by the round-5 review are fixed in place and marked |
| `toy/dual_field_quantum_nosignal2.py` | **no-signaling v2 / round-5 extension (§3f, 2026-11-22)** — the full 2×2 square (all 4 corners × 3 F classes × both directions, hand-derived closed forms to 8×10⁻¹⁷); the product-state safe-family proposition (w = s(a,x)·r(b,y), per-corner factorization leaks 40/40); the entangled-family no-go theorem (scoped: 2×2, XZ plane, |ψ_θ⟩ family — all-state no-signaling forces w = c(α,β), i.e. P′ = P); a CPTP positive control (observable local change + no signaling coexist); the to-first-order null space of the tested square (16 F-values, 4 constraints, nullity 12) |
| `toy/dual_field_quantum_nosignal3.py` | **no-signaling v3 / the GENERAL no-go (§3f, 2026-11-22, round 6)** — extends v2 from the scoped XZ-plane/correlated-family theorem to the full 2×2 statement: ALL states + ALL local projective 2-outcome settings (full Bloch sphere). Establishes that no-signaling for every state ⟹ F is outcome-independent (P′ = P). The key new subtlety: \|Φ⁺⟩ ALONE is NOT sufficient — the joint outcome term e^{εkab} is exactly no-signaling-safe for \|Φ⁺⟩ but leaks for \|ψ_θ⟩ (θ≠π/4) with closed form \|cos2θ\|·tanh(εk) (verified to 10⁻¹⁶); \|Φ⁺⟩ kills the a/b local terms, the correlated family θ≠π/4 kills the a·b term. Closed forms hand-derived, hard-asserted; numpy only |
| `ab-fork-one-pager.md` | **"One substrate, many representations" — the self-contained, forwardable artifact (2026-11-21, round-4 corrected):** no backstory required; the A/B fork, the 2-layer closed-form demonstration (13/13 PASS, corrected H_1/H_∞ + persistence metrics), the three findings, the psychedelic hook, the honest limits, and room positioning (reach room = this page; physics room = opener + the ε-program numbers) |
| `toy/dual_field_quantum_auxiliary.py` | **the P⊗I auxiliary model (§3h, 2026-11-22, the review's commit #2 — "take Dual Field literally")** — an ACTUAL second dynamical sector 𝓘 coupled to the physical qubits A,B by a joint unitary U = e^{−iε H_int} (free H_AB=0; 𝓘 starts in |0⟩): a LOCAL coupling GEN = Z_A I_B Z_I vs a JOINT coupling INFO = Z_A Z_B Z_I, on the correlated A-B family ρ_c = ¼(I+XX) + (c/4)(IX+XI) (c∈[−1,1]). Three parts, all pre-registered and hard-asserted to machine precision (numpy only, exit 0): **(A) no-signaling holds** (a joint unitary is CPTP → Bob's marginal is independent of Alice's setting, Δ_B ≤ 1.1×10⁻¹⁶ for GEN, INFO, and a generic random coupling — no automatic FTL, unlike the killed reweighting); **(B) observable, reproducible back-action** with the EXACT closed form **D_B(INFO, c, ε) = |c|·sin²ε** (Bob's Bloch vector stays on the x-axis, x-component = c·cos 2ε; D_AB = O(ε); the back-action is a 2nd-order "virtual" process because [Z_𝓘,|0⟩⟨0|]=0 kills the first order); **(C) the informational (nonlocal) signature**: a LOCAL coupling leaves the remote party EXACTLY invariant (D_B = 0 for all c,ε), while the JOINT coupling reaches the remote party in a way a local one cannot (D_B = |c|sin²ε, even in c, zero at c=0) — the structural property ordinary local environmental noise lacks. Sharpens the open question: is coupling 𝓘 to the JOINT observable (Z_A Z_B vs Z_A) what lets the back-action reach the remote party? |
| `toy/dual_field_quantum_auxiliary2.py` | **the HONEST A↔𝓘↔B auxiliary model (§3i, 2026-11-22, the review's commit #3 — round 7 killed §3h's *interpretation*, not its numerics)** — the round-7 review (`~/feedback_quantum_aux`) ran §3h and confirmed every closed form, but found: (1) 𝓘 was a **spectator eigenstate** (Z_𝓘\|0⟩=\|0⟩ → the model reduced to the DIRECT Z_A Z_B interaction), (2) the no-signaling test was a **completeness tautology** (global CPTP ≠ no-signaling; the correct encode-then-read test gives D=\|sin 2ε\|), (3) c was **locally visible** (ρ_A=ρ_B=½(I+cX), so ⟨X_A⟩=⟨X_B⟩=c). PART A re-verifies all three to ~10⁻¹⁶. The honest model: 𝓘 coupled via **H_int = (Z_A+Z_B) X_𝓘** (A↔𝓘↔B, **no direct A-B term**; [X_𝓘,\|0⟩⟨0\|]≠0 so 𝓘 genuinely participates), on the \|00⟩-\\|11⟩ coherent family ρ_θ (all marginals = I/2 → all local observables fixed; θ = the joint \|00⟩-\\|11⟩ coherence). Three pre-registered, machine-precision parts (numpy only, exit 0): **(Q1) 𝓘 participates** — ρ_𝓘^final = diag(cos²2ε, sin²2ε) (θ-independent), S(ρ_𝓘)=h(cos²2ε)>0; **(Q2) the 𝓘-mediated A→B channel** — CPTP (no auto-FTL), the joint \|00⟩⟨11\| coherence dephased by **cos 4ε** (the causal timescale), Bob's local state invariant (no LOCAL A→B signal); **(Q3) the response distinguishes JOINT info with all local observables fixed** — **D_AB(θ,ε) = (θ/2)\|1−cos 4ε\|**, so θ=0 and θ=1 (|Φ⁺⟩) share identical marginals but differ in back-action (0 vs ≈0.971). Sharpens the open question: is dephasing-in-a-joint-observable the GENERIC auxiliary back-action, or specific to the Z-structure coupling? |

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

### 3f. Two-qubit no-signaling check — the first wall from existing physics (2026-11-21; extended 2026-11-22)

`toy/dual_field_quantum_nosignal.py` (v1, round 4) and
`toy/dual_field_quantum_nosignal2.py` (v2, round-5 extension; exact linear
algebra, numpy only, no quantum hardware).

**Setup (v1).** Put the reweighting `P' ∝ P·exp(εF)` on
**|Φ⁺⟩ = (|00⟩+|11⟩)/√2** — Alice chooses her measurement basis (Z or X),
Bob always Z, no communication. The branch is the full joint outcome (a,i,b);
the reweighting acts on branch probabilities with per-setup normalization; the
test is `Δ_B = TV(P'_B(·|X), P'_B(·|Z))` — Alice's basis choice leaking into
Bob's marginal is a signaling channel.

**v1 result (round 4, 2026-11-21)** — closed forms reproduced to 8×10⁻¹⁷:

| F class | Δ_B(ε) closed form | 1st order | verdict (corrected 2026-11-22) |
|---|---|---|---|
| 1. Alice-local (references the upstream branch) | ½·tanh(\|ε\|/2) | ε/4 | **LEAKS** (Alice→Bob) |
| 2. Bob-local (F = b, Bob's own outcome) | 0 to all orders *in this direction* (e^{εf(b)} factors out of the sum over i) | — | **SURVIVES in this direction only** — leaks in the flipped direction (round 5) |
| 3. Joint/future (F = i′·b, upstream × downstream) | \|e^ε−1\|/((3+e^ε)(1+e^ε)) | ε/8 (ε>0) | **LEAKS** (both directions) |

**Round 5 (2026-11-22): external review → two real v1 bugs, both independently
re-verified to machine precision before fixing.** (1) The "Bob-local SURVIVES"
was the tested corner, not physics: flipping the direction (Alice fixed Z, Bob
chooses Z/X) the Bob-local F leaks into Alice's marginal with
Δ_A = ½·tanh(\|ε\|/2) (0.2311 at ε=1). (2) The case-3 closed form was wrong for
ε<0 — the old form (e^{\|ε\|}−1)/((3+e^{\|ε\|})(1+e^{\|ε\|})) assumed ε>0; the
correct form uses e^ε in the denominator (0.13721 vs old 0.08081 at ε=−1); v1's
ε list was all-positive, so it was hidden. Also scoped: v1's "one linear
constraint" is the to-first-order condition of the *tested* setup (16 F-values
→ 4 independent first-order constraints, nullity 12 — the surviving family is
large), not the universal no-signaling condition.

**The full 2×2 square (v2, part A)** — all four corners, both directions, all
three F's (Δ = TV of the remote local marginal across the sender's two
settings; closed forms hand-derived, reproduced to 8×10⁻¹⁷; the two
bug-fix cells were pre-registered across all ε including negative):

| F | A→B @B=Z | A→B @B=X | B→A @A=Z | B→A @A=X | closed form |
|---|---|---|---|---|---|
| 1. Alice-local | 0.1225 | 0.1225 | 0 | 0 | ½·tanh(\|ε\|/2), A→B only |
| 2. Bob-local | 0 | 0 | 0.1225 | 0.1225 | ½·tanh(\|ε\|/2), B→A only |
| 3. Joint | 0.0527 | 0.0527 | 0.0527 | 0.0527 | \|e^ε−1\|/((3+e^ε)(1+e^ε)), all corners |

(values at ε = 0.5.) **Reading: each local F leaks in exactly the direction v1
never tested; the joint F leaks everywhere. NO outcome-referencing F survives
the full square on |Φ⁺⟩.** The round-4 dichotomy survives in corrected form:
what fails is the branch-*reweighting* architecture, not "informational
physics" in general — the positive control below shows observability +
no-signaling coexist once the coupling is dynamics.

**Product-state proposition (v2, part C; statement + proof sketch + numerics).**
For product states, the reweighting preserves both marginals for ALL product
states and ALL settings ⟺ the weight factors as
`w(a,b,x,y) = s(a,x)·r(b,y)` — each party's factor depends only on its OWN
outcome and its OWN setting (setting-local factors; in the exponent,
F = F_A(a,x) + F_B(b,y)). *Sufficiency:* the common factor cancels in both
marginals against the per-corner normalization:
P′_B(b|x,y) = P_B(b|y)·r(b,y)/Σ_{b′}P_B(b′|y)r(b′,y) — x-independent (mirror for
A). *Necessity (sketch):* with τ = I/2 the Bob-direction no-signaling condition
is, for all σ, x, x′, an identity in σ of the ratio
[Σ_a P_A(a|x)w(a,b,x,y)]/Σ_{b′}(·) = [same at x′] — a ratio of linear forms in
σ. Evaluating at (x,x′) = (Z,X) with σ = diag(p,1−p) — such σ's X-distribution
is pinned at (½,½), independent of p — and separating the p and (1−p)
coefficients gives w₊(b)·Σ_{b′}(w₊(b′)+w₋(b′)) = (w₊(b)+w₋(b))·Σ_{b′}w₊(b′)
and the w₋-mirror; the two force w₊(b)/w₋(b) to be b-independent (a fixed
ratio), i.e. the b-profile is universal across Alice's outcomes:
w(a,b,x,y) = W_a(x,y)·r(b,y); the mirror argument (Alice direction) makes the
a-factor setting-local; together, up to a per-corner scale absorbed by
normalization: w = s(a,x)·r(b,y). *Numerics (40 random product states × random
XZ axes):* safe family → max Δ = 2×10⁻¹⁶ (machine 0); the tempting per-corner
factorization w = e^{A(a,x,y)+B(b,x,y)} (remote-setting dependence inside a
factor) leaks on 40/40 (min max-Δ 3.2×10⁻²); a generic non-separable w leaks on
40/40.

**Entangled-family no-go theorem (v2, part D — the reviewer's "no-go I'd try to
prove next", now a theorem within its stated scope).** *Scope:* 2×2 qubits; all
projective 2-outcome settings in the XZ plane (continuous); the correlated
family |ψ_θ⟩ = cosθ|00⟩ + sinθ|11⟩, θ ∈ (0,π/2). *Statement:* any positive
weighting w(a,b,α,β) whose reweighted Bob AND Alice marginals are both
independent of the remote setting — for ALL θ, all α, β — is outcome-constant
per corner: w = c(α,β), hence P′ = P (operationally trivial). *Mechanism/proof
sketch:* the reweighted Bob marginal at corner (α,β) is
f(α) = [S_A(1+c·cosβ)+Δ_A(c·cosα+cosα·cosβ+sinα·sinβ·sin2θ)] /
[2(S_A+Δ_A·c·cosα)], with S_A = w₊+w₋, Δ_A = w₊−w₋ (Alice-factor values at
setting α; c = cos2θ). f(α) ≡ k for all α forces Δ_A(α) ≡ 0 for generic
(β,θ): clear the denominator and project the resulting trigonometric identity
onto the sinα/cosα Fourier modes — (t−kc)∫Δ_A sin2α + v∫Δ_A = 0 = the mirror,
v = sinβ·sin2θ; for positive Δ_A, ∫Δ_A = 0 on the open (β,θ) set where
(t−kc)² ≠ v² forces Δ_A ≡ 0. The mirror argument kills the Bob factor.
*Numerics (v2 part D):* every nontrivial member of the product-state-safe
family (the F1/F2 classes) leaks at the standard corners at EVERY tested θ
(min leak 0.0325; at θ = π/4 both directions = ½·tanh(\|ε\|/2)), while the
trivial w gives Δ = 8×10⁻¹⁷. **Conclusion: within the stated scope, naive
globally-normalized branch reweighting is INCOMPATIBLE with universal
no-signaling unless the weighting is operationally trivial.** Generalization is
open work: all states (not just the correlated family), higher dimensions,
POVMs (the product-state proposition is the template for the necessity side;
the sinα mechanism is expected to survive).

**Positive control (v2, part B) — the escape route that works.** A local CPTP
channel as *dynamics* (Bob's qubit reset to |1⟩; Kraus K₀=|1⟩⟨0|, K₁=|1⟩⟨1|,
ΣK†K = I) changes Bob's local statistics observably
(P(s_b=−1|Z): 0.5 → 1.0) while preserving the trace and giving Δ = O(10⁻¹⁷) in
both directions. So the no-go is against the *branch-reweighting* architecture
(acting on measured joint branches with per-corner normalization), not against
informational modifications of physics in general: observability + no-signaling
COEXIST once the coupling is a valid (linear, CPTP-or-more-general) evolution
of ρ — at the cost of the reweighting's simplicity. This is the live direction
for the dual field: "the information functional couples to the state" must
mean something like this, not a reweighting of measurement branches.

**Ledger update (2026-11-22):** classical exponential weighting = valid toy
machinery; symmetry breaking = understood (§3c/d); depth-shortcut ideas =
refined (A/B note); naive quantum branch weighting = killed by no-signaling
(scoped, here); dual-field core = still open. Next steps on this thread:
(1) generalize the no-go (all states / dimensions / POVMs); (2) formulate the
CPTP alternative architecture (what IS the dual-field evolution, concretely?);
(3) the to-first-order null space (v2 part E: 16 F-values, 4 independent
first-order constraints on the tested square, nullity 12; 200/200 random
null-space members non-constant in the outcomes) = what the 4-corner test
ALONE can and cannot establish. The O(ε) marginal shifts remain the signature a
later no-signaling/Bell-type hardware test would look for — the hierarchy
stands: first linear algebra (done, now scoped), then simulation, then maybe
quantum experiment.

### 3g. Round 6 — the "what's left" strategic review + the GENERAL no-go (2026-11-22)

An external strategic review (ChatGPT; `~/feedback_dual_field_whats_left`) was
received asking *"what mathematical forms could produce an informational
residual without immediately contradicting ordinary physics?"* and proposing a
branch ledger + the next three commits. It was verified accurately before
integration. Three load-bearing external citations were checked and all three
are accurate and on-point:

1. **The "fence"** — Simon, Bužek, Gisin, *"No-signaling condition and quantum
   dynamics,"* **PRL 87, 170405 (2001)** (arXiv:quant-ph/0102125; PubMed
   11690257). Abstract, verbatim: no-signaling + (1) states = Hilbert rays +
   (2) Born/trace rule ⟹ *dynamics = linear completely-positive maps on density
   matrices.* This is exactly the fence the review invokes: the ensemble ρ must
   evolve linearly/CP, which is what an explicit extra sector (below) satisfies
   automatically and what a post-hoc branch reweighting generally does not.
2. **The collapse "narrow corridor"** — *"Introduction to Dynamical Wave
   Function Collapse: Realism in Quantum Physics, Vol. 1"* (Oxford, 2024),
   **CSL Theory** chapter. Confirms stochastic-collapse models (nonlinear
   stochastic single-trajectories + linear/CP ensemble master equation) as the
   working example of "nonstandard microscopic dynamics that is NOT
   automatically FTL."
3. **The global-history branch** — Zhao, Tang, Zhang, *"Nonequilibrium
   statistical mechanics revealed by Doob h-transform and variational
   autoregressive networks,"* **PRE 111, 034120 (2025)**. Confirms tilted /
   Doob-h-transformed trajectory ensembles as a current, active tool — so the
   "could a history weighting be a fundamental law rather than a conditioned
   ensemble, and what observable distinguishes them?" question is live, not
   broken.

**Branch ledger (review's table), cross-checked against our rounds 1–5:**

| Branch | Review status | Our verification |
|---|---|---|
| Naive branch weighting P′∝P·e^{εF} | "severely wounded / probably dead QM" | **Now PROVEN dead (scoped 2×2):** §3g no-go below — the "what remains to test" is done |
| Classical exponential trajectory weighting | "alive mathematically" | Accurate — a standard conditioned/tilted ensemble (Doob h-transform); the real question is fundamental-law-vs-conditioned |
| Depth = correlation time | "dead" | Accurate — the long ξ is *persistence* (local dynamics), not depth (§3, A/B note) |
| Depth as global F[H] | "alive, difficult" | Accurate — genuinely a whole-history quantity; the open work is defining it without representation cheating + sampling |
| Information = surprisal | "alive as quantity, wrong as depth" | Accurate — S ≠ R ≠ short-range memory (EPI); a control, probably not the sought 𝓘 |
| Chiral informational current | "valid toy behavior" | Accurate — the ε-program / ratchet demonstrates the symmetry structure, not fundamental evidence (§3c/d) |
| Explicit 2nd informational DOF | "**very much alive**" | The central proposal — the P⊗I auxiliary model below; the CPTP positive control (§3f) is the first concrete step |
| Quantum info coupling at ρ level | "alive under severe constraints" | Accurate — the SBG fence (linear/CP ensemble) is the constraint |
| Life/AI/cosmology | "parked" | Accurate — the survival question has moved down to the microscopic core |

**The GENERAL 2×2 no-signaling no-go (v3, `dual_field_quantum_nosignal3.py`)** —
the review's "next cheap kill" ("finish murdering the old one properly"),
completed and verified to machine precision. *Statement:* for 2×2 qubits, the
branch reweighting P′(a,b|n,m) = P(a,b|n,m)·e^{εF(a,b,n,m)}/Z preserves
no-signaling (both directions) for **every** state ρ and **every** local
projective 2-outcome setting pair (n,m) [full Bloch sphere] **iff** F is
independent of the outcomes (a,b) — in which case e^{εF} factors out and
P′ = P. *Proof sketch:* (⟸) trivial (P′ = P). (⟹) the all-states hypothesis
implies no-signaling on the correlated family |ψ_θ⟩ = cosθ|00⟩+sinθ|11⟩ for all
θ; to first order in ε the constraint is linear in F, and decomposing F in the
{1, a, b, ab} character basis on {±1}² with P(a,b|n,m) = ¼[1 + a·n·u + b·m·u +
ab·n·T·m], u = (0,0,cos2θ), T = diag(sin2θ, −sin2θ, 1): the a-only and b-only
components leak at θ = π/4 (|Φ⁺⟩) already (TV = ½·tanh(ε/2) for F1), and the ab
(joint) component is safe at θ = π/4 but leaks for θ ≠ π/4. Every non-constant
component is killed ⟹ F = f(n,m). *The key new subtlety (beyond round 5):*
**|Φ⁺⟩ alone is NOT sufficient** — the joint outcome term e^{εkab} is *exactly*
no-signaling-safe for |Φ⁺⟩ (both directions, all settings; v3 part C, Δ =
5.6×10⁻¹⁷) but leaks for |ψ_θ⟩, θ≠π/4, with the hand-derived 2-point closed
form **A→B TV = |cos 2θ|·tanh(εk)** (v3 part D, verified to 10⁻¹⁶ at θ =
0.2/0.3/0.5/0.7/1.0; vanishes exactly at θ = π/4). e^{εkab} is also *not*
rank-1 (det = 2 sinh 2εk ≠ 0), so it is not in the round-5 product-state safe
family and leaks for some product states too (|0⟩⊗I/2: A→B = 3.8×10⁻¹). So the
**all-entanglement** condition (the correlated family for every θ ⊂ "every
state") is what kills the joint term; |Φ⁺⟩ alone kills only the local terms.
*Scope:* 2×2, projective 2-outcome settings (full sphere), all states. *Open:*
higher dimensions, POVMs. *Conclusion (clean project result, as the review
wants):* **universal branchwise exponential reweighting is incompatible with
no-signaling except in the trivial (outcome-independent) case — so we stop
writing toys around the reweighting mechanism.**

**The surviving route the review pushes: take "Dual Field" literally.**
Instead of rescaling probabilities *after* QM generates branches (P → P·e^{εF},
which the no-go kills), introduce an **actual additional dynamical subsystem**
𝓘 with H_total = H_P + H_𝓘 + ε·H_int, joint state ρ_{P𝓘} evolving under a
legitimate quantum map ℰ, and observe only ρ_P = Tr_𝓘 ρ_{P𝓘}. Advantages:
(1) QM already handles inaccessible degrees of freedom (decoherence, memory,
non-Markovian dynamics); (2) if the joint evolution is unitary/CPTP, the reduced
ρ_P dynamics is automatically linear/CP (the SBG fence) — so no automatic FTL;
(3) "second field" gains operational meaning. **Proposed concrete next toy
(not yet built — the review's commit #2):** `dual_field_quantum_auxiliary.py` —
two physical qubits A, B (start entangled) + one informational qubit 𝓘; weak
interaction U = e^{−i t(H_AB + ε H_{A𝓘/B𝓘})}; the question: *can 𝓘 alter locally
observable statistics in a reproducible way while Alice's measurement choices
still cannot signal to Bob?* If every interesting H_int just looks like an
ordinary hidden environment, that is a useful failure (Dual Field → ordinary
extra field); if 𝓘 must carry a structural property ordinary environmental
noise lacks (memory across histories, coupling to causal organization), that
locates the real novelty. **Review's commit #3:** a `STATUS.md` ruthless ledger
(survives / artifact / tautology / killed / open) — the archaeology made
visible. The review's framing, which we agree with: after all the destruction,
the hypothesis is closer to its *original* name — **two actual coupled dynamical
sectors**, not "ordinary physics + an informational scoring function." The
survival question has moved down to: *can an informational degree of freedom
couple to quantum matter nontrivially, observably, and without violating
no-signaling?* If no, nearly everything upstream dies; if yes (even in one
construction), the project changes character.

### 3h. The P⊗I auxiliary model — "Dual Field" taken literally (2026-11-22, the review's commit #2)

The review's central surviving proposal, built and verified in
`toy/dual_field_quantum_auxiliary.py` (numpy only, pre-registered closed forms
hard-asserted, exit 0). Instead of rescaling branch probabilities *after* QM
generates them (the reweighting, killed by the §3g no-go), introduce an **actual
second dynamical subsystem 𝓘** coupled to the physical qubits A,B by a **joint
unitary**, and observe only the reduced physical state:

```
Physical: qubits A, B.   Informational: qubit 𝓘.   Total dim = 8.
Joint unitary   U(ε) = exp(−i ε H_int)        (free H_AB = 0; t = 1; 𝓘 starts in |0⟩).
GEN  = Z_A I_B Z_I   (𝓘 couples to a LOCAL observable of A — an ordinary environment)
INFO = Z_A Z_B Z_I   (𝓘 couples to the A-B JOINT observable Z_A Z_B — the informational case)
Initial A-B state:  ρ_c = ¼(I + X X) + (c/4)(I X + X I),  c ∈ [−1,1]
        (c = the A-B single-flip (IX+XI)/2 joint coherence: c=0 → a Bell-state
         mixture [classically X-correlated, <XX>=1, <ZZ>=0]; c=±1 → |+>|+> / |->|->.
         c is a property of the JOINT state, not of either local state alone.)
```

**Result A — No-signaling holds (the architecture is valid; no automatic FTL).**
For GEN, INFO, **and a generic random 8-D coupling** (a CPTP unitary with no
special structure), Bob's marginal is independent of Alice's local setting (X vs
Z): max Δ_B = 1.1×10⁻¹⁶ across all couplings, c, ε. This is the Simon–Buzek–Gisin
fence in action: a joint unitary is CPTP, so the reduced ρ_P dynamics is linear/CP
**by construction** — the reweighting auto-signaled precisely because it was a
post-hoc *non*-CPTP map on measured branches. *The auxiliary architecture does not
inherit the reweighting's fatal wound.*

**Result B — Observable, reproducible back-action, with an EXACT closed form.**
The informational sector changes the physical statistics in a locally observable,
reproducible way. The headline, verified to 2×10⁻¹⁶ across 16 (c,ε) points:

```
D_B(INFO, c, ε) = |c| · sin²(ε)        [trace distance of Bob's local state]
```

(i.e. Bob's Bloch vector stays on the x-axis with x-component = c·cos 2ε). The
joint A-B state also changes, D_AB = O(ε) (D_AB/ε → 1.0). The Bob back-action is
a **second-order ("virtual") process**: because 𝓘 starts in |0⟩ (a Z eigenstate),
[Z_𝓘, |0⟩⟨0|] = 0 kills the first order, so D_B = |c|ε² + O(ε⁴) (D_B/ε² → |c| as
ε→0, verified). This is the back-action the reweighting was *supposed* to give —
now delivered by a legitimate CPTP evolution instead of a signaling post-hoc map.

**Result C — The informational (nonlocal) signature: local ≠ joint.**
Discriminate the two couplings by the back-action on the **remote** party B (the
party H_int reaches only *through* A, via Z_A Z_B):

| coupling | back-action on B (the remote party) |
|---|---|
| GEN = Z_A I_B Z_I (local) | **D_B = 0** for ALL c and ALL ε — a local coupling never touches B; Bob's state is EXACTLY invariant (max over all c,ε = 5.6×10⁻¹⁷) |
| INFO = Z_A Z_B Z_I (joint) | **D_B = |c|·sin²ε** — a nontrivial function of the JOINT-state coherence c; even in c; zero at c = 0 (D_B(c=0) = 5.6×10⁻¹⁷) |

*The structural property ordinary (local) environmental noise lacks:* a coupling
to a **joint observable** produces a back-action on the remote party that a
**local** coupling cannot (D_B = 0). The informational sector, coupled to a joint
observable, reaches *both* parties, and the back-action is set by the joint state's
coherence — not by either local state alone (B's local state is not what varies the
back-action; it is the A-B single-flip coherence c).

**Synthesis.** Reweighting (rounds 4–6): P′ ∝ P·e^{εF}, a post-hoc *non*-CPTP map
on measured branches → it signaled (the general no-go). The P⊗I auxiliary model: a
joint unitary is CPTP → it does **not** signal (A), while carrying an **observable**
back-action (B) that is **informational/nonlocal** (C). "Dual Field" = an actual
second dynamical sector coupled to a joint observable — not "ordinary physics + an
informational score." This is the first construction in which an informational
degree of freedom couples to quantum matter **nontrivially, observably, and
without violating no-signaling** — the survival question the review posed, answered
"yes" in one concrete construction.

**Honest limits + the open question this toy sharpens.** The closed form
D_B = |c|sin²ε is exact *for this coupling and this initial-state family*; it is a
demonstration, not a theorem over all H_int. The load-bearing open question
(next step): **is coupling 𝓘 to the JOINT observable (Z_A Z_B rather than Z_A) the
structural property that lets the back-action reach the remote party, or can a
generic H_int (a random 8-D Hermitian, or a local coupling with 𝓘 in a
superposition) reproduce the c-dependent back-action on B?** If every interesting
H_int just looks like an ordinary hidden environment (local, or a trivial
reparameterization of it), that is a *useful* failure (Dual Field → ordinary extra
field). If the joint-observable coupling is what's required, that **locates the
real novelty**: the informational sector must couple to a *correlational* property
of the physical system — a genuine "second field" with no single-particle home.
(Also open: can the back-action be made *informational* in the stronger sense —
dependent on the mutual information / causal organization of A-B — rather than on
a fixed joint-observable amplitude c?)

### 3i. Round 7 — the auxiliary model's *interpretation* fails in three ways; the honest A↔I↔B model (2026-11-22, the review's commit #3)

The round-7 review (`~/feedback_quantum_aux`) ran the §3h toy and confirmed every
asserted closed form passes to machine precision, but found the **interpretation**
fails in three load-bearing ways. Each was independently re-verified to ~10⁻¹⁶
(PART A of `dual_field_quantum_auxiliary2.py`):

1. **𝓘 was a spectator eigenstate.** With `H_INFO = Z_A Z_B Z_𝓘` and 𝓘
   initialized to \|0⟩ (a +1 eigenstate of Z_𝓘), Z_𝓘\|0⟩ = \|0⟩, so
   e^{−iε Z_A Z_B Z_𝓘}(\|ψ⟩_AB ⊗ \|0⟩) = (e^{−iε Z_A Z_B}\|ψ⟩_AB) ⊗ \|0⟩. The
   auxiliary qubit **never leaves \|0⟩** (ρ_𝓘(ε) = \|0⟩⟨0\| for all c,ε) and the
   model quietly reduces to the **direct** two-qubit interaction
   U_AB = e^{−iε Z_A Z_B}. "Coupling 𝓘 to a joint observable" was, in fact, "a
   direct A-B interaction with a passive spectator."
2. **The no-signaling test was a tautology.** Global CPTP ≠ no-signaling (a SWAP or
   CNOT is unitary + CPTP and transmits information). §3h's Δ_B (Bob's P(b=0) under
   Alice's X- vs Z-basis, *summed over Alice outcomes*) is 0 for **any** state ρ′,
   because ∑_a P_a^(x) = I_A for any complete basis: it tests measurement
   **completeness**, not no-signaling (verified 0 on 40 random states). The *correct*
   test — Alice encodes *before* the interaction, Bob reads *after* — gives
   **D = \|sin 2ε\|** for the reduced Z_A Z_B, i.e. Alice **can** signal. §3h's Part A
   was blind to it.
3. **c was locally visible, not joint-only.** §3h's ρ_c = ¼(I + X_A X_B) +
   (c/4)(I_A X_B + X_A I_B) has partial traces ρ_A = ρ_B = ½(I + c X), so
   ⟨X_A⟩ = ⟨X_B⟩ = c. c is directly measurable from **either** local qubit; D_B =
   |c|sin²ε was proportional to Bob's **local** initial X-polarization, not to an
   inaccessible joint coherence.

**Verdict:** the numerics were right, the interpretation was wrong, and the
auxiliary-**sector** strategy itself is still alive. The review specified the clean
next model: **A ↔ 𝓘 ↔ B, no direct A-B term; 𝓘 genuinely changing state; initial
A-B states with identical local marginals but different joint structure** — and asked
to test three things separately. That is `dual_field_quantum_auxiliary2.py`:

- **Model.** 𝓘 coupled via `H_int = (Z_A + Z_B) X_𝓘 = Z_A X_𝓘 + Z_B X_𝓘` — a
  sum of an A-𝓘 term and a B-𝓘 term only, **no A-B term**. Because 𝓘 is coupled
  by **X_𝓘** (not Z_𝓘) and [X_𝓘,\|0⟩⟨0\|] ≠ 0, 𝓘 **genuinely participates**
  (it evolves and entangles with AB) — the direct fix for bug #1. Initial A-B state:
  the \|00⟩-\\|11⟩ coherent family ρ_θ = ½(\|00⟩⟨00\|+\|11⟩⟨11\|) +
  (θ/2)(\|00⟩⟨11\|+\|11⟩⟨00\|), θ∈[0,1] (θ=1 → \|Φ⁺⟩). **Every member has
  ρ_A = ρ_B = I/2** (all six local observables ⟨X⟩,⟨Y⟩,⟨Z⟩ on A and B are 0): the
  only thing that varies with θ is the **joint** \|00⟩-\\|11⟩ coherence, invisible in
  either local state. (Mechanically, U(ε) only acts on the (Z_A+Z_B)=±2 eigenspace
  (|00⟩,|11⟩) and leaves the =0 eigenspace (|01⟩,|10⟩) untouched: it is an
  environment that dephases AB in the (Z_A+Z_B) eigenbasis, which yields the exact
  closed forms below.)

The three questions, each with a pre-registered closed form hard-asserted to machine
precision (numpy only, exit 0):

- **(Q1) Does 𝓘 really participate?  YES.**
  **ρ_𝓘^final = diag(cos²2ε, sin²2ε)** (exact and **θ-independent**);
  **S(ρ_𝓘) = h(cos²2ε) > 0** for ε ≠ 0 (h = binary entropy). 𝓘 changes state and
  entangles with AB (θ > 0). This is the fix for the spectator bug.
- **(Q2) Can Alice signal through it, and at what causal timescale?** The reduced
  A-B map (trace out 𝓘) is **CPTP** → a legitimate physical channel on AB → **no
  automatic FTL** (the Simon-Buzek-Gisin fence in the *correct* form, not a
  global-CPTP tautology). Its A→B action: the **joint** \|00⟩⟨11\| coherence is
  **dephased by a factor cos(4ε)** (exact: \|00⟩⟨11\|_final = (θ/2)cos 4ε) — the
  A→B imprint on the joint structure propagates through 𝓘 with amplitude cos 4ε,
  controlled by ε = the causal timescale. And **Bob's local state is invariant**
  (ρ_B^final = I/2 for all θ,ε): the 𝓘-mediated influence is *entirely in the joint
  structure*, so there is **no LOCAL A→B signal** (consistent with the no direct A-B
  term). Alice can imprint on the joint A-B state; the 𝓘-mediated channel then
  dephases that imprint by cos 4ε.
- **(Q3) Does its response distinguish JOINT information when all local observables
  are held fixed?  YES.**
  **D_AB(θ, ε) = (θ/2)·|1 − cos(4ε)|** (exact, to 3×10⁻¹⁶) — a nontrivial function
  of the **joint** \|00⟩-\\|11⟩ coherence θ while every local observable is held
  fixed (marginals = I/2). The crisp contrast: θ = 0 (the classical mixture
  ½(\|00⟩⟨00\|+\|11⟩⟨11\|)) and θ = 1 (\|Φ⁺⟩) have **identical marginals** (both
  I/2) but **D_AB(θ=0) = 0 vs D_AB(θ=1) = ½|1−cos 4ε| ≈ 0.971** (ε = 0.7). The
  back-action on the physical system depends on **joint information** (θ) that is
  invisible in any local observable — the corrected informational signature (v1 faked
  it with a locally-visible c; here it is provably joint-only).

**Honest limits + the open question this round sharpens.** The closed forms are exact
*for this coupling* H_int = (Z_A+Z_B) X_𝓘 *and this initial-state family* (the
\|00⟩-\\|11⟩ coherent subfamily); the 𝓘-mediated channel is a **dephasing** in the
(Z_A+Z_B) eigenbasis (a specific CPTP map). The load-bearing open question (next
step): **does a GENERIC A↔𝓘↔B coupling (adding X_A, X_B, Y terms, or a different
mediator state) reproduce the "response depends on joint information with the
marginals fixed" property, or is it specific to the Z-structure coupling?**
Equivalently: is **dephasing in a joint observable the generic back-action** an
auxiliary sector can have on the physical system, or can other CPTP structures
(amplitude damping, etc.) arise from A↔𝓘↔B couplings? If only dephasing-in-a-joint-
observable survives, that **locates the novelty** precisely: the informational sector
acts on the physical system *only* through its correlational (joint) degrees of
freedom — a genuine "second field" with no single-particle home.

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
4. **A/B fork diagnostic (2026-11-21, `psychedelic-ab-fork-note.md` +
   `dual_field_toy_2layer.py`): psychedelic phenomenology tracks the description
   layer (B).** LSD (5-HT2A → entorhinal disconnection) and ketamine (NMDA
   antagonism → thalamocortical gating) hold the substrate ~fixed and retune the
   generative model; the experienced "reality" tracks the model parameters, not
   the substrate → reality-as-experienced is a **B-object** (generative/description
   layer). **Under the stated experience assumption**, the depth4 D_causal/D_min
   fork therefore **leans D_min (B)** for the experience-relevant branch. The
   2-layer toy (fixed 1st-order chain = layer A, D_causal=N; BSC gate γ = layer B)
   verifies the pre-registered closed forms (I=1−h(γ), ρ_Y(k)=ρ_X^k(1−2γ)²,
   H_1(Y)=h((1+ρ_X(1−2γ)²)/2); all 13 γ rows PASS) and shows A invariant / B
   freely parameterized. Empirical (ROUND-4 CORRECTED metrics — the 2026-11-21
   external review caught that H_rate was the 1-step conditional H_1, not the
   hidden-Markov entropy rate, and that the old ξ metric was a 1st-order
   extrapolation; the toy now reports H_∞ via a Bayes filter): the experienced
   correlation amplitude is ×(1−2γ)² (1/e memory scale 49.5→27.4 at γ=0.1,
   absent for γ∈(0.19,0.81)) while the long-lag DECAY RATE is invariant — the
   substrate's time is HIDDEN, not destroyed; H_∞ = 0.534 at γ=0.1 (∩-shape
   survives, magnitudes corrected); γ=1 retains I≈1 under an inverted mapping
   (by construction — I/ρ/H/zlib are invariant under symbol relabeling: the
   measures are BLIND to representation, "alienness" = a fourth quantity);
   γ=0.5 = maximally incompressible but white-noise structure (the S/D fork
   maximized at the experience layer). Review record + claim-status table:
   `psychedelic-ab-fork-note.md` §9. Status: **analogical/structural, not a
   proof** — it constrains the A/B choice under the experience assumption and is
   silent on the substrate ontology by design. Andrey's call on the fork is still
   pending.
5. **`depth3` (DONE, 2026-08-25): the "I = depth" functional is not a clean new
   degree of freedom.** The strict question (can two processes have MATCHED ordinary
   statistics but radically different *irreducible* generation cost?) has a **no**:
   the *irreducible* (shortcut-free) cost is a function of P_phys (the dynamic), so
   matched statistics ⇒ matched irreducible cost — the counterexample attempt fails
   (`dual_field_toy_depth3.py`). Only *cancelling* (output-invisible) computation
   changes the *total* (non-irreducible) size, not the irreducible cost. The
   per-history form "I[H] = logical depth(H)" is a valid per-history functional but
   is GLOBAL (variance catastrophe) and UNCOMPUTABLE in general; its average over
   P_phys is still fixed by P_phys. **Consequence:** don't pursue "I = depth" as a
   *general* functional. The distinctive, TESTABLE version is the **amplification
   experiment** (branch probability vs the *future* depth of continuations) — a
   specific global effect, to be built with the **true** Doob h-transform (tilted
   operator + dominant-eigenvector factor r_ε(y)/r_ε(x)) / cloning population
   dynamics, computing its (J, I, Sdot) signature. That is the depth thread worth
   continuing.
6. **Two-qubit no-signaling check (round-4 program-level priority, 2026-11-21,
   proposed in the external review, Claude) — DONE 2026-11-21, result in §3f.**
   The reweighting on |Φ⁺⟩: Alice-local and joint/future F's LEAK (Δ_B ~ ε/4,
   ε/8 — O(ε) signaling through the entanglement); the Bob-local F SURVIVES to
   all orders (factorization). The dichotomy: observable ε in an entangled
   scenario + downstream-informational F ⇒ signaling, unless the reweighting
   acts on the measurement-free history ensemble — in which case ε is
   observationally invisible there. FOLLOW-UP (the "ask why"): characterize the
   all-orders no-leak family (first order = one linear constraint on the 8
   components of F; conjecture: Bob-local) and generalize the scenario (other
   states/bases/dimensions). The claim-status table in
   `psychedelic-ab-fork-note.md` §9 (verified / artifact / tautology /
   interpretation / prediction) is the standing ledger for the program.

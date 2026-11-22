# Dual-Field toy models — how to run

All scripts are self-contained and need only **numpy** (no matplotlib; plots are
ASCII).

```bash
python3 dual_field_toy.py           # 2-state model   (~30 s)
python3 dual_field_toy_3state.py    # 3-state motor   (~60 s, the N=1e6 power run is the slow part)
python3 dual_field_toy_ratchet.py   # driven ratchet  (~60 s) — symmetric drive: a control/negative result (J=0)
python3 dual_field_toy_chiral.py    # open problem (d) (~60 s) — a chiral (S-odd) I that DOES break the symmetry (J≈0.16·ε)
python3 dual_field_toy_2layer.py    # 2-layer substrate/experience (<5 s) — A fixed, B variable (the D_causal/D_min fork illustration)
python3 dual_field_quantum_nosignal.py  # two-qubit no-signaling v1 (<5 s, exact linear algebra) — does P'~P exp(eps F) leak across entanglement?
python3 dual_field_quantum_nosignal2.py # no-signaling v2 / round-5 (<5 s) — the full 2x2 square, the safe-family proposition, the scoped no-go theorem, the CPTP positive control
python3 dual_field_quantum_nosignal3.py # no-signaling v3 / the GENERAL no-go, round 6 (<5 s) — all states + full Bloch sphere; no-signaling for every state => F outcome-independent (P' = P); the |Phi+>-alone subtlety
```

## What each computes

Both implement the hypothesis locally per transition:
`P_DF(y|past) ∝ P_phys(y|past)·exp(ε·I)`, with `I` = excess predictive information
of the memory (past beyond the current state). `ε=0` recovers standard physics.

Each prints:
- **(a)** the steady-state population (2-state) / motor current (3-state) and the
  pre-registered residual `δ(ε) = observable(ε) − observable(0)`, with an O(ε)
  scaling check;
- **(b)** the entropy production `Sdot(ε)` and detailed-balance residual;
- **(b′)** the average dual-field information `I_avg(ε)` (the information-selection
  signature);
- **(c)** 3-state only: the TUR precision fraction `E = 2<J>²/(D·Sdot)` (must be ≤1);
- **(d)** min detectable ε at 95% confidence vs trajectory length N (statistical
  power).

`dual_field_toy_2layer.py` is a different kind of toy: it does NOT implement the
`P_DF ∝ P_phys·exp(ε·I)` reweighting. It is the 2-layer formalization behind
`../psychedelic-ab-fork-note.md` (the D_causal/D_min fork diagnostic). Layer A =
ONE realized trajectory of a 1st-order chain (P(stay)=0.99, ξ≈50; the "actual
causal history", D_causal=N, invariant). Layer B = a **bit-flip channel**
"gate" (BSC, crossover γ) on that trajectory (the formalization of entorhinal
disconnection; ROUND-4 FIX: the channel is a bit flip, NOT "replace by a random
bit" — that mechanism has effective crossover γ/2 and never reaches the mirror).
It verifies the closed forms `I(X;Y)=1−h(γ)`, `ρ_Y(k)=ρ_X^k(1−2γ)²` (amplitude
scaling; the DECAY RATE is invariant), `H_1(Y)=h((1+ρ_X(1−2γ)²)/2)` (the 1-step
conditional entropy — NOT the hidden-Markov entropy rate) empirically across γ,
reports the true entropy rate `H_∞` (Bayes filter; limits + γ↔1−γ symmetry
asserted), and the corrected 1/e persistence scale (49.5 → 27.4 at γ=0.1;
ABSENT for γ∈(0.19,0.81)); known-limit asserts: γ=0→Y≡H, γ=1→Y≡1−H, and the
(1−2γ)² amplitude flatness at lags 1–40. Shows A invariant / B freely
parameterized. Review record: `../psychedelic-ab-fork-note.md` §9.

`dual_field_quantum_nosignal.py` is the round-4 program-level test (README §3f):
the reweighting `P' ∝ P·exp(εF)` placed on the maximally-entangled state
|Φ⁺⟩=(|00⟩+|11⟩)/√2. Alice chooses her measurement basis (Z or X), Bob always
measures Z and never communicates; the branch is the full joint outcome
(a,i,b) and the reweighting acts on the branch probabilities (per-setup
normalization). The test is `Δ_B = TV(P'_B(·|X), P'_B(·|Z))` — a nonzero value
means Alice's basis choice leaked into Bob's marginal (signaling). Three F
classes are tested (Alice-local, Bob-local, joint/future). It is exact linear
algebra (projectors, partial traces, reweighting, marginalization) — no Monte
Carlo, no quantum hardware — and verifies the pre-registered closed forms to
8×10⁻¹⁷.

`dual_field_quantum_nosignal2.py` is the round-5 extension (README §3f,
2026-11-22), same exact-arithmetic machinery: (A) the full 2×2 no-signaling
square — Alice and Bob each with Z/X, BOTH directions, all three F classes,
every cell against a hand-derived closed form; (B) a CPTP positive control —
a local reset channel on Bob as dynamics (observable + no-signaling coexist);
(C) the product-state proposition — the exactly-safe family is the
setting-local factorization `w = s(a,x)·r(b,y)`, with the per-corner
factorization shown to leak; (D) the entangled-family no-go on the correlated
family |ψ_θ⟩ = cosθ|00⟩+sinθ|11⟩ — all-state no-signaling forces
`w = c(α,β)` (proof sketch in README §3f); (E) the to-first-order null space
of the tested square (16 F-values, 4 constraints, nullity 12). All hard
asserts; exit 0 = consistent.

`dual_field_quantum_nosignal3.py` is the round-6 GENERAL no-go (README §3g,
2026-11-22). It extends v2 from the scoped XZ-plane / correlated-family theorem
to the full 2×2 statement: **every** quantum state + **every** local projective
2-outcome setting (the full Bloch sphere, not just the XZ plane). The machinery
is exact (the joint law P(a,b|n,m) = ¼[1 + a·n·u + b·m·u + ab·n·T·m] with the
state's Bloch vectors u and correlation tensor T; no Monte Carlo, no hardware).
Parts: (A) a settings-only (outcome-independent) F is no-signaling-safe for
every state (P′ = P); (B) the Alice-local F1=(1+a)/2 leaks A→B on |Φ⁺⟩ with the
closed form ½·tanh(ε/2) (matches v2); (C) the **joint** outcome term e^{εkab}
is *exactly* no-signaling-safe for |Φ⁺⟩ (the key new subtlety — |Φ⁺⟩ alone does
NOT force F outcome-independent); (D) that same joint term leaks for |ψ_θ⟩,
θ≠π/4, with the hand-derived 2-point closed form A→B TV = |cos2θ|·tanh(εk)
(verified to 10⁻¹⁶ at θ = 0.2/0.3/0.5/0.7/1.0, vanishing exactly at θ=π/4);
(E) an all-θ sweep showing the correlated family (every θ ⊂ "every state") is
what kills the joint term — the leak is nonzero on both sides of θ=π/4 and
peaks near the product-state limit. All hard asserts; exit 0 = consistent.
Conclusion: no-signaling for every state ⟹ F is outcome-independent (P′ = P);
the reweighting architecture is killed for 2×2 (open: higher dimensions,
POVMs).

## Headline numbers (reference output)

- **2-state:** `δ(ε) = P_ε(x=1)−P_0(x=1) ≈ −0.035·ε`; `I_avg` rises monotonically
  with ε; `Sdot` has a sharp minimum (reversibility resonance) at ε*≈0.28.
- **3-state:** motor current `J₀≈0.235`; `δJ(ε) ≈ −0.003·ε`; `I_avg` rises
  monotonically; TUR satisfied (`E≤1`), with the field trading efficiency for
  information.
- **driven ratchet (control/negative):** a time-reversal-symmetric rocking drive
  gives **`J(ε)=0` for all ε** (to machine precision) — the information coupling
  does *not* rectify a symmetric drive (in a symmetric system `I` is itself
  symmetric, so amplifying it can't break the symmetry). `I_avg` still rises
  monotonically with ε (information selection survives, independent of current).
  A net current needs a geometry asymmetry → see the 3-state motor. (An earlier
  "J=0.0245→0.0293" reading was a convergence-bug artifact; fixed.)
- **chiral I (open problem (d)):** a *direction-dependent* (S-odd) information
  functional — chiral predictive information `I_chir = sgn(a→b)·log[P_phys/P_null]`
  — **does** break the symmetry of the symmetric drive and drives a current:
  `J ≈ 0.16·ε` (clean O(ε)), and **flipping the handedness flips the current**. A
  *neutral* (S-even) `I` gives J=0. So the dual field drives a current iff the
  information functional carries a handedness — the direction is an *input* to `I`,
  not an output (the Onsager–Casimir / reciprocity principle, made concrete).
- **2-layer substrate/experience (A fixed, B variable):** all three closed forms
  verified across 13 γ values (max deviation 0.17 tolerance units; known-limit
  asserts pass exactly). `I(γ)` and `ρ_Y(γ)` are U-shaped (min at 0.5);
  `H_rate(γ)` and the zlib compressibility are ∩-shaped (max at 0.5); the
  predicted γ↔1−γ mirror symmetry holds. The experienced correlation AMPLITUDE
  is ×(1−2γ)² — the 1/e memory scale runs 49.5→27.4 at γ=0.1 and is ABSENT for
  γ∈(0.19,0.81) — while the long-lag DECAY RATE is invariant (the substrate's
  time is hidden, not destroyed; the experience is a hidden-Markov process).
  `H_∞(γ=0.1) = 0.534` (Bayes filter; the old "H_rate" column was the 1-step
  conditional `H_1 = 0.694` — round-4 correction, note §9). At γ=1, `I≈1` is
  retained under an inverted mapping (zlib identical to γ=0) — **information
  retention ≠ perceptual stability** (by construction: I/ρ/H/zlib are invariant
  under symbol relabeling — the measures are blind to representation;
  "alienness" is the fourth quantity). At γ=0.5 the experience is maximally
  incompressible yet structurally white noise — the S/D fork maximized at the
  experience layer.
- **two-qubit no-signaling v1 (the first wall from existing physics,
  2026-11-21; verdicts corrected 2026-11-22):** on |Φ⁺⟩, reweighting the full
  joint branches by `exp(εF)`, Alice basis X vs Z, Bob fixed Z: **Alice-local F
  leaks** `Δ_B = ½·tanh(|ε|/2) ~ ε/4`; **joint/future F leaks**
  `Δ_B = |e^ε−1|/((3+e^ε)(1+e^ε)) ~ ε/8` (the `e^|ε|`-denominator form was
  wrong for ε<0 — round-5 fix); **Bob-local F survives to all orders IN THIS
  DIRECTION** (`Δ_B = 0`; `e^{εf(b)}` factors out of the sum over i) — but
  flips the direction and it leaks `Δ_A = ½·tanh(|ε|/2)` (round-5 fix; see v2).
  Closed forms verified to 8×10⁻¹⁷.
- **two-qubit no-signaling v2 (round-5 extension, 2026-11-22):** the FULL 2×2
  square (all 4 corners × 3 F classes × both directions): **NO
  outcome-referencing F survives** — each local F leaks in exactly the
  direction v1 never tested, the joint F leaks everywhere (12 cells vs
  hand-derived closed forms, 8×10⁻¹⁷). **Product-state proposition:** the
  exactly-safe family for product states is `w(a,b,x,y) = s(a,x)·r(b,y)` —
  each party's factor depends only on its own outcome AND its own setting
  (verified: safe family → machine 0 on 40 random product states; the
  per-corner factorization `e^{A(a,x,y)+B(b,x,y)}` leaks 40/40). **Entangled-
  family no-go theorem (scoped: 2×2, XZ plane, |ψ_θ⟩ = cosθ|00⟩+sinθ|11⟩):**
  all-state no-signaling (both directions, all θ) forces the weighting to be
  outcome-constant per corner, `w = c(α,β)` — i.e. `P′ = P`; the mechanism is
  the sinα term ∝ (w₊−w₋)·sinβ·sin2θ. **CPTP positive control:** a local
  reset-to-|1⟩ channel on Bob is observable (P(s_b=−1|Z): 0.5→1.0), CPTP
  (trace 1), and no-signaling (Δ = O(10⁻¹⁷)) — observability + no-signaling
  COEXIST; what fails is the branch-reweighting architecture. **First-order
  null space of the tested square:** 16 F-values, 4 independent first-order
  constraints, nullity 12; 200/200 random null-space members non-constant in
  the outcomes — the 4-corner test alone cannot prove triviality. Follow-up:
  generalize the theorem (all states / dimensions / POVMs); formulate the CPTP
  alternative architecture (README §3f).
- **two-qubit no-signaling v3 (the GENERAL no-go, round 6, 2026-11-22):** the
  full 2×2 statement — no-signaling (both directions) for **every** state and
  **every** local projective setting (full Bloch sphere) ⟹ F is
  outcome-independent (P′ = P). The load-bearing new result: the **joint**
  outcome term e^{εkab} is *exactly* no-signaling-safe for |Φ⁺⟩ (Δ = 5.6×10⁻¹⁷,
  both directions, all settings) — so |Φ⁺⟩ alone does NOT force triviality —
  but leaks for |ψ_θ⟩, θ≠π/4, with the closed form **A→B TV = |cos2θ|·tanh(εk)**
  (verified to 10⁻¹⁶; vanishes exactly at θ=π/4; peaks 0.758 near the
  product-state limit θ→0). e^{εkab} is not rank-1 (det = 2sinh2εk ≠ 0), so it
  is not in the round-5 product-safe family and leaks for some product states
  too (|0⟩⊗I/2: A→B = 3.8×10⁻¹). Hence the **all-entanglement** condition (the
  correlated family for every θ) kills the joint term, |Φ⁺⟩ kills the a/b local
  terms, and any outcome-dependent F (a {1,a,b,ab} sum) is trivialized. The
  "next cheap kill" from the round-6 review is done: universal branchwise
  exponential reweighting is incompatible with no-signaling except trivially
  (2×2; open: higher dimensions, POVMs).

Tweak the baseline physics at the top of each file (the `P1` table for the 2-state;
`BASE_CW / BASE_CCW / BASE_STAY / INERTIA` for the 3-state) to explore other
parameter regimes.

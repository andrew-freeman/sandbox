# Dual-Field toy models — how to run

Both scripts are self-contained and need only **numpy** (no matplotlib; plots are
ASCII).

```bash
python3 dual_field_toy.py           # 2-state model   (~30 s)
python3 dual_field_toy_3state.py    # 3-state motor   (~60 s, the N=1e6 power run is the slow part)
python3 dual_field_toy_ratchet.py   # driven ratchet  (~60 s) — symmetric drive: a control/negative result (J=0)
python3 dual_field_toy_chiral.py    # open problem (d) (~60 s) — a chiral (S-odd) I that DOES break the symmetry (J≈0.16·ε)
python3 dual_field_toy_2layer.py    # 2-layer substrate/experience (<5 s) — A fixed, B variable (the D_causal/D_min fork illustration)
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
causal history", D_causal=N, invariant). Layer B = a binary-symmetric-channel
"gate" γ on that trajectory (the formalization of entorhinal disconnection:
random input bleeds into the model with probability γ). It verifies the
closed forms `I(X;Y)=1−h(γ)`, `ρ_Y=ρ_X(1−2γ)²`,
`H_rate(Y)=h((1+ρ_X(1−2γ)²)/2)` empirically across γ, plus known-limit asserts
(γ=0→Y≡H, γ=1→Y≡1−H), and shows A invariant / B freely parameterized.

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
  predicted γ↔1−γ mirror symmetry holds. The experience's persistence ξ_Y
  collapses 48.7→2.2 at γ=0.1 — the substrate's long-range temporal structure
  dissolves at a *small* gate opening. At γ=1, `I≈1` is retained under an
  inverted mapping (zlib identical to γ=0) — **information retention ≠
  perceptual stability**. At γ=0.5 the experience is maximally incompressible
  yet structurally white noise — the S/D fork maximized at the experience layer.

Tweak the baseline physics at the top of each file (the `P1` table for the 2-state;
`BASE_CW / BASE_CCW / BASE_STAY / INERTIA` for the 3-state) to explore other
parameter regimes.

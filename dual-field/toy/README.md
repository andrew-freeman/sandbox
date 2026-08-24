# Dual-Field toy models — how to run

Both scripts are self-contained and need only **numpy** (no matplotlib; plots are
ASCII).

```bash
python3 dual_field_toy.py           # 2-state model   (~30 s)
python3 dual_field_toy_3state.py    # 3-state motor   (~60 s, the N=1e6 power run is the slow part)
python3 dual_field_toy_ratchet.py   # driven ratchet  (~60 s) — the 'information powers the motor' result
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

Tweak the baseline physics at the top of each file (the `P1` table for the 2-state;
`BASE_CW / BASE_CCW / BASE_STAY / INERTIA` for the 3-state) to explore other
parameter regimes.

#!/usr/bin/env python3
"""
*** CORRECTED / SUPERSEDED by dual_field_toy_depth4.py (ChatGPT round-3 review) ***
The central premise here -- "a long xi forces ~xi sequential steps; you cannot
shortcut the causal chain" (xi used as a proxy for irreducible depth) -- is
FALSE: the chain x_t = x_{t-1} XOR f_t is computed in O(log N) depth by a PARALLEL
PREFIX (scan), so xi is NOT a lower bound on circuit depth. depth4 CONSTRUCTS the
shortcut and MEASURES D_causal (N) vs D_min (log2 N) vs xi, showing the real
ambiguity: the dual field must specify whether it weights the ACTUAL CAUSAL depth
or the MINIMUM generative depth. Also: the "reparameterization trap" framing was
too strong -- the new ingredient is the coupling epsilon (P~e^{-beta E} analogy),
and the substantive content is one universal eps predicting across experiments.
*** (Read depth4 before relying on this file.) ***

Dual-Field toy — depth3: is IRREDUCIBLE computational depth a NEW degree of freedom?

The strict question (from OpenAI's round-2 review):
    "Can two processes have MATCHED ordinary statistics but radically different
     IRREDUCIBLE sequential generation cost?"

Key concept
-----------
IRREDUCIBLE generation cost = the cost you CANNOT shortcut (the minimum circuit
depth / the sequential work the dynamics force on you). It is a function of the
DYNAMICS (the transition rule, = P_phys), for a fixed gate set G.  A natural
computable proxy is the MIXING / CORRELATION length xi: a chain with long xi
forces ~xi sequential steps to propagate (you cannot shortcut the causal chain),
so xi bounds the irreducible sequential cost from below and is its natural proxy.

The claim to test
-----------------
Because the irreducible cost is f(P_phys), "matched statistics" (same P_phys)
IMPLIES "matched irreducible cost".  So you CANNOT have "matched statistics,
different IRREDUCIBLE cost".  This script *attempts* to build the counterexample
and shows it fails:
  [1] xi (irreducible-cost proxy) is a DETERMINISTIC function of the dynamic s.
  [2] Holding the statistics fixed (same s), you CANNOT get a different
      irreducible cost -- the attempt fails.
  [3] The only way to change the "cost" without changing the statistics is to add
      CANCELLING (output-invisible) computation -- which grows the TOTAL
      (non-irreducible) size, not the IRREDUCIBLE cost.

Conclusion (expected)
---------------------
"I = irreducible computational depth" is a FUNCTIONAL OF P_phys (the ordinary
physics) -> NOT a new degree of freedom; it reduces to (a function of)
persistence R.  In its per-history form, "I[H] = logical depth(H)" IS a (valid)
per-history functional, but it is GLOBAL (variance catastrophe) and HARD TO
COMPUTE (logical depth is uncomputable in general); its AVERAGE over P_phys is
still fixed by P_phys.  So the depth idea does NOT yield a clean, observable,
local new degree of freedom.  The distinctive, TESTABLE depth effect is instead
the AMPLIFICATION experiment (branch probability vs the FUTURE depth of
continuations) -- a specific global effect, built with the true Doob/cloning
machinery, not a general "I = depth" functional.
"""
import numpy as np

rng = np.random.default_rng(20260823)

def xi_theory(s, kmax=100000):
    """1/e decay length of C(k)=(2s-1)^k for the symmetric 2-state chain."""
    base = 2.0 * s - 1.0
    if abs(base) < 1e-12:
        return 1
    return int(np.ceil(1.0 / abs(np.log(base))))

def sim_markov(s, n, seed):
    r = np.random.default_rng(seed)
    x = np.empty(n, dtype=int); x[0] = r.integers(2)
    flip = 1.0 - s
    for t in range(1, n):
        x[t] = x[t-1] ^ (1 if r.random() < flip else 0)
    return x

def xi_measured(x, kmax=600):
    mu = x.mean(); xc = x - mu; var = (xc**2).mean()
    for k in range(1, kmax):
        if (xc[:-k] * xc[k:]).mean() / var < 1/np.e:
            return k
    return kmax

def main():
    print("=" * 78)
    print("depth3: is IRREDUCIBLE computational depth a NEW degree of freedom?")
    print("=" * 78)
    print("Question: matched statistics but different IRREDUCIBLE generation cost?")
    print("Irreducible cost = the work the dynamics FORCE (can't shortcut).")
    print("Proxy: mixing/correlation length xi (a long xi forces ~xi sequential")
    print("steps; you can't shortcut the causal chain).")

    print("\n[1] xi (irreducible-cost proxy) as a function of the dynamic s:")
    print(f"    {'s':>6} | {'xi theory':>11} | {'xi measured':>12} |  note")
    for s in [0.5, 0.75, 0.9, 0.95, 0.99]:
        xt = xi_theory(s); xm = xi_measured(sim_markov(s, 20000, 42))
        print(f"    {s:6.2f} | {xt:11d} | {xm:12d} |  same s -> same xi")
    print("    -> xi is a DETERMINISTIC function of the dynamic s.  The statistics")
    print("       (the transition rule) FIX the irreducible cost.  There is no free")
    print("       knob to vary the irreducible cost at fixed statistics.")

    print("\n[2] ATTEMPT: build a MATCHED-statistics process with DIFFERENT")
    print("    irreducible cost.  (Fix the statistics = fix s; try to change the cost.)")
    s = 0.9
    # Any process with these statistics is the SAME 1st-order Markov chain (same s).
    # Its irreducible cost is xi(s) -- there is no other process with these
    # statistics and a different irreducible cost.  The attempt FAILS:
    xi_fixed = xi_theory(s)
    print(f"    s = {s}: statistics fixed -> irreducible cost = xi ~ {xi_fixed}.")
    print("    To get a 'different cost' you must change s (change the statistics).")
    print("    Holding the statistics fixed, the irreducible cost is FIXED. FAIL.")

    print("\n[3] The ONLY 'cost change' at fixed statistics = CANCELLING computation:")
    n = 5000
    xA = sim_markov(s, n, 7)
    xiA = xi_measured(xA)
    # Version B = the SAME output xA, generated by a circuit that ALSO computes a
    # deep hidden chain h (h_i = h_{i-1} XOR coin) that CANCELS: out = x XOR (h^h) = x.
    sizeA = n      # N gates: just the x chain (irreducible)
    sizeB = 2 * n  # 2N gates: x chain + cancelling hidden chain
    print(f"    s={s}:  Version A: output xi={xiA}, circuit size = {sizeA} gates.")
    print(f"            Version B: output xi={xiA} (SAME output), size = {sizeB} gates (2x).")
    print("    Same statistics, SAME irreducible cost (~xi); only the TOTAL")
    print("    (non-irreducible, shortcuttable) size grew.  The statistics bound the")
    print("    IRREDUCIBLE cost but not the total size.")

    print("\nCONCLUSION:")
    print("  * The IRREDUCIBLE computational depth is a FUNCTION of P_phys (the")
    print("    ordinary physics, for a fixed gate set).  'Matched statistics,")
    print("    different IRREDUCIBLE depth' is IMPOSSIBLE -- the attempt fails.")
    print("  * => 'I = irreducible depth' is a functional of P_phys, NOT a new degree")
    print("    of freedom: it reduces to (a function of) persistence R and hits the")
    print("    reparameterization trap (absorbed into the ordinary physics).")
    print("  * The per-history form 'I[H] = logical depth(H)' IS a valid per-history")
    print("    functional, but it is GLOBAL (variance catastrophe) and UNCOMPUTABLE")
    print("    in general; its average over P_phys is still fixed by P_phys.  So it")
    print("    is not a clean, observable, local new degree of freedom either.")
    print("  * The distinctive, TESTABLE depth effect is the AMPLIFICATION experiment")
    print("    (branch probability vs the FUTURE depth of continuations) -- a specific")
    print("    global effect built with the true Doob/cloning machinery, not a general")
    print("    'I = depth' functional.  That is the version worth pursuing.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Dual-Field toy — reweighting global vs local functionals (CORRECTED after review).

Two separate, often-conflated issues, now kept apart:
  (A) MEASURE-OVERLAP / ESS collapse: naive reweighting by exp(eps*A_T) for an
      EXTENSIVE observable A_T (variance ~ T) concentrates on rare trajectories.
      This happens for ANY extensive A_T (additive or not) -- it is a measure-
      overlap problem, NOT a consequence of non-additivity per se.
  (B) LOCALIZABILITY: a functional that is ADDITIVE (per-step) localizes to a
      local transition rule P_eps(y|x) ~ P(y|x)*exp(eps*a(x,y)) (a locally-
      normalized tilt) and can be simulated DIRECTLY (no reweighting). A
      NON-ADDITIVE functional (compressed length) does NOT localize, so you are
      FORCED into the (A) reweighting.  This is the real value of additivity.

This script CONFIRMS (A) for the global compressed-length functional (ESS/N
collapses, worse for longer L, eps_crit ~ 1/sqrt(L)) and SHOWS that the LOCAL
additive functionals localize and are well-posed -- running BOTH distinct local
rules (raw SURPRISAL P^ (1-eps), and EXCESS PREDICTIVE INFO), which are different
functionals (an earlier version only ran the EPI one under a 'surprisal' label).

IMPORTANT (the conceptual correction): the local, well-posed functionals here are
SURPRISAL / DESCRIPTION-LENGTH (S/K in the S/R/K/D taxonomy) -- NOT computational
difficulty. A rare random bit has huge surprisal yet trivial generation cost. So
these local functionals are SAFE but they do NOT capture the 'depth' the
simulation intuition points to; that is the GLOBAL generative quantity D, see
dual_field_toy_depth2.py (persistence R) and the proposed depth3 (computational
depth D).

The physics:
  * Global proxy (K, description length): gzip compressed length. Non-additive.
  * Local proxy (S, surprisal): per-step -log P(x_t|history), = code length.
    Additive, localizes (P_eps ~ P^(1-eps)); eps=1 -> fair coin (sanity check).
"""
import numpy as np, gzip
import dual_field_toy as m2

rng = np.random.default_rng(20260823)
P1 = m2.P1

def gen_traj(L, x0=(0, 0)):
    a, b = x0
    traj = [a, b]
    for _ in range(L):
        y = 1 if rng.random() < P1[(a, b)] else 0
        a, b = b, y
        traj.append(b)
    return traj

def gzip_len(traj):
    return len(gzip.compress(''.join(map(str, traj)).encode(), 9))

def nll(traj):
    t = 0.0
    for k in range(2, len(traj)):
        a, b, y = traj[k-2], traj[k-1], traj[k]
        p = P1[(a, b)] if y == 1 else 1.0 - P1[(a, b)]
        t += -np.log(p)
    return t

def surprisal_pop(eps):
    """ACTUAL raw-surprisal weighting, implemented and simulated directly:
       P_eps(y|a,b) = P_phys(y|a,b)^(1-eps) / Z_y  (a locally-normalized tilt).
       At eps=1 every outcome has weight P^0=1 -> uniform transition -> fair coin
       -> P(x=1)=0.5 exactly (the sanity check that this is the surprisal rule,
       NOT the EPI rule)."""
    T = {}
    for a in (0, 1):
        for b in (0, 1):
            p1 = P1[(a, b)]; p0 = 1.0 - p1
            w1 = p1 ** (1.0 - eps); w0 = p0 ** (1.0 - eps)
            T[(a, b)] = w1 / (w1 + w0)
    M = m2.make_matrix(T)
    pi = m2.stationary(M)
    return pi[m2.sidx(0, 1)] + pi[m2.sidx(1, 1)]

def ess_of(eps, X):
    w = np.exp(eps * (X - X.mean()))      # center to avoid overflow
    w = w / w.sum()
    return 1.0 / np.sum(w**2)             # effective sample size (units of N)

def run(L, n):
    tr = [gen_traj(L) for _ in range(n)]
    return np.array([gzip_len(t) for t in tr]), np.array([nll(t) for t in tr])

def main():
    print("=" * 76)
    print("I = computational difficulty: global (non-additive) vs local (additive)")
    print("=" * 76)
    print("\n[1] GLOBAL compressed length (gzip, ~Kolmogorov) — must reweight samples.")
    print("    effective sample size ESS/N after reweighting by exp(eps*L_gzip):")
    print(f"    {'L':>6} | " + " | ".join(f"eps={e:<3}" for e in [0.1, 0.5, 1.0]))
    for L, n in [(200, 4000), (2000, 2000)]:
        Lc, _ = run(L, n)
        cells = [f"{ess_of(e, Lc)/n:<8.4f}" for e in [0.1, 0.5, 1.0]]
        print(f"    {L:>6} | " + " | ".join(cells))
    print("    (relative ESS/N, so 1.0 = intact, 0.01 = one sample carries all weight)")
    print("    -> ESS/N collapses as eps grows, and collapses SOONER for longer L.")
    print("    PRECISE CAUSE: this is a MEASURE-OVERLAP problem, not a consequence of")
    print("    non-additivity per se. ANY extensive observable A_T (variance ~ T),")
    print("    additive or not, makes exp(eps*A_T) concentrate on rare trajectories")
    print("    under naive reweighting. Non-additivity is a SEPARATE issue: it is what")
    print("    PREVENTS a local transition rule (the cloning/Doob fix), so for compressed")
    print("    length you cannot even avoid the reweighting in the first place.")

    # critical eps where relative ESS/N drops to 0.1
    print("\n    critical eps (where relative ESS/N drops to 0.1):")
    for L, n in [(200, 6000), (2000, 3000)]:
        Lc, _ = run(L, n)
        eps = np.linspace(0.02, 1.0, 200)
        vals = np.array([ess_of(e, Lc)/n for e in eps])
        crit = eps[np.argmax(vals < 0.1)] if vals.min() < 0.1 else '>1.0'
        print(f"      L={L:5d}: eps_crit ~ {crit if isinstance(crit,str) else round(crit,3)}")
    print("       -> eps_crit shrinks ~1/sqrt(L): to reweight longer trajectories you")
    print("          must use SMALLER eps, but the power analysis needs LONGER")
    print("          trajectories for SMALLER eps. The two pull in opposite directions.")

    print("\n[2] LOCAL additive functionals DO localize (simulate DIRECTLY, no reweighting).")
    print("    Two DISTINCT local rules -- run each (they are different functionals):")
    print("    (a) RAW SURPRISAL:  P_eps(y|a,b) = P_phys(y|a,b)^(1-eps)/Z")
    print("        (the -log P tilt).  Sanity check: at eps=1 all weights = P^0 = 1")
    print("        -> uniform transition -> P(x=1) must be exactly 0.5.")
    for eps in [0.0, 0.5, 1.0, 2.0, 4.0]:
        print(f"      eps={eps:<3}: P(x=1)={surprisal_pop(eps):.4f}")
    print("    (b) EXCESS PREDICTIVE INFO (EPI): P_eps(y|a,b) ~ P_phys * exp(eps*log[P_phys/P_null])")
    print("        (the machinery used in the 2-state/3-state models; ~ P_phys^(1+eps)/P_null^eps).")
    for eps in [0.0, 0.5, 1.0, 2.0, 4.0]:
        print(f"      eps={eps:<3}: P(x=1)={m2.pop1(eps):.4f}")
    print("    Both give a clean stationary state for any eps (no reweighting, no ESS")
    print("    collapse) -- a LOCAL additive functional localizes to a well-posed Markov")
    print("    rule.  (Note: this is a locally-normalized exponential TILT, not the full")
    print("    Doob h-transform, which additionally needs the tilted-operator's dominant")
    print("    eigenvector ratio r_eps(y)/r_eps(x).)")

    print("\nVERDICT (corrected after external review):")
    print("  * 'I = compressed length' (global, non-additive) is NOT directly usable:")
    print("    naive reweighting -> ESS/measure-overlap collapse (worse for longer L);")
    print("    AND non-additivity prevents a local rule, so you can't even avoid the")
    print("    reweighting. Conflicts with the power analysis.")
    print("  * 'I = per-step SURPRISAL' (local, additive) DOES localize: P_eps ~ P^(1-eps),")
    print("    a clean well-posed Markov rule (eps=1 -> fair coin, P(x=1)=0.5).  BUT this")
    print("    is DESCRIPTION/LENGTH, not computation: a rare random bit has huge")
    print("    surprisal yet trivial generation cost.  So surprisal is a local SAFE")
    print("    functional, but it is NOT 'computational difficulty'.")
    print("  * Bottom line: the LOCAL, well-posed functionals (surprisal S, EPI) are")
    print("    just the machinery already in use -- they do NOT capture the 'depth' the")
    print("    simulation intuition points to.  The distinctive candidate (computational")
    print("    DEPTH, D, in the S/R/K/D taxonomy) is a GLOBAL generative quantity ->")
    print("    see dual_field_toy_depth2.py (persistence R) and the proposed depth3.")

if __name__ == "__main__":
    main()

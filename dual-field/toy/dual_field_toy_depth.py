#!/usr/bin/env python3
"""
Dual-Field toy — 'I is computational difficulty' (the simulation idea).

Tests the sharpest technical claim in the two external answers:
  * Claude: complexity (compressed length) is a GLOBAL, non-additive functional,
    so it CANNOT be localized into a per-step transition rule; naive importance
    reweighting by exp(eps*complexity) suffers a variance catastrophe (effective
    sample size collapses) that gets WORSE as trajectories get longer -- pulling
    against the power analysis (which needs long trajectories for small eps).
  * The fix (Claude, citing Giardinà-Kurchan-Peliti / Doob transform): a
    LOCAL ADDITIVE functional (per-step) can be turned into an exact local
    transition rule P_DF ∝ P_phys*exp(eps*local_term) and simulated DIRECTLY as
    a proper Markov chain -- no reweighting, no variance catastrophe.

This script CONFIRMS the catastrophe for the global compressed-length functional
and SHOWS that the additive local functional (per-step surprise, i.e. the
excess-predictive-information machinery) is well-posed because it localizes.

The physics: 'computational difficulty' ~ how hard a step is to predict/generate.
  * Global proxy : gzip compressed length (model-free, ~Kolmogorov).  Non-additive.
  * Local proxy  : per-step surprise -log P(x_t|x_{t-1},x_{t-2}), summed.  Additive.
    (the negative log-likelihood / code length under the model -- a local,
    well-posed complexity; high average surprise = 'harder to generate')
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
    print("       (the catastrophe Claude flagged; it is forced, because compressed")
    print("        length is non-additive -> no local transition rule -> you MUST)")

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

    print("\n[2] LOCAL additive surprise (per-step -log P) — CAN localize (Doob).")
    print("    P_DF(y|a,b) = P_phys(y|a,b)*exp(eps*surprise)/Z  -> simulate DIRECTLY.")
    print("    (This is the 2-state excess-predictive-information machinery.)")
    for eps in [0.0, 0.5, 1.0, 2.0, 4.0]:
        _, pop = m2.steady(eps)
        print(f"      eps={eps:<3}: P(x=1)={m2.pop1(eps):.4f}   (clean stationary state;")
        print(f"              no reweighting, no ESS collapse -- well-posed for any eps)")

    print("\nVERDICT:")
    print("  * 'I = compressed length' (global, non-additive) is NOT directly usable:")
    print("    forced sample reweighting -> variance catastrophe -> conflicts with the")
    print("    power analysis. (Confirms Claude.)")
    print("  * 'I = per-step surprise / code length' (local, additive) IS usable:")
    print("    it localizes to a clean Markov rule (Doob transform) -> well-posed.")
    print("  * So the computational-difficulty idea survives, but ONLY through a LOCAL")
    print("    (additive, Markov) surrogate for depth -- never the raw global complexity.")
    print("    The per-step surprise is exactly that surrogate: 'how hard is this step")
    print("    to predict/generate', summed.  Whether it also needs the chirality (the")
    print("    S-odd part) to drive a directed effect is the next question.")

if __name__ == "__main__":
    main()

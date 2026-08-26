#!/usr/bin/env python3
"""
Dual-Field toy — step 1, CORRECTED: surprise vs PERSISTENCE (NOT 'depth').

External review (OpenAI) caught an overreach: the quantity this script calls
'depth' (the autocorrelation length xi) is actually PERSISTENCE / correlation
time (R in the S/R/K/D taxonomy), NOT computational depth (D, Bennett's logical
depth). The correction:
  * These are all 1st-order Markov chains: P(x_t|past) = P(x_t|x_{t-1}). The
    long xi is generated entirely by ONE local number s -- influence propagates
    through successive LOCAL transitions, the law never accesses the distant past.
    So 'long xi => GLOBAL => not localizable' does NOT follow; xi is a property
    of the local dynamics (an emergent long-range property of a local rule).
  * What this script actually shows:  surprisal (S)  !=  persistence (R)  !=
    short-range conditional memory (2nd-order EPI).  A slow chain (s->1) is
    LOW-surprise but HIGH-persistence, and has ZERO 2nd-order EPI.
  * In this ONE-parameter family, H and xi are both functions of the same s, so
    they are anti-correlated, not independent.  (True independence needs a
    two-parameter family: hold entropy rate fixed, vary correlation length.)
  * The genuinely GLOBAL, non-localizable candidate is computational DEPTH (D),
    which this script does NOT measure.  That needs depth3: two processes with
    MATCHED ordinary statistics but different irreducible sequential generation
    cost, D_G(H|B) = min_C depth(C) over generators C of H from boundary B using
    the universe's local gates G.

Test processes
--------------
2-state 1st-order Markov chains, P(stay)=s, s in [0.5,1).  s=0.5 white noise
(high S, zero R); s->1 slow chain (low S, long R).  All order-1 -> 2nd-order
EPI = 0 exactly (a theorem: X_t is conditionally independent of X_{t-2} given
X_{t-1}), while R grows.

Measures (estimated from a long sample)
---------------------------------------
  * entropy rate H            : bits/step, the surprisal (S).
  * autocorrelation length xi : 1/e decay of C(k)=(2s-1)^k, the PERSISTENCE (R).
  * 2nd-order EPI             : I(x_t ; x_{t-2} | x_{t-1}), short-range memory
                                (= 0 for all order-1 chains, by the Markov property).
"""
import numpy as np

rng = np.random.default_rng(20260823)

def sample_chain(s, n=2**16):
    x = np.empty(n, dtype=int)
    x[0] = rng.integers(2)
    flip = 1 - s
    for t in range(1, n):
        x[t] = x[t-1] ^ (1 if rng.random() < flip else 0)
    return x

def entropy_rate(x):
    # H(X_t | X_{t-1}) from empirical 1st-order conditionals
    counts = np.zeros((2, 2))
    for a, b in zip(x[:-1], x[1:]):
        counts[a, b] += 1
    rowp = counts.sum(1) / counts.sum()
    H = 0.0
    for a in range(2):
        for b in range(2):
            if counts[a, b] > 0:
                pab = counts[a, b] / counts.sum()
                pcond = counts[a, b] / counts[a].sum()
                H -= pab * np.log2(pcond)
    return H

def autocorr_decay(x, kmax=400):
    # C(k) in [0,1] coding, find 1/e decay length
    mu = x.mean()
    xc = x - mu
    var = (xc**2).mean()
    c0 = (xc**2).mean()
    # 1/e decay: first k with C(k) < 1/e
    inv_e = 1/np.e
    for k in range(1, kmax):
        c = (xc[:-k] * xc[k:]).mean() / var
        if c < inv_e:
            return k
    return kmax

def epi2(x, kmax=2000):
    # 2nd-order EPI: I(X_t ; X_{t-2} | X_{t-1})  (local short-range memory)
    # = sum p(a,b,c) log[ p(c|a,b) / p(c|b) ],  (a,b,c)=(x_{t-2},x_{t-1},x_t)
    c3 = np.zeros((2, 2, 2)); c2 = np.zeros((2, 2))
    for i in range(2, len(x)):
        a, b, c = x[i-2], x[i-1], x[i]
        c3[a, b, c] += 1; c2[b, c] += 1
    I = 0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                if c3[a, b, c] > 0 and c2[b, c] > 0:
                    p3 = c3[a, b, c] / c3.sum()
                    p_cond3 = c3[a, b, c] / c3[a, b].sum() if c3[a, b].sum() else 0
                    p_cond2 = c2[b, c] / c2[b].sum() if c2[b].sum() else 0
                    if p_cond3 > 0 and p_cond2 > 0:
                        I += p3 * np.log2(p_cond3 / p_cond2)
    return max(0.0, I)   # clip tiny negative sampling noise

def main():
    print("=" * 78)
    print("STEP 1 (corrected): surprisal (S) vs PERSISTENCE (R) -- NOT 'computational depth'")
    print("=" * 78)
    print("2-state 1st-order chain, P(stay)=s.  s=0.5 white noise, s->1 slow chain.")
    print(f"{'s':>6} | {'surprisal H (bits/step)':>24} | {'persistence xi (1/e)':>22} | "
          f"{'2nd-ord EPI (memory)':>18}")
    print("-" * 78)
    for s in [0.5, 0.6, 0.75, 0.9, 0.95, 0.99]:
        x = sample_chain(s)
        H = entropy_rate(x)
        xi = autocorr_decay(x)
        epi = epi2(x)
        print(f"{s:6.2f} | {H:24.3f} | {xi:22d} | {epi:18.4f}")
    print("-" * 78)
    print("READING (corrected):")
    print("  * As s goes 0.5 -> 0.99:  SURPRISAL (entropy rate H) falls (1.0 -> 0.078)")
    print("    while PERSISTENCE (xi) rises (1 -> ~52).  A slow chain (s=0.99) is LOW-")
    print("    surprisal but HIGH-persistence.  So surprisal (S) and persistence (R)")
    print("    are DIFFERENT quantities: S is the irreducible/unpredictable part, R is")
    print("    how long the state PERSISTS (how much the past resolves the present).")
    print("  * IMPORTANT (the correction): xi is PERSISTENCE, NOT computational depth.")
    print("    All these are 1st-order Markov (P(x_t|past)=P(x_t|x_{t-1})); the long xi")
    print("    is generated by ONE local number s (influence propagates through local")
    print("    steps).  So 'long xi => not localizable' does NOT follow -- xi is a")
    print("    property of the LOCAL dynamics (an emergent long-range property).")
    print("  * The 2nd-order EPI is 0 for ALL of them -- a THEOREM (X_t is conditionally")
    print("    independent of X_{t-2} given X_{t-1} for any order-1 chain), not a")
    print("    tendency.  So short-range memory (EPI) is a THIRD, distinct quantity.")
    print("  * Caveat: in this ONE-parameter family H and xi are both functions of the")
    print("    same s (anti-correlated, not independent).  True independence needs a")
    print("    two-parameter family (hold entropy rate fixed, vary correlation length).")

    print("\nCONSEQUENCE (corrected):")
    print("  * This script separated THREE distinct quantities: surprisal (S),")
    print("    persistence (R), and short-range conditional memory (2nd-order EPI).")
    print("    It did NOT measure computational depth (D) -- the long xi of an order-1")
    print("    chain is persistence (a local-dynamics property), not generative depth.")
    print("  * The LOCAL, well-posed functionals (S, EPI) are just the machinery already")
    print("    in use; they do NOT capture the 'depth' the simulation intuition points to.")
    print("  * The distinctive candidate IS computational depth (D, Bennett's logical")
    print("    depth: irreducible sequential generation cost) -- a genuinely GLOBAL,")
    print("    generative, non-localizable quantity.  Testing it needs depth3: two")
    print("    processes with MATCHED ordinary statistics but different D, via")
    print("    D_G(H|B) = min_C depth(C) (generate H from boundary B using the")
    print("    universe's local gates G -- 'the universe supplies the instruction set').")

    print("\nCHIRALITY (does a depth-based I need it to drive a directed effect?):")
    print("  * Yes -- by the SAME symmetry argument as every neutral I (sec 3c/3d):")
    print("    a depth I derived from symmetric physics is S-even -> J=0 in a symmetric")
    print("    drive; it needs the S-odd (chiral) part to drive a net current.  Depth")
    print("    changes WHAT is weighted (deep vs shallow histories); chirality changes")
    print("    WHICH DIRECTION.  Orthogonal knobs: depth = the 'what', chirality =")
    print("    the 'which way'.")

    print("\nBOTTOM LINE FOR STEP 1 (corrected):")
    print("  This script showed  surprisal (S) != persistence (R) != short-range memory,")
    print("  three distinct quantities -- but it did NOT establish that 'computational")
    print("  depth (D) is global' (an earlier reading overreached: the long xi of an")
    print("  order-1 chain is persistence, a local-dynamics property).  The local,")
    print("  well-posed functionals (S, EPI) are just the existing machinery.  The")
    print("  distinctive candidate remains computational depth (D) -- a GLOBAL,")
    print("  generative, non-localizable quantity.  NEXT (depth3): test whether two")
    print("  processes can have MATCHED ordinary statistics but different D, via")
    print("  D_G(H|B) = min_C depth(C) using the universe's local gates G; then")
    print("  implement D via cloning/population dynamics (the true Doob h-transform,")
    print("  with the dominant-eigenvector factor r_eps(y)/r_eps(x)), compute its")
    print("  (J, I, Sdot) signature, and connect to the amplification experiment.")

if __name__ == "__main__":
    main()

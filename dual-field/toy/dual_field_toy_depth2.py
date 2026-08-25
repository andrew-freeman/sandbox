#!/usr/bin/env python3
"""
Dual-Field toy — step 1 of 'I = computational depth': SEPARATE depth from
surprise, and find what the LOCAL machinery can (and cannot) see.

The question
------------
'I = computational difficulty/depth' needs an operational, testable 'depth'.
Two candidate axes that are easy to confuse:
  * SURPRISE  : how unpredictable each step is (entropy rate; local).
  * DEPTH     : how far the causal influence reaches (long causal chains; the
                autocorrelation / predictive-memory length).

The key thing to check FIRST: are they actually independent?  If a process can
have LOW surprise but HIGH depth, then 'depth' captures something a
surprise-based I misses (slow, structured processes), and it is a distinct
candidate for I.  If they're just the same axis, 'depth' adds nothing.

Then the harder question: is depth LOCAL?  The variance-catastrophe result says
a GLOBAL (non-additive) functional can't be implemented by the local/Doob
machinery.  Depth (long causal chains) is long-range by definition.  So we test
whether a bounded-window LOCAL functional (the 2nd-order excess predictive
information, my existing 'memory' I) can capture depth at all.

Test processes
--------------
2-state 1st-order Markov chains with self-transition probability s
  P(x_t = x_{t-1}) = s,  P(x_t != x_{t-1}) = 1 - s.
  s in [0.5, 1):  s=0.5 is white noise (high surprise, zero depth);
                  s -> 1 is a slow chain (low surprise, long causal reach).
This single knob sweeps the (surprise, depth) plane in the non-oscillatory
quadrant.  All are order-1, so the 2nd-order EPI (local short-range memory)
should be ~0 for all of them -- which is exactly the point: long-range depth
grows while the local memory functional stays flat.

Measures (all estimated from a long sample)
-------------------------------------------
  * entropy rate H        : bits/step, the surprise (local).
  * autocorrelation length xi : 1/e decay of C(k)=(2s-1)^k, the depth.
  * 2nd-order EPI         : I(x_t ; x_{t-2} | x_{t-1}), the LOCAL memory I.
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
    print("STEP 1: does 'depth' separate from 'surprise'?  What can the local see?")
    print("=" * 78)
    print("2-state 1st-order chain, P(stay)=s.  s=0.5 white noise, s->1 slow chain.")
    print(f"{'s':>6} | {'surprise H (bits/step)':>24} | {'depth xi (1/e decay)':>22} | "
          f"{'local 2nd-ord EPI':>18}")
    print("-" * 78)
    for s in [0.5, 0.6, 0.75, 0.9, 0.95, 0.99]:
        x = sample_chain(s)
        H = entropy_rate(x)
        xi = autocorr_decay(x)
        epi = epi2(x)
        print(f"{s:6.2f} | {H:24.3f} | {xi:22d} | {epi:18.4f}")
    print("-" * 78)
    print("READING:")
    print("  * As s goes 0.5 -> 0.99:  SURPRISE (entropy rate H) falls (1.0 -> 0.078)")
    print("    while DEPTH (xi, 'how far back the history matters') rises (1 -> ~52).")
    print("    They move in OPPOSITE directions.  A slow chain (s=0.99) is LOW-")
    print("    surprise but HIGH-depth.  So depth is NOT 'just surprise': it is the")
    print("    PREDICTABLE/STRUCTURED axis (how much the past RESOLVES the present),")
    print("    complementary to surprise (the irreducible, unpredictable part).  A")
    print("    surprise-based I calls the slow chain 'simple'; a depth-based I calls")
    print("    it 'deep' -- genuinely different functionals (opposite sign).")
    print("  * The LOCAL 2nd-order EPI is ~0 for ALL of them (they're all order-1):")
    print("    it measures only SHORT-RANGE (order-2) memory, NOT the overall depth")
    print("    xi.  A slow chain has long xi but zero 2nd-order EPI -> the bounded-")
    print("    window local functional CANNOT see the long-range depth.")

    print("\nCONSEQUENCE (the boundary, made precise):")
    print("  * 'short-range memory' (order k): LOCAL -> Doob-transformable -> well-posed.")
    print("    (This is the I I've used all along; it modulates currents, needs a")
    print("    ratchet for a net current, and needs chirality for a symmetric drive.)")
    print("  * 'long-range depth' (xi -> large): GLOBAL (needs the whole history) ->")
    print("    NOT localizable -> hits the variance catastrophe (dual_field_toy_depth.py).")
    print("  * So 'I = computational depth' in the DEEP (long-causal-chain) sense is a")
    print("    GLOBAL hypothesis: it is the same class as the amplification experiment")
    print("    (branch probability depends on the FUTURE depth of the continuations),")
    print("    NOT a local one.  It is simulable only by global methods (cloning /")
    print("    population dynamics), and it is the distinctive, hardest-to-mimic")
    print("    signature -- precisely because it cannot be a local reparameterization.")

    print("\nCHIRALITY (does a depth-based I need it to drive a directed effect?):")
    print("  * Yes -- by the SAME symmetry argument as every neutral I (sec 3c/3d):")
    print("    a depth I derived from symmetric physics is S-even -> J=0 in a symmetric")
    print("    drive; it needs the S-odd (chiral) part to drive a net current.  Depth")
    print("    changes WHAT is selected (deep vs shallow histories); chirality changes")
    print("    WHICH DIRECTION.  They are orthogonal knobs: depth = the 'what',")
    print("    chirality = the 'which way'.")

    print("\nBOTTOM LINE FOR STEP 1:")
    print("  'depth' separates cleanly from 'surprise' (it is the complementary,")
    print("  predictable/structured axis).  But it is, in general, GLOBAL, not local:")
    print("  the local/Markov machinery captures only the short-range (order-k) special")
    print("  case (the order-k EPI I've used all along).  So 'I = computational depth'")
    print("  is a GLOBAL dual-field hypothesis -- harder to simulate (variance")
    print("  catastrophe) but more distinctive (it cannot be a local reparameterization).")
    print("  NEXT: implement the GLOBAL version properly via the cloning / Doob")
    print("  population-dynamics method (not naive reweighting), compute its (J, I, Sdot)")
    print("  signature, and connect to the amplification experiment.")

if __name__ == "__main__":
    main()

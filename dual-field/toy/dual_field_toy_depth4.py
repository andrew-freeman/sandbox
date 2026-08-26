#!/usr/bin/env python3
"""
Dual-Field toy — depth4: CONSTRUCT the actual shortcut (ChatGPT round-3 review).

depth3's ERROR: it used the correlation length xi as a proxy for 'irreducible
computational depth', assuming 'a long xi forces ~xi sequential steps; you
cannot shortcut the causal chain.' That is FALSE in general. The persistent
chain  x_t = x_{t-1} XOR f_t  (f_t independent) satisfies
    x_t = x_0 XOR f_1 XOR ... XOR f_t,
which a PARALLEL PREFIX (scan) computes in O(log N) depth, not O(N). So xi is
NOT a lower bound on computational circuit depth.

depth4 therefore does NOT argue -- it CONSTRUCTS both realizations of the SAME
trajectory and MEASURES each one's circuit depth (the number of sequential /
parallel steps, = the circuit's critical path):

  A) SEQUENTIAL (streaming -- how the universe actually propagates it):
         x_t = x_{t-1} XOR f_t, one step at a time.   depth = N.
         This is the ACTUAL CAUSAL DEPTH, D_causal.
  B) PARALLEL PREFIX (batch -- the shallowest circuit that reproduces it):
         x_t = x_0 XOR (f_1..f_t), via a Hillis-Steele XOR scan.  depth = log2(N).
         This is the MINIMUM GENERATIVE DEPTH, D_min (Bennett's neighborhood).

  Both realizations produce the IDENTICAL trajectory (verified below), hence the
  SAME statistics.  The correlation length xi is a THIRD, independent quantity.

RESULT (expected):  D_causal (N)  !=  D_min (log2 N)  !=  xi.
Three distinct quantities for the SAME trajectory.  This is the 'depth of WHAT?'
fork: the dual field is DIFFERENT physics under choice (A) vs (B) (they differ by
a factor N/log N), so 'I = depth' is undefined until that fork is settled.

Note (ChatGPT): D_min also needs Bennett's delta-restriction to avoid the
print(H) cheat -- only count programs near the shortest description, |p|<=K(H)+d.
"""
import numpy as np
import math

def gen_flip_bits(N, p_flip, seed):
    """f_1..f_N, independent Bernoulli(p_flip).  s = P(stay) = 1 - p_flip."""
    return (np.random.default_rng(seed).random(N) < p_flip).astype(int)

def sequential_realize(f, x0):
    """A: x_t = x_{t-1} XOR f_t, step by step (streaming). depth = N (a chain)."""
    x = [x0]
    for ft in f:
        x.append(x[-1] ^ ft)
    return x, len(f)            # trajectory, depth

def parallel_realize(f, x0):
    """B: x_t = x0 XOR (f_1..f_t) via Hillis-Steele inclusive XOR scan (batch).
    Each scan 'offset' is one parallel layer; there are log2(N) of them."""
    N = len(f)
    M = 1
    while M < N:
        M *= 2
    a = list(f) + [0] * (M - N)
    depth = 0
    offset = 1
    while offset < M:
        b = a[:]
        for i in range(offset, M):
            b[i] = a[i] ^ a[i - offset]
        a = b
        offset *= 2
        depth += 1
    # inclusive scan: a[i] = XOR of f_1..f_{i+1};  x_t = x0 XOR a[t-1]
    x = [x0] + [x0 ^ a[t - 1] for t in range(1, N + 1)]
    return x, depth             # trajectory, depth

def correlation_length(x, kmax=800):
    mu = np.mean(x); xc = x - mu; var = (xc**2).mean()
    for k in range(1, kmax):
        if (xc[:-k] * xc[k:]).mean() / var < 1.0 / math.e:
            return k
    return kmax

def main():
    print("=" * 76)
    print("depth4: CONSTRUCT the shortcut -- D_causal vs D_min vs correlation length")
    print("=" * 76)
    print("ONE trajectory, TWO realizations, MEASURED circuit depth (critical path):")
    print("  A) sequential / streaming (the universe's way): x_t = x_{t-1} XOR f_t")
    print("  B) parallel prefix / batch (shallowest circuit): x_t = x_0 XOR f_1..f_t")
    print("     (Hillis-Steele XOR scan).  s = P(stay) = 0.99 -> xi ~ 50.")
    print()
    print(f"    {'N':>7} | {'D_causal (A)':>14} | {'D_min (B)':>11} | {'xi':>4} | "
          f"{'A==B?':>6} | {'A/ B ratio':>11}")
    for N in [64, 256, 1024, 4096, 65536]:
        f = gen_flip_bits(N, p_flip=0.01, seed=42)
        xA, dA = sequential_realize(f, 0)
        xB, dB = parallel_realize(f, 0)
        same = (xA == xB)
        xi = correlation_length(xA)
        print(f"    {N:>7} | {dA:>14} | {dB:>11} | {xi:>4} | {str(same):>6} | "
              f"{dA/dB:>11.1f}")
    print()
    print("READING (measured, not asserted):")
    print("  * The two realizations give the IDENTICAL trajectory (A==B True), so the")
    print("    statistics are the same.  But their circuit depths differ drastically:")
    print("    D_causal (sequential) = N;  D_min (parallel prefix) = log2(N).")
    print("  * xi (~50) is a THIRD quantity, and it is NOT a lower bound on the depth:")
    print("    for N=65536, D_min = 16 < xi ~ 50 -- the shallow circuit is SHORTER than")
    print("    the correlation length.  depth3's 'xi forces the depth' premise fails.")
    print("  * D_causal / D_min = N / log2(N) -> grows without bound (the fork widens).")
    print()
    print("THE FORK (which depth does the dual field weight?):")
    print("  (A) ACTUAL CAUSAL DEPTH  D_causal = N : how the universe ACTUALLY")
    print("      propagates (streaming, step by step) -- a property of what HAPPENED.")
    print("  (B) MINIMUM GENERATIVE DEPTH  D_min = log2 N : the SHALLOWEST circuit")
    print("      that reproduces the trajectory (shortcuts allowed) -- Bennett's")
    print("      logical-depth neighborhood (with the delta-restriction against")
    print("      print(H)).")
    print("  Choosing (A) vs (B) gives DIFFERENT physics (different I[H], different")
    print("  predictions), so 'I = depth' is UNDEFINED until the fork is settled.")
    print()
    print("NEXT: decide (A) vs (B) on physical grounds (is the dual field a property")
    print("of the actual causal history, or of the space of laws that could have")
    print("produced it?), then re-derive the (J,I,Sdot) signature for the chosen depth.")

if __name__ == "__main__":
    main()

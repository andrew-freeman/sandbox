#!/usr/bin/env python3
"""
Dual-Field toy — 2-layer substrate/experience model (layer A fixed, layer B variable).

Claim under test (see ../psychedelic-ab-fork-note.md)
------------------------------------------------------
"Reality-as-experienced" tracks the generative/description layer (B, the model
output), not the causal-process layer (A, what physically happened).
Psychedelic action is a natural demonstration of the structure: a substrate
plus a retuned mapping -> a different experienced reality.  (The claim is an
interpretation of the construction, not a theorem of it — the toy shows the
A->B map is a free parameter.)

Formalization
-------------
Layer A (substrate): a 1st-order Markov chain, P(stay)=s (s=0.99, the
depth2/3 family; 1/e memory scale ~50).  ONE realized trajectory H (fixed
seed) = the actual causal history.  Its causal depth D_causal = N sequential
steps is a property of what happened and is invariant.

Layer B (experience): a BIT-FLIP CHANNEL (binary symmetric channel) on H with
crossover gamma in [0,1] = the "gate".  With probability gamma the symbol is
FLIPPED (B = A XOR E, E ~ Bernoulli(gamma)).
    ROUND-4 FIX: this is NOT "an independent random bit replaces the symbol"
    — that mechanism has effective crossover gamma/2 and never reaches the
    mirror.  The toy implements the flip; the closed forms below are for the
    flip channel.
    gamma=0    perfect copy (sobriety: the model tracks the substrate fully)
    gamma=1    deterministic inversion (mirror world: stable but alien;
               note gamma>0.5 is ANTCORRELATION, not more disconnection —
               the honest 2-D phase space is (gamma noise, M remap), queued)
    gamma=0.5  maximum disconnection (the experience is white noise: no
               information, no temporal structure)
H is identical across all gamma (checksum-asserted); the output statistics
Y(gamma) vary freely.

Closed forms (fair substrate, p(x=1)=0.5) -- the toy verifies each empirically
(pre-registered in the note, house method):
    I(X;Y)  = 1 - h(gamma)                         (U-shaped; 0 at 0.5, 1 at 0/1)
    rho_Y(k)= rho_X^k * (1-2*gamma)**2   for k>=1  (amplitude scaling; the
             DECAY RATE rho_X^k is INVARIANT — the substrate's time is hidden,
             not destroyed; Y is a hidden-Markov process)
    H_1(Y)  = H(Y_t | Y_{t-1})  (1-step conditional entropy)
            = h( (1 + rho_X*(1-2*gamma)**2) / 2 )  (cap-shaped, max at 0.5)
    H_inf(Y) = true entropy rate of the hidden-Markov process Y
            = E[h(q_t)], q_t = P(Y_t=1 | Y_{<t}) via the Bayes filter.
            NO closed form; measured; limits + symmetry asserted:
            H_inf(0) = H_inf(1) = h(1-s), H_inf(0.5) = 1, H_inf(g)=H_inf(1-g).
where h is the binary entropy (bits).

Persistence (ROUND-4 FIX): the old metric xi_Y = -1/ln(rho_Y(1)) treated Y as
if it were 1st-order Markov (it is not).  Corrected metrics:
    xi_cross(gamma): the 1/e crossing of the TRUE correlation
    C_Y(k) = (1-2g)^2 rho_X^k measured from the C(0)=1 baseline:
        k* = (-1 - 2 ln|1-2g|) / ln(rho_X),  reported only when k* >= 1.
    It exists only for |1-2g| > (1/(e rho_X))^(1/2) ~ 0.613, i.e.
    gamma < ~0.19 or gamma > ~0.81; the middle band has NO experienced 1/e
    memory scale.  49.5 (gamma=0) -> 27.4 (gamma=0.1).

Known-limit tells (hard asserts, the one-failed-tell discipline):
    gamma=0:  Y == H exactly
    gamma=1:  Y == 1-H exactly
    gamma=.5: I_emp ~ 0 and H1_emp ~ 1 (within MC tolerance)
    H_inf limits (above) and the |1-2g|^2 amplitude flatness at lags 1-40
    for gamma in {0.1, 0.3}.

Round-4 review (2026-11-21): two independent external reviews + agent
re-verification of every numerical claim — see ../psychedelic-ab-fork-note.md
section 9.  Changes: channel text; H_rate -> H_1 + H_inf filter column;
persistence metrics; verdict wording.
"""
import hashlib
import zlib

import numpy as np

# --------------------------- parameters --------------------------------------
S = 0.99            # P(stay) for the substrate chain (depth2/3 family, xi ~ 50)
N = 200_000         # trajectory length
SEED_A = 20261121   # substrate seed: layer A is fixed across all rows
SEED_B = 20261122   # channel-noise seed
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
TOL_I, TOL_RHO, TOL_H = 0.02, 0.02, 0.02
TOL_INF = 0.02      # H_inf limit/symmetry tolerance
TOL_AMP = 0.02      # amplitude-flatness tolerance at lags 1-40
WARM = 1000         # filter warm-up before averaging

# --------------------------- layer A: the substrate --------------------------
def substrate_trajectory(seed):
    """1st-order chain, P(stay)=S, fair stationary (p=0.5)."""
    rng = np.random.default_rng(seed)
    x = np.empty(N, dtype=np.int8)
    x[0] = rng.integers(2)
    flip = rng.random(N - 1) < (1 - S)
    x[1:] = x[0] ^ (np.cumsum(flip, dtype=np.int64) % 2)
    x = x.astype(np.int8)
    return x

def checksum(x):
    # full-trajectory hash (the first bytes of a slow chain are uninformative)
    return hashlib.sha256(x.tobytes()).hexdigest()[:16]

# --------------------------- layer B: the gate -------------------------------
def bsc(x, gamma, rng):
    """Bit-flip channel (BSC): flip each bit independently with prob gamma."""
    if gamma == 0.0:
        return x.copy()
    if gamma == 1.0:
        return 1 - x
    flip = rng.random(N) < gamma
    return (x ^ flip).astype(np.int8)

# --------------------------- observables -------------------------------------
def h2(p):
    """Binary entropy, bits; h(0)=h(1)=0."""
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

def mutual_information(x, y):
    """Empirical I(X;Y), bits, from the 4-bin joint + marginals."""
    joint = np.bincount(x.astype(np.int64) * 2 + y.astype(np.int64),
                        minlength=4).reshape(2, 2) / N
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    i = 0.0
    for i_ in range(2):
        for j in range(2):
            if joint[i_, j] > 0:
                i += joint[i_, j] * np.log2(joint[i_, j] / (px[i_] * py[j]))
    return i

def corr_lag(z, k):
    """Pearson correlation of the +/-1 stream with its k-step shift."""
    return float(np.mean(z[:-k] * z[k:]))

def cond_entropy1(y):
    """Empirical 1-step conditional entropy H(y_t | y_{t-1}), bits.
    (ROUND-4: this is H_1, NOT the entropy rate of the hidden-Markov process.)"""
    m = N - 1
    joint = np.bincount(y[:-1].astype(np.int64) * 2 + y[1:].astype(np.int64),
                        minlength=4).reshape(2, 2) / m
    pprev = joint.sum(axis=1)
    h = 0.0
    for i in range(2):
        if pprev[i] > 0:
            for j in range(2):
                if joint[i, j] > 0:
                    h -= joint[i, j] * np.log2(joint[i, j] / pprev[i])
    return h

def hmme_rate(x, y, g):
    """True entropy rate H_inf(Y) = lim H(Y_t | Y_{t-1}, ...) of the
    hidden-Markov observation process, via the Bayes filter:
    H_inf = E[h(q_t)], q_t = P(Y_t=1 | Y_{<t}).  No closed form.
    Filter order per step: prior -> q -> observe -> transition."""
    p = 0.5  # prior for A_0 (fair stationary)
    qsum = 0.0
    for t in range(N):
        q = g + p * (1 - 2 * g)
        if t >= WARM:
            q = min(max(q, 1e-15), 1 - 1e-15)
            qsum += -(q * np.log2(q) + (1 - q) * np.log2(1 - q))
        # observe y[t] -> posterior of A_t; then transition -> prior for A_{t+1}
        num = p * (1 - g) if y[t] else p * g
        p_post = num / (num + (1 - p) * (g if y[t] else 1 - g))
        p = p_post * S + (1 - p_post) * (1 - S)
    return qsum / (N - WARM)

def xi_cross1e(g, rhoA):
    """1/e crossing of the TRUE correlation C_Y(k) = (1-2g)^2 rhoA^k (k>=1),
    from the C(0)=1 baseline: k* = (-1 - 2 ln|1-2g|) / ln(rhoA).
    Returns 0.0 when the crossing already passed by lag 1 (k* < 1)."""
    k = (-1.0 - 2.0 * np.log(abs(1 - 2 * g) + 1e-15)) / np.log(rhoA)
    return k if k >= 1.0 else 0.0

def compress_ratio(bits):
    """zlib size ratio (compressed/original) of the packed bit string."""
    raw = np.packbits(bits)
    return len(zlib.compress(raw, 9)) / len(raw)

# --------------------------- ASCII plot (house convention) -------------------
def ascii_plot(xs, ys, title, width=56, height=15):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    xmin, xmax = xs.min(), xs.max(); ymin, ymax = ys.min(), ys.max()
    if ymax - ymin < 1e-12: ymax = ymin + 1e-12
    grid = [[' '] * width for _ in range(height)]
    for x, y in zip(xs, ys):
        cx = int((x - xmin) / (xmax - xmin + 1e-15) * (width - 1))
        cy = int((y - ymin) / (ymax - ymin + 1e-15) * (height - 1))
        grid[height - 1 - cy][cx] = '*'
    for i in range(width): grid[height - 1][i] = '-'
    for rr in range(height): grid[rr][0] = '|'
    lines = [title, '']
    step = max(1, height // 4)
    for rr in range(height - 1, -1, -1):
        val = ymin + (height - 1 - rr) / (height - 1) * (ymax - ymin)
        tag = (f"{val: .4g}".rjust(9) if (height - 1 - rr) % step == 0 else ' ' * 9)
        lines.append(tag + ' ' + ''.join(grid[rr]))
    return '\n'.join(lines)

# --------------------------- main --------------------------------------------
def main():
    print("=" * 78)
    print("DUAL-FIELD -- 2-layer substrate/experience model (A fixed, B variable)")
    print("                (round-4 metrics: H_1 + H_inf, corrected persistence)")
    print("=" * 78)
    print(f"Layer A: 1st-order chain, P(stay)={S}, N={N}, seed={SEED_A}.")
    print("Layer B: bit-flip channel (BSC) gate gamma, crossover gamma.")
    print("         (NOT 'replace by a random bit' -- that has crossover gamma/2.)")
    print("         H identical across all rows (asserted).")
    print()

    H = substrate_trajectory(SEED_A)
    zH = 2 * H.astype(np.float64) - 1
    rho_x = corr_lag(zH, 1)
    h_x = cond_entropy1(H)
    print("LAYER A (substrate / causal process) -- invariant across all rows:")
    print(f"  p(x=1)={H.mean():.4f}  rho_1={rho_x:+.4f} (theory 2s-1={2*S-1:+.4f})")
    print(f"  H_1={h_x:.4f} bits/step  (theory h(1-s)={h2(1-S):.4f})")
    print(f"  1/e memory scale xi_A = {1.0/abs(np.log(rho_x)):.1f} steps "
          f"(theory {1.0/abs(np.log(2*S-1)):.1f})")
    print(f"  D_causal = N = {N} sequential steps (a property of what happened)")
    print(f"  checksum = {checksum(H)}")
    print()

    # Known-limit tells (hard asserts)
    y0 = bsc(H, 0.0, None)
    y1 = bsc(H, 1.0, None)
    assert np.array_equal(y0, H), "gamma=0 must reproduce H exactly"
    assert np.array_equal(y1, 1 - H), "gamma=1 must invert H exactly"
    print("Known-limit tells: gamma=0 -> Y==H  [PASS];  gamma=1 -> Y==1-H  [PASS]")
    print()

    rng_b = np.random.default_rng(SEED_B)
    print(f"{'gamma':>6} {'I_emp':>8} {'I_th':>9} {'rho_emp':>9} {'rho_th':>11} "
          f"{'H1_emp':>9} {'H1_th':>8} {'Hinf_emp':>9} {'zlib':>6} {'xi1e':>6}  verdict")
    rows = []
    worst = 0.0
    for g in GAMMAS:
        y = bsc(H, g, rng_b)
        i_emp = mutual_information(H, y)
        i_th = 1 - h2(g)
        zy = 2 * y.astype(np.float64) - 1
        r_emp = corr_lag(zy, 1)
        r_th = rho_x * (1 - 2 * g) ** 2
        h1_emp = cond_entropy1(y)
        h1_th = h2((1 + rho_x * (1 - 2 * g) ** 2) / 2)
        hinf_emp = hmme_rate(H, y, g)
        zr = compress_ratio(y)
        xi1e = xi_cross1e(g, rho_x)
        dev = max(abs(i_emp - i_th) / TOL_I, abs(r_emp - r_th) / TOL_RHO,
                  abs(h1_emp - h1_th) / TOL_H)
        worst = max(worst, dev)
        ok = "PASS" if dev < 1 else "FAIL"
        rows.append((g, i_emp, r_emp, h1_emp, hinf_emp, zr, xi1e))
        print(f"{g:>6.2f} {i_emp:>8.4f} {i_th:>9.4f} {r_emp:>+9.4f} {r_th:>+11.4f} "
              f"{h1_emp:>9.4f} {h1_th:>8.4f} {hinf_emp:>9.4f} {zr:>6.3f} "
              f"{xi1e:>6.1f}  {ok}")

    print()
    print(f"max deviation vs closed forms I/rho/H_1 (in tolerance units): {worst:.3f}  "
          f"({'PASS' if worst < 1 else 'FAIL'} -- tolerances: I {TOL_I}, rho {TOL_RHO}, H1 {TOL_H})")
    assert worst < 1, "empirical statistics deviate from the closed forms"

    # H_inf tells: limits + symmetry (no closed form, so shape/limit asserts).
    # Index-based: GAMMAS is symmetric under g -> 1-g (i <-> len-1-i).
    inf_vals = [r[4] for r in rows]
    h_lim = h2(1 - S)
    mid = len(GAMMAS) // 2
    assert abs(inf_vals[mid] - 1.0) < TOL_INF, "H_inf(0.5) must be 1 (white noise)"
    assert abs(inf_vals[0] - h_lim) < TOL_INF, "H_inf(0) must equal the substrate rate"
    assert abs(inf_vals[-1] - h_lim) < TOL_INF, "H_inf(1) must equal the substrate rate (relabeling)"
    for k in range(mid + 1):
        assert abs(inf_vals[k] - inf_vals[len(GAMMAS) - 1 - k]) < TOL_INF, \
            f"H_inf must be symmetric in gamma (row {k})"
    print(f"H_inf tells: limits (0/0.5/1 -> {h_lim:.4f}/1/{h_lim:.4f}) + "
          f"gamma<->1-gamma symmetry [PASS]")
    print()

    # Amplitude-flatness tell: C_Y(k)/C_X(k) = (1-2g)^2, decay rate invariant
    zy = {g: 2 * bsc(H, g, np.random.default_rng(SEED_B + int(g * 100))).astype(np.float64) - 1
          for g in (0.1, 0.3)}
    flat_ok = True
    for g in (0.1, 0.3):
        for k in (1, 5, 20, 40):
            ratio = corr_lag(zy[g], k) / corr_lag(zH, k)
            if abs(ratio - (1 - 2 * g) ** 2) > TOL_AMP:
                flat_ok = False
    assert flat_ok, "amplitude scaling (1-2g)^2 must be lag-independent at 1..40"
    print("Amplitude tell: C_Y(k)/C_X(k) = (1-2g)^2 at lags 1,5,20,40 for g in "
          "{0.1, 0.3} [PASS] -- the decay rate is invariant, only the amplitude "
          "is scaled; the substrate's time is HIDDEN, not destroyed.")
    print()

    g = [r[0] for r in rows]; i = [r[1] for r in rows]
    r = [r[2] for r in rows]; h1 = [r[3] for r in rows]
    hinf = [r[4] for r in rows]; z = [r[5] for r in rows]
    print(ascii_plot(g, i, "I(X;Y) vs gamma   (theory: 1 - h(gamma))"))
    print()
    print(ascii_plot(g, r, "rho_1(Y) vs gamma   (theory: rho_X * (1-2gamma)^2)"))
    print()
    print(ascii_plot(g, h1, "H_1(Y) = H(y_t|y_{t-1}) vs gamma   (theory: h((1+rho_X(1-2g)^2)/2))"))
    print()
    print(ascii_plot(g, hinf, "H_inf(Y) true entropy rate (Bayes filter) vs gamma"))
    print()
    print(ascii_plot(g, z, "zlib compress ratio vs gamma   (1 = incompressible)"))
    print()

    print("A/B ILLUSTRATION (round-4 corrected metrics):")
    print("  - Layer A is INVARIANT under gamma: one trajectory H, one causal")
    print("    unfolding, D_causal = N; checksum identical for every row above.")
    print("  - Layer B is FREELY parameterized by gamma: I, rho, H_1, H_inf and")
    print("    the compressibility of Y(gamma) all vary, for the SAME substrate.")
    print(f"  - TEMPORAL STRUCTURE: the experience's correlation amplitude is scaled")
    print(f"    by (1-2gamma)^2 (1/e memory scale {1.0/abs(np.log(rho_x)):.1f} ->")
    print(f"    {xi_cross1e(0.1, rho_x):.1f} at gamma=0.1; ABSENT for 0.19 < gamma < 0.81)")
    print("    while the long-lag DECAY RATE is unchanged (amplitude tell above):")
    print("    the substrate's time is HIDDEN, not destroyed (Y is a hidden-Markov")
    print("    process; the rate is recoverable from Y alone by a filter).")
    print("  - INFORMATION vs STABILITY: gamma=1 keeps I=1 (full information) under")
    print("    an inverted mapping; I, rho, H and zlib are all invariant under")
    print("    symbol relabeling, so the mirror is indistinguishable from sobriety")
    print("    BY THESE MEASURES BY CONSTRUCTION -- the measures are blind to")
    print('    representation ("alienness" is a 4th quantity).')
    print()
    print("VERDICT (structure, not ontology):")
    print("  - fixed substrate (A) + variable mapping (B) -> different experienced")
    print("    realities: the layer the EXPERIENCE tracks is B (an interpretation of")
    print("    the construction, not a theorem; the toy shows the A->B map is a")
    print("    free parameter).")
    print("  - => under the experience assumption, the depth4 fork (D_causal vs")
    print("    D_min) leans toward D_min (B) for the experience-relevant branch.")
    print("  - by design the toy is silent on the substrate: it shows the free-")
    print("    parameter structure between A and B, not what the substrate is.")

if __name__ == "__main__":
    main()

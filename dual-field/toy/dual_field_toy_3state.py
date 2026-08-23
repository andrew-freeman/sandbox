#!/usr/bin/env python3
"""
Dual-Field Hypothesis — toy model, 3-STATE UPGRADE (Steps 2+3+6).

Why 3 states
------------
A 2-state system carries NO net directed current in steady state (stationarity
forces J(0->1)=J(1->0)); a current needs >=3 states.  So a 3-state ring is the
minimal system that can host a 'motor' effect and a genuine thermodynamic
uncertainty relation (TUR).  The headline result: the dual field acts as
INFORMATION FUEL that rectifies / powers the motor current.

Physical system
---------------
A 3-state ring x_t in {0,1,2} with SHORT-RANGE MEMORY (inertia): the transition
depends on (x_{t-1}, x_t) (a 2nd-order Markov chain, lifted to the N^2=9 joint
states s=(a,b)=(x_{t-1},x_t)).  Two ingredients in the baseline (standard
physics):
  * a constant TILT favoring clockwise (cw rate > ccw rate)  -> baseline current
  * INERTIA: the system tends to continue its previous direction  -> memory
The inertia is what makes the excess predictive information nonzero, so the dual
field acts on genuine 'information in the past', not a reparameterization.

Dual-field coupling (the hypothesis)
------------------------------------
P(H) ~ P_phys(H) * exp(eps * I[H])  applied locally per transition outcome y:
      P_DF(y | b,a) = P_phys(y|b,a) * exp(eps * I(b,a,y)) / Z
with the informational functional = EXCESS PREDICTIVE INFORMATION of the memory:
      I(b,a,y) = log[ P_phys(y | x_t=b, x_{t-1}=a) / P_null(y | x_t=b) ],
      P_null(y|b) = sum_a P(a|b) P_phys(y|b,a)     (the 1st-order 'local' desc.)
P_null is fixed from the baseline (eps=0) steady state.  eps>0 amplifies the
memory/inertia (favor information-consistent trajectories); eps<0 suppresses it;
eps=0 recovers standard physics exactly (the null H0).

Deliverables
------------
(a) directed current J(eps)             -> the 'motor' signature + residual delta
(b) entropy production Sdot(eps)        -> the nonequilibrium 'FT residual'
(b') information content I_avg(eps)     -> the 'information selection' signature
(c) TUR:  precision fraction E = 2*<J>^2/(D*Sdot) <= 1  -> precision vs
        dissipation; how the dual field trades efficiency for information
(d) statistical power to detect eps vs N (pre-registered P(A)=p+delta)
"""
import numpy as np

N = 3
rng = np.random.default_rng(20260823)

# --------------------------- baseline (eps=0) physics ------------------------
# tilt: cw favored over ccw ;  inertia: continue the previous direction
BASE_CW, BASE_CCW, BASE_STAY = 0.30, 0.10, 0.60
INERTIA = 0.5

def base_prob(a, b):
    """P(next=y | now=b, prev=a) as an array over y in 0..N-1."""
    if b == (a + 1) % N:      pcw, pccw = 1, 0   # prev move was cw
    elif b == (a + 2) % N:    pcw, pccw = 0, 1   # prev move was ccw
    else:                     pcw, pccw = 0, 0   # stayed
    wcw  = BASE_CW  * (1 + INERTIA * pcw - INERTIA * pccw)
    wccw = BASE_CCW * (1 + INERTIA * pccw - INERTIA * pcw)
    wst  = BASE_STAY
    tot = wcw + wccw + wst
    P = np.zeros(N)
    P[(b + 1) % N] = wcw / tot     # clockwise neighbor
    P[(b + 2) % N] = wccw / tot    # counterclockwise neighbor
    P[b]          = wst / tot      # stay
    return P

def sidx(a, b): return a * N + b
def mat_from_table(P):
    M = np.zeros((N * N, N * N))
    for a in range(N):
        for b in range(N):
            f = sidx(a, b)
            for y in range(N):
                M[sidx(b, y), f] += P[(a, b)][y]
    return M

def stationary(M, iters=100000):
    pi = np.full(N * N, 1.0 / (N * N))
    for _ in range(iters):
        pn = M @ pi
        if np.max(np.abs(pn - pi)) < 1e-15:
            return pn
        pi = pn
    return pi

P_BASE = {(a, b): base_prob(a, b) for a in range(N) for b in range(N)}
M0  = mat_from_table(P_BASE)
PI0 = stationary(M0)

# baseline 1st-order (local) description P_NULL[(b,y)] = P_null(next=y | now=b)
P_NULL = {}
for b in range(N):
    marg = sum(PI0[sidx(a, b)] for a in range(N))
    for y in range(N):
        P_NULL[(b, y)] = sum(PI0[sidx(a, b)] * P_BASE[(a, b)][y]
                             for a in range(N)) / marg

# --------------------------- dual-field modification -------------------------
def df_table(eps):
    if eps == 0:
        return P_BASE
    T = {}
    for a in range(N):
        for b in range(N):
            Pb = P_BASE[(a, b)]; w = np.zeros(N)
            for y in range(N):
                if Pb[y] > 0:
                    r = Pb[y] / P_NULL[(b, y)]
                    w[y] = Pb[y] * r ** eps
            T[(a, b)] = w / w.sum()
    return T

# --------------------------- observables ------------------------------------
def current(eps=0.0):
    """Net clockwise current (cw minus ccw crossings per step)."""
    T = df_table(eps); pi = stationary(mat_from_table(T))
    cw = ccw = 0.0
    for a in range(N):
        for b in range(N):
            cw  += pi[sidx(a, b)] * T[(a, b)][(b + 1) % N]
            ccw += pi[sidx(a, b)] * T[(a, b)][(b + 2) % N]
    return cw - ccw

def I_avg(eps=0.0):
    """Average dual-field information over the realized eps-process."""
    T = df_table(eps); pi = stationary(mat_from_table(T)); S = 0.0
    for a in range(N):
        for b in range(N):
            for y in range(N):
                if P_BASE[(a, b)][y] > 0:
                    Iv = np.log(P_BASE[(a, b)][y] / P_NULL[(b, y)])
                    S += pi[sidx(a, b)] * T[(a, b)][y] * Iv
    return S

def entropy_production(eps=0.0):
    """Steady-state entropy production (nats/step), dynamical-reverse pairing.
       reverse of step (a,b)->(b,y) is step (b,y)->(y,a)."""
    T = df_table(eps); pi = stationary(mat_from_table(T)); S = 0.0
    for a in range(N):
        for b in range(N):
            for y in range(N):
                Jf = pi[sidx(a, b)] * T[(a, b)][y]
                Jr = pi[sidx(b, y)] * T[(b, y)][a]
                if Jf > 0 and Jr > 0:
                    S += Jf * np.log(Jf / Jr)
    return S

def db_residual(eps=0.0):
    T = df_table(eps); pi = stationary(mat_from_table(T)); res = 0.0
    for a in range(N):
        for b in range(N):
            for y in range(N):
                Jf = pi[sidx(a, b)] * T[(a, b)][y]
                Jr = pi[sidx(b, y)] * T[(b, y)][a]
                if Jf > 0 and Jr > 0:
                    res = max(res, abs(np.log(Jf / Jr)))
    return res

# --------------------------- simulation -------------------------------------
def simulate_crossings(eps, n_steps, n_rep):
    """n_rep parallel 9-state trajectories -> net cw crossings (int) each."""
    T = df_table(eps)
    prob = np.zeros((N * N, N))
    for a in range(N):
        for b in range(N):
            prob[sidx(a, b)] = T[(a, b)]
    x = rng.integers(0, N * N, size=n_rep)
    nc = np.zeros(n_rep, np.int64)
    t = 0
    while t < n_steps:
        n = min(50000, n_steps - t)
        r = rng.random((n, n_rep))
        for k in range(n):
            b = x % N
            cdf = np.cumsum(prob[x], axis=1)              # (n_rep, N)
            y = (r[k][:, None] < cdf).argmax(axis=1)      # (n_rep,) first crossing
            nc += ((y == (b + 1) % N).astype(np.int8)
                   - (y == (b + 2) % N).astype(np.int8))
            x = b * N + y
        t += n
    return nc

# --------------------------- ASCII plot -------------------------------------
def ascii_plot(xs, ys, title, xlabel, ylabel, width=56, height=15):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    xmin, xmax = xs.min(), xs.max(); ymin, ymax = ys.min(), ys.max()
    if ymax - ymin < 1e-12: ymax = ymin + 1e-12
    grid = [[' '] * width for _ in range(height)]
    for x, y in zip(xs, ys):
        cx = int((x - xmin) / (xmax - xmin + 1e-15) * (width - 1))
        cy = int((y - ymin) / (ymax - ymin) * (height - 1))
        grid[height - 1 - cy][cx] = '*'
    for i in range(width): grid[height - 1][i] = '-'
    for rr in range(height): grid[rr][0] = '|'
    lines = [title, '']
    step = max(1, height // 4)
    for rr in range(height - 1, -1, -1):
        val = ymin + (height - 1 - rr) / (height - 1) * (ymax - ymin)
        tag = (f"{val: .4g}".rjust(9) if (height - 1 - rr) % step == 0 else ' ' * 9)
        lines.append(tag + ' ' + ''.join(grid[rr]))
    lines.append(' ' * 9 + ' +' + '-' * (width - 1))
    lines.append(' ' * 10 + xlabel + f"   [{ylabel}]")
    return '\n'.join(lines)

# --------------------------- main -------------------------------------------
def main():
    print("=" * 78)
    print("DUAL-FIELD TOY MODEL — 3-STATE RING UPGRADE (information-powered motor)")
    print("=" * 78)
    print(f"baseline 9-state steady state pi0 = {np.round(PI0, 4).tolist()}")
    print("baseline local (1st-order) P_null(next=cw|b), P_null(next=ccw|b), P_null(stay|b):")
    for b in range(N):
        print(f"   b={b}:  cw={P_NULL[(b,(b+1)%N)]:.4f}  ccw={P_NULL[(b,(b+2)%N)]:.4f}  "
              f"stay={P_NULL[(b,b)]:.4f}")

    J0 = current(0.0)
    print(f"\nbaseline:  J={J0:+.6f}  I_avg={I_avg(0.0):+.5f}  "
          f"Sdot={entropy_production(0.0):.5f}  DB_resid={db_residual(0.0):.4f}")
    print(f"\n{'eps':>6} {'J(cw curr)':>12} {'dJ=J-J0':>10} {'I_avg':>9} "
          f"{'Sdot':>9} {'DB_resid':>9}")
    for eps in [-1.0, -0.5, 0.0, 0.2, 0.5, 1.0, 2.0]:
        print(f"{eps:6.2f} {current(eps):+12.6f} {current(eps)-J0:+10.6f} "
              f"{I_avg(eps):+9.5f} {entropy_production(eps):9.5f} "
              f"{db_residual(eps):9.4f}")

    # pre-registered residual delta(eps) = J(eps) - J(0)
    print("\n  pre-registered residual  delta(eps) = J(eps)-J(0)   (O(eps) check):")
    for eps in [0.05, 0.1, 0.2]:
        print(f"    eps={eps:4.2f}  delta={current(eps)-J0:+.6f}   "
              f"delta/eps={(current(eps)-J0)/eps:+.5f}")

    # (c) TUR
    print("\n" + "-" * 78)
    print("(c) THERMODYNAMIC UNCERTAINTY RELATION")
    print("    TUR:  Var(G)/<G>^2 >= 2/Sdot   <=>   D/J^2 >= 2/Sdot   (D=Var(G)/T)")
    print("    precision fraction  E = 2*<J>^2/(D*Sdot)  must satisfy  E <= 1")
    print("    (E=1 saturates the bound = maximally precise for its dissipation)")
    for eps in [0.0, 0.5, 1.0, 2.0]:
        nc = simulate_crossings(eps, 20000, 200)
        Jm = nc.mean() / 20000.0
        D  = nc.var() / 20000.0
        S  = entropy_production(eps)
        E  = 2 * Jm**2 / (D * S) if (D > 0 and S > 0) else np.inf
        ok = "ok" if E <= 1 else "VIOLATION?"
        print(f"    eps={eps:4.2f}  <J>={Jm:+.6f}  D={D:.3e}  Sdot={S:.5f}  "
              f"E={E:.3f}  [{ok}]")

    # (d) power
    print("\n" + "-" * 78)
    print("(d) MIN DETECTABLE eps @95% vs N   [observable = net current J]")
    e_grid = np.arange(0.01, 4.0 + 1e-9, 0.01)
    Jex = np.array([current(e) for e in e_grid])
    N_grid = [2_000, 20_000, 200_000, 2_000_000]
    print(f"    {'N':>9} {'min_eps@95%':>12} {'delta there':>12} {'SE(N)':>11}")
    for Nt in N_grid:
        nc0 = simulate_crossings(0.0, Nt, 300)
        J0m = nc0.mean() / Nt
        J0se = nc0.std() / np.sqrt(300) / Nt
        mask = np.abs(Jex - J0m) >= 1.96 * J0se
        if mask.any():
            me = e_grid[mask.argmax()]
            print(f"    {Nt:9d} {me:12.3f} {Jex[mask.argmax()]-J0m:+12.6f} "
                  f"{J0se:11.3e}")
        else:
            print(f"    {Nt:9d} {'not<4':>12}")

    # plots
    ep = np.linspace(-1.0, 2.0, 91)
    Jc = [current(e) for e in ep]
    Ss = [entropy_production(e) for e in ep]
    Ii = [I_avg(e) for e in ep]
    print("\n" + ascii_plot(ep, Jc, "directed current J(eps)  [the motor]", "eps", "J (crossings/step)"))
    print()
    print(ascii_plot(ep, Ss, "entropy production Sdot(eps)", "eps", "Sdot (nats/step)"))
    print()
    print(ascii_plot(ep, Ii, "average dual-field information I_avg(eps)", "eps", "I_avg (nats/step)"))
    print("\nDone.")

if __name__ == "__main__":
    main()

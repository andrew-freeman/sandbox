#!/usr/bin/env python3
"""
Dual-Field Hypothesis — toy model (Steps 2+3+6 combined).  [v3: correct observables]

Physical system
---------------
A 2-state variable x_t in {0,1} WITH SHORT-RANGE MEMORY: the transition depends
on (x_{t-1}, x_t) (a 2nd-order Markov chain, lifted to a 4-state chain over the
joint states s=(a,b)=(x_{t-1},x_t)).  Minimal system that (i) carries genuine
'information in the past' and (ii) has a non-trivial nonequilibrium structure.

KEY FACT (checked numerically): a 2-state process carries NO net directed current
in steady state — stationarity forces J(0->1)=J(1->0).  A directed current
(a 'motor' effect, and the standard TUR) needs >=3 states.  So on a 2-state
system the dual-field signature is:  (a) population shift, (b) entropy-production
change (non-monotonic!), (b') information-content change.  Those are reported here.

Dual-field coupling (the hypothesis)
------------------------------------
P(H) ~ P_phys(H) * exp(eps * I[H])  applied locally per transition outcome y:
      P_DF(y | b,a) = P_phys(y|b,a) * exp(eps * I(b,a,y)) / Z
with the informational functional = EXCESS PREDICTIVE INFORMATION of the memory:
      I(b,a,y) = log[ P_phys(y | x_t=b, x_{t-1}=a) / P_null(y | x_t=b) ],
      P_null(y|b) = sum_a P(a|b) P_phys(y|b,a)     (the 1st-order 'local' desc.)
I = information in the memory bit a beyond the local state b  = Layer I:
'an informational variable not captured by the ordinary local physical
description'.  Observer-independent, computable, NOT a reparameterization of
P_phys (depends on the past).  P_null is fixed from the baseline (eps=0) steady
state, so the dual field is a well-defined, non-self-referential perturbation.
      eps>0 -> amplify the memory contrast (select information-rich trajectories)
      eps<0 -> suppress it (push toward the memoryless / local description)
      eps=0 -> EXACTLY the baseline (the null H0)

Deliverables
------------
(a) population P(x=1)                      -> pre-registered residual delta(eps)
(b) entropy production Sdot(eps)           -> nonequilibrium 'FT residual';
                                               non-monotonic, reversibility min
(b') information content I_avg(eps)        -> the 'information selection' signature
(d) statistical power to detect eps vs N   (pre-registered P(A)=p+delta)
NOTE: the standard TUR (c) needs a current (>=3 states); see report + next step.
"""
import numpy as np

rng = np.random.default_rng(20260823)

# --------------------------- baseline (eps=0) physics ------------------------
# P1[a,b] = P(next x=1 | x_t=b, x_{t-1}=a)     (a=prev, b=now)
P1 = {
    (0, 0): 0.12,   # been in 0, settled  -> low 0->1
    (1, 0): 0.30,   # just flipped to 0   -> high 0->1 (excited)
    (0, 1): 0.45,   # just flipped to 1   -> 45% stay 1, 55% flip back (excited)
    (1, 1): 0.88,   # been in 1, settled  -> 88% stay 1, 12% flip to 0
}
def sidx(a, b): return a * 2 + b          # 0=00, 1=01, 2=10, 3=11

def make_matrix(P):
    M = np.zeros((4, 4))
    for a in (0, 1):
        for b in (0, 1):
            f = sidx(a, b); p1 = P[(a, b)]
            M[b * 2 + 0, f] += (1 - p1)   # to (b,0)
            M[b * 2 + 1, f] += p1         # to (b,1)
    return M

def stationary(M, iters=100000):
    pi = np.full(4, 0.25)
    for _ in range(iters):
        pn = M @ pi
        if np.max(np.abs(pn - pi)) < 1e-15:
            return pn
        pi = pn
    return pi

M0  = make_matrix(P1)
PI0 = stationary(M0)

# baseline 1st-order (local) description P_null(y|b)
P_NULL = {}
for b in (0, 1):
    marg = sum(PI0[sidx(a, b)] for a in (0, 1))
    P_NULL[(b, 1)] = sum(PI0[sidx(a, b)] * P1[(a, b)] for a in (0, 1)) / marg
    P_NULL[(b, 0)] = 1.0 - P_NULL[(b, 1)]

# --------------------------- dual-field modification -------------------------
def df_P1(a, b, eps):
    p  = P1[(a, b)]; pn = P_NULL[(b, 1)]
    r1 = p / pn                    # likelihood ratio for y=1
    r0 = (1 - p) / (1 - pn)        # likelihood ratio for y=0
    w1 = p * r1 ** eps
    w0 = (1 - p) * r0 ** eps
    return w1 / (w1 + w0)

def table(eps):
    if eps == 0: return P1
    return {(a, b): df_P1(a, b, eps) for a in (0, 1) for b in (0, 1)}

def matrix(eps):
    return M0 if eps == 0 else make_matrix(table(eps))

# --------------------------- observables ------------------------------------
def steady(eps):
    return stationary(matrix(eps)), table(eps)

def pop1(eps=0.0):
    pi, _ = steady(eps)
    return pi[1] + pi[3]           # P(x=1)

def I_local(a, b, y):
    """the dual-field functional: excess predictive info (vs baseline local)."""
    if y == 1: return np.log(P1[(a, b)] / P_NULL[(b, 1)])
    else:      return np.log((1 - P1[(a, b)]) / P_NULL[(b, 0)])

def I_avg(eps=0.0):
    """Average dual-field information over the realized eps-process.
       eps>0 selects high-I outcomes -> I_avg should rise with eps."""
    pi, P = steady(eps); S = 0.0
    for a in (0, 1):
        for b in (0, 1):
            for y in (0, 1):
                pf = P[(a, b)] if y == 1 else 1 - P[(a, b)]
                S += pi[sidx(a, b)] * pf * I_local(a, b, y)
    return S

def _fwd(P, a, b, y):  return P[(a, b)] if y == 1 else 1 - P[(a, b)]
def _rev(P, a, b, y):  return P[(b, y)] if a == 1 else 1 - P[(b, y)]

def entropy_production(eps=0.0):
    """Steady-state entropy production (nats/step), dynamical-reverse pairing.
       sigma = sum J_f ln(J_f/J_r) >= 0 ; 0 <=> reversible (detailed balance)."""
    pi, P = steady(eps); S = 0.0
    for a in (0, 1):
        for b in (0, 1):
            for y in (0, 1):
                Jf = pi[sidx(a, b)] * _fwd(P, a, b, y)
                Jr = pi[sidx(b, y)] * _rev(P, a, b, y)
                if Jf > 0 and Jr > 0:
                    S += Jf * np.log(Jf / Jr)
    return S

def db_residual(eps=0.0):
    pi, P = steady(eps); res = 0.0
    for a in (0, 1):
        for b in (0, 1):
            for y in (0, 1):
                Jf = pi[sidx(a, b)] * _fwd(P, a, b, y)
                Jr = pi[sidx(b, y)] * _rev(P, a, b, y)
                if Jf > 0 and Jr > 0:
                    res = max(res, abs(np.log(Jf / Jr)))
    return res

# --------------------------- simulation -------------------------------------
def simulate_populations(eps, n_steps, n_rep):
    """n_rep parallel 4-state trajectories, length n_steps -> fraction in x=1."""
    P = table(eps)
    p1v = np.array([P[(s // 2, s % 2)] for s in range(4)])   # P(next=1 | s)
    x = rng.integers(0, 4, size=n_rep)
    cnt = np.zeros(n_rep, np.int64)
    t = 0
    while t < n_steps:
        n = min(200000, n_steps - t)
        r = rng.random((n, n_rep))
        for k in range(n):
            b = x % 2
            to1 = r[k] < p1v[x]
            x = b * 2 + to1
            cnt += (x % 2)                    # count 'now' state == 1
        t += n
    return cnt / n_steps

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
    print("DUAL-FIELD TOY MODEL v3 — 2-state chain w/ memory, I = excess pred. info")
    print("=" * 78)
    print(f"baseline 4-state steady state pi0 = {np.round(PI0, 4).tolist()}")
    print(f"baseline local (1st-order) P_null(1|now=0)={P_NULL[(0,1)]:.4f}  "
          f"P_null(1|now=1)={P_NULL[(1,1)]:.4f}")

    P0 = pop1(0.0)
    print(f"\nbaseline:  P(x=1)={P0:.5f}  I_avg={I_avg(0.0):+.6f}  "
          f"Sdot={entropy_production(0.0):.5f}  DB_resid={db_residual(0.0):.4f}")
    print("  (note: net 2-state current is identically 0 in steady state — a fact")
    print("   about 2-state processes; the signatures here are population, Sdot, I)")
    print(f"\n{'eps':>5} {'P(x=1)':>9} {'dP':>9} {'I_avg':>9} {'Sdot':>9} {'DB_resid':>9}")
    for eps in [0.0, 0.1, 0.25, 0.5, 1.0, 2.0]:
        print(f"{eps:5.2f} {pop1(eps):9.5f} {pop1(eps)-P0:+9.5f} {I_avg(eps):+9.5f} "
              f"{entropy_production(eps):9.5f} {db_residual(eps):9.4f}")

    # pre-registered residual delta(eps) = P_eps(x=1) - P_0(x=1)
    print("\n  pre-registered residual  delta(eps) = P_eps(x=1) - P_0(x=1):")
    for eps in [0.05, 0.1, 0.2]:
        print(f"    eps={eps:4.2f}  delta={pop1(eps)-P0:+.6f}   "
              f"delta/eps={(pop1(eps)-P0)/eps:+.5f}   (O(eps) check)")

    # fine scan: find the reversibility (Sdot) minimum
    print("\n  fine scan of Sdot(eps) — looking for the reversibility minimum:")
    efin = np.linspace(0.0, 1.0, 41)
    Sfin = [entropy_production(e) for e in efin]
    emin = efin[int(np.argmin(Sfin))]
    print(f"    Sdot minimum at eps* ~ {emin:.2f}  (Sdot={min(Sfin):.2e});  "
          f"Sdot(0)={entropy_production(0.0):.4f}, Sdot(1)={entropy_production(1.0):.4f}")

    # (d) statistical power vs N  (exact signal on P(x=1), simulated null noise)
    print("\n" + "-" * 78)
    print("(d) MIN DETECTABLE eps @95% vs N   [observable = P(x=1)]")
    print("    signal = |P_eps(x=1)-P_0(x=1)| (exact model);")
    print("    noise = SE of the population estimate from n_rep runs at eps=0")
    e_grid = np.arange(0.005, 3.0 + 1e-9, 0.005)
    Pex = np.array([pop1(e) for e in e_grid])
    N_grid = [2_000, 20_000, 200_000, 2_000_000]
    nrep_d = 300
    print(f"    {'N':>9} {'min_eps@95%':>12} {'delta there':>12} {'SE(N)':>11} "
          f"{'min_eps*sqrt(N)':>15}")
    for N in N_grid:
        h = simulate_populations(0.0, N, nrep_d)
        m, se = h.mean(), h.std() / np.sqrt(nrep_d)
        mask = np.abs(Pex - m) >= 1.96 * se
        if mask.any():
            me = e_grid[mask.argmax()]
            print(f"    {N:9d} {me:12.3f} {Pex[mask.argmax()]-m:+12.6f} "
                  f"{se:11.3e} {me*np.sqrt(N):15.3f}")
        else:
            print(f"    {N:9d} {'not<3':>12}")

    # plots
    ep = np.linspace(0, 2.0, 81)
    Pp = [pop1(e) for e in ep]
    Ss = [entropy_production(e) for e in ep]
    Ii = [I_avg(e) for e in ep]
    print("\n" + ascii_plot(ep, Pp, "population P(x=1) vs eps", "eps", "P(x=1)"))
    print()
    print(ascii_plot(ep, Ss, "entropy production Sdot(eps)  [non-monotonic]", "eps", "Sdot (nats/step)"))
    print()
    print(ascii_plot(ep, Ii, "average dual-field information I_avg(eps)", "eps", "I_avg (nats/step)"))
    print("\nDone.")

if __name__ == "__main__":
    main()

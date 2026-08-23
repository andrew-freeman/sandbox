#!/usr/bin/env python3
"""
Dual-Field toy — PERIODICALLY DRIVEN 3-STATE RATCHET (the 'information powers
the motor' target).

Idea
----
A 3-state ring {0,1,2} driven by a 2-phase square-wave protocol that is
TIME-REVERSAL SYMMETRIC on its own (rocking: phase A pushes clockwise, phase B
pushes counterclockwise, equal strength & duration).  A symmetric rocking drive
rectifies NOTHING in the memoryless case -> baseline (eps=0, no memory) current
is 0.  Short-range memory (inertia) lets the system break the symmetry; the
dual field, coupling to the excess predictive information, amplifies that memory
and is what RECTIFIES the drive into a net current.  If J(0)=0 and J(eps)>0 for
eps>0, the current is information-powered.

The dual-field coupling is identical to the other models:
    P_DF(y|a,b,phase) ∝ P_phys(y|a,b,phase) * exp(eps * I),
    I = log[ P_phys(y|a,b,phase) / P_null(phase)(y|b) ]   (excess pred. info)
with P_null(phase) fixed from the baseline (eps=0) periodic steady state.

Deliverables: periodic-steady-state net current J(eps) (the motor), the
information content I_avg(eps), and the pre-registered residual delta(eps).
"""
import numpy as np

N = 3
rng = np.random.default_rng(20260823)

# ---- protocol: symmetric rocking (A pushes cw, B pushes ccw) ----
T_A, T_B = 3, 3
T = T_A + T_B
ROCK = 0.35                 # rocking strength (cw in A, ccw in B)
BASE_STAY = 0.60
INERTIA = 0.5

def phase_seq():
    return ['A'] * T_A + ['B'] * T_B

def sidx(a, b): return a * N + b

def base_prob(phase, a, b):
    """P(next=y | a,b,phase), eps=0, with inertia. Symmetric rocking + tilt-free."""
    cw  = 0.5 + ROCK * (1 if phase == 'A' else -1)   # A: cw>ccw ; B: ccw>cw
    ccw = 0.5 - ROCK * (1 if phase == 'A' else -1)
    cw  = max(cw, 0.02); ccw = max(ccw, 0.02)
    if b == (a + 1) % N:   pcw, pccw = 1, 0
    elif b == (a + 2) % N: pcw, pccw = 0, 1
    else:                  pcw = pccw = 0
    wcw  = cw  * (1 + INERTIA * pcw - INERTIA * pccw)
    wccw = ccw * (1 + INERTIA * pccw - INERTIA * pcw)
    wst  = BASE_STAY
    tot = wcw + wccw + wst
    P = np.zeros(N)
    P[(b + 1) % N] = wcw / tot
    P[(b + 2) % N] = wccw / tot
    P[b]          = wst / tot
    return P

def phase_matrix(phase, table):
    M = np.zeros((N * N, N * N))
    for a in range(N):
        for b in range(N):
            f = sidx(a, b)
            P = table[(phase, a, b)]
            for y in range(N):
                M[sidx(b, y), f] += P[y]
    return M

def base_table():
    return {('A', a, b): base_prob('A', a, b) for a in range(N) for b in range(N)} | \
           {('B', a, b): base_prob('B', a, b) for a in range(N) for b in range(N)}

def base_matrices():
    tb = base_table()
    return [phase_matrix(ph, tb) for ph in phase_seq()]

def periodic_ss(matrices, iters=100000):
    M = np.eye(N * N)
    for Mt in matrices:                 # M_cycle = M_{T-1} @ ... @ M_0
        M = Mt @ M
    pi0 = np.full(N * N, 1.0 / (N * N))
    for _ in range(iters):
        pn = M @ pi0
        if np.max(np.abs(pn - pi0)) < 1e-15:
            pi0 = pn
            break
    pis, pi = [pi0], pi0
    for Mt in matrices:
        pi = Mt @ pi
        pis.append(pi)
    return pis[:T]                      # pi_0..pi_{T-1}

BASE_TB   = base_table()
BASE_PIS  = periodic_ss(base_matrices())

# P_null(phase)(y|b) from the baseline periodic steady state
def pnull():
    Pn = {}
    for ph, (t0, dur) in (('A', (0, T_A)), ('B', (T_A, T_B))):
        pi = np.mean([BASE_PIS[t] for t in range(t0, t0 + dur)], axis=0)
        for b in range(N):
            marg = sum(pi[sidx(a, b)] for a in range(N))
            for y in range(N):
                Pn[(ph, b, y)] = sum(pi[sidx(a, b)] * BASE_TB[(ph, a, b)][y]
                                     for a in range(N)) / marg
    return Pn

PN = pnull()

def df_table(eps):
    if eps == 0:
        return BASE_TB
    T_ = {}
    for ph in ('A', 'B'):
        for a in range(N):
            for b in range(N):
                Pb = BASE_TB[(ph, a, b)]; w = np.zeros(N)
                for y in range(N):
                    if Pb[y] > 0:
                        r = Pb[y] / PN[(ph, b, y)]
                        w[y] = Pb[y] * r ** eps
                T_[(ph, a, b)] = w / w.sum()
    return T_

def pis_for(eps):
    tb = df_table(eps)
    mats = [phase_matrix(ph, tb) for ph in phase_seq()]
    return periodic_ss(mats), mats

def current(eps=0.0):
    pis, mats = pis_for(eps)
    J = 0.0
    for t in range(T):
        pi = pis[t]; ph = phase_seq()[t]; tb = df_table(eps)
        for a in range(N):
            for b in range(N):
                J += pi[sidx(a, b)] * (tb[(ph, a, b)][(b + 1) % N]
                                       - tb[(ph, a, b)][(b + 2) % N])
    return J / T

def I_avg(eps=0.0):
    pis, _ = pis_for(eps); tb = df_table(eps); S = 0.0
    for t in range(T):
        pi = pis[t]; ph = phase_seq()[t]
        for a in range(N):
            for b in range(N):
                for y in range(N):
                    if BASE_TB[(ph, a, b)][y] > 0:
                        Iv = np.log(BASE_TB[(ph, a, b)][y] / PN[(ph, b, y)])
                        S += pi[sidx(a, b)] * tb[(ph, a, b)][y] * Iv
    return S / T

def main():
    print("=" * 74)
    print("DUAL-FIELD TOY — DRIVEN 3-STATE RATCHET (information powers the motor?)")
    print("=" * 74)
    print(f"protocol: A(cw push,{T_A} steps) / B(ccw push,{T_B} steps);  "
          f"rocking={ROCK}, inertia={INERTIA}")
    print("baseline check (eps=0, symmetric rocking):")
    J0 = current(0.0)
    print(f"    J(0) = {J0:+.6f}   (0 if the symmetric drive rectifies nothing)")
    # memoryless limit check: is the baseline current from memory?
    print(f"{'eps':>6} {'J(cw curr)':>13} {'dJ=J-J0':>11} {'I_avg':>9}")
    for eps in [0.0, 0.2, 0.5, 1.0, 2.0, -1.0]:
        print(f"{eps:6.2f} {current(eps):+13.6f} {current(eps)-J0:+11.6f} "
              f"{I_avg(eps):+9.5f}")
    print("\n  pre-registered residual delta(eps)=J(eps)-J(0)  (O(eps) check):")
    for eps in [0.1, 0.2, 0.5]:
        print(f"    eps={eps:4.2f}  delta={current(eps)-J0:+.6f}   "
              f"delta/eps={(current(eps)-J0)/eps:+.5f}")

    def ascii_plot(xs, ys, title, xlabel, ylabel, width=56, height=14):
        xs = np.asarray(xs, float); ys = np.asarray(ys, float)
        x0, x1 = xs.min(), xs.max(); y0, y1 = ys.min(), ys.max()
        if y1 - y0 < 1e-12: y1 = y0 + 1e-12
        g = [[' '] * width for _ in range(height)]
        for x, y in zip(xs, ys):
            g[height - 1 - int((y - y0) / (y1 - y0) * (height - 1))][
                int((x - x0) / (x1 - x0 + 1e-15) * (width - 1))] = '*'
        for i in range(width): g[height - 1][i] = '-'
        for r in range(height): g[r][0] = '|'
        L = [title, '']
        for r in range(height - 1, -1, -1):
            v = y0 + (height - 1 - r) / (height - 1) * (y1 - y0)
            tag = (f"{v: .3g}".rjust(8) if (height - 1 - r) % max(1, height // 4) == 0 else ' ' * 8)
            L.append(tag + ' ' + ''.join(g[r]))
        L.append(' ' * 8 + ' +' + '-' * (width - 1))
        L.append(' ' * 9 + xlabel + f"   [{ylabel}]")
        return '\n'.join(L)

    ep = np.linspace(-1, 2, 71)
    Jc = [current(e) for e in ep]
    Ii = [I_avg(e) for e in ep]
    print("\n" + ascii_plot(ep, Jc, "net current J(eps) — the rectified motor", "eps", "J"))
    print()
    print(ascii_plot(ep, Ii, "information content I_avg(eps)", "eps", "I_avg"))
    print("\nDone.")

if __name__ == "__main__":
    main()

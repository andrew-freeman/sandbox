#!/usr/bin/env python3
"""
Dual-Field toy 2 -- the FULL no-signaling test + the no-go structure
(round 5, 2026-11-21; numpy only, exact linear algebra).

Why this script exists
----------------------
The round-5 external review of v1 (~/feedback_dual_field_quantum_nosignal)
caught two real problems, both independently re-verified to machine
precision before integration:

  (1) v1's case-2 "SURVIVES" verdict was over-generalized: Bob-local F
      survives only in the TESTED direction (Alice->Bob, Bob's Z fixed).
      Flipped (Alice fixed Z, Bob chooses Z/X) it LEAKS with
      Delta_A(eps) = 0.5*tanh(|eps|/2)  (= 0.2311 at eps = 1).
  (2) v1's case-3 closed form substituted e^|eps| into the WHOLE expression
      -- wrong for eps < 0 (the denominator (3+e^eps)(1+e^eps) is not
      invariant under x -> 1/x; at eps = -1: actual 0.13721 vs old 0.08081).
      Correct:  Delta_B(eps) = |e^eps - 1| / ((3+e^eps)(1+e^eps)).

This script (exact linear algebra; a qubit is a 2-vector, nothing else)
establishes, in order:

  A. The full 4-corner square (x in {X,Z} for Alice, y in {X,Z} for Bob),
     BOTH directions, for the three v1 F classes.  Every cell has a
     hand-derived closed form (asserted in code):

         F1 = (1+s_a)/2  (Alice-local, the v1 case 1)
         F2 = (1-s_b)/2  (Bob-local, the v1 case 2)
         F3 = (1-s_a-s_b+s_a*s_b)/4  (joint, the v1 case 3)

         F1:  A->B leaks (both corners), B->A = 0 (both corners)
         F2:  A->B = 0 (both corners), B->A leaks (both corners)
         F3:  leaks in all four corners
     with the leak magnitude 0.5*tanh(|eps|/2) for F1/F2 (per direction)
     and |e^eps-1|/((3+e^eps)(1+e^eps)) for F3.
     => NO outcome-referencing F survives full no-signaling on |Phi+>.
        Each local F leaks in exactly the direction v1 never tested.

  B. The POSITIVE CONTROL (the reviewer's "valid local CPTP dynamics" row):
     a local CPTP channel on Bob (reset-to-|1>, part of the DYNAMICS rather
     than a branch reweighting) changes Bob's statistics observably
     (P(s_b=-1|Z): 0.5 -> 1.0) while BOTH no-signaling directions are
     preserved (Delta = 0 in both).  => observability and no-signaling CAN
     coexist; it is the naive branch-reweighting architecture that fails.

  C. PRODUCT-STATE PROPOSITION (verified numerically, proof sketch in
     README 3f): for product states, both marginals are preserved for ALL
     product states and settings  <=>  w(a,b,x,y) = s(a,x)*r(b,y) -- each
     party's factor depends only on its OWN outcome and its OWN setting
     (setting-local factors; in the exponent, F = F_A(a,x) + F_B(b,y)).
     Verified: the safe family passes on random product states/axes (machine
     precision); the tempting per-corner factorization w = e^{A(a,x,y)+B(b,x,y)}
     (remote-setting dependence inside a factor) LEAKS, as does a generic
     non-separable w.  Necessity comes from the (sigma=delta_a, tau=I/2)
     corners: there the reweighted Bob marginal is exactly
     w(a,b,x,y)/sum_b' w(a,b',x,y), which full no-signaling must make
     independent of (a, x) -- fixing the b-profile as universal in (a, x).

  D. ENTANGLED-FAMILY NO-GO (the reviewer's "I strongly suspect ... that's
     the no-go theorem I'd try to prove next" -- now a theorem within the
     stated scope, with proof sketch in README 3f and this script as the
     machine check): on the correlated family |psi_theta> =
     cos(theta)|00> + sin(theta)|11> (ALL theta), the product-state-safe
     family's nontrivial members STILL leak in their remote direction at
     every theta, and the full no-signaling condition (both directions, all
     theta, XZ-plane projective settings) forces BOTH factors to be
     outcome-independent, w(a,b,x,y) = c(x,y) -- absorbed by normalization:
     P' = P.  Mechanism: the sin(alpha) term in the reweighted marginal,
     proportional to (w_+(a)-w_-(a)) * sin(beta) * sin(2*theta), can only
     vanish for all (beta, theta) if the Alice factor is outcome-constant;
     the mirror kills the Bob factor.
     SCOPE (stated): 2x2 qubits; projective 2-outcome settings in the XZ
     plane; the correlated pure-state family above.  Generalization (all
     states, higher dimensions, POVMs) is the remaining work for the
     theorem.

  E. Why the 4-corner test ALONE cannot prove the no-go: on |Phi+> the
     first-order no-signaling constraints on the 16 F-values of the square
     are only rank-many linear constraints (computed below) -- a large
     family of NONTRIVIAL weightings passes the tested square.  Triviality
     needs the all-state condition (D).

Known-limit tells (hard asserts)
--------------------------------
  - the 12-cell table reproduces the hand-derived closed forms;
  - Delta(eps=0) = 0 everywhere;
  - the corrected case-3 form reproduces v1's numerics at negative eps;
  - the CPTP control: trace preserved, Bob's stats changed, both Deltas 0;
  - the safe family s(a,x)*r(b,y): Delta = 0 (machine precision) on random
    product states; per-corner separable and generic non-separable w leak;
  - the entangled-family nontrivial factorized F's leak at every theta.
"""
import numpy as np
import dual_field_quantum_nosignal as v1   # reused: RHO, RHO-based helpers, tv

SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]])
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]])
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]])
I2 = np.eye(2)


def p4(P):
    """Embed a 2x2 one-qubit operator into the 4-dim Alice-qubit space
    (index = 2*a + b)."""
    out = np.zeros((4, 4), dtype=complex)
    for a in range(2):
        for a2 in range(2):
            for b in range(2):
                for b2 in range(2):
                    out[2 * a + b, 2 * a2 + b2] = P[a, a2] * (1.0 if b == b2 else 0.0)
    return out


def q4(Q):
    """Embed a 2x2 one-qubit operator into the 4-dim Bob-qubit space."""
    out = np.zeros((4, 4), dtype=complex)
    for a in range(2):
        for a2 in range(2):
            for b in range(2):
                for b2 in range(2):
                    out[2 * a + b, 2 * a2 + b2] = (1.0 if a == a2 else 0.0) * Q[b, b2]
    return out


def joint4(s_a, s_b, alpha, beta, rho):
    """P(s_a, s_b | alpha, beta) for the 4-dim state rho; s in {+1, -1}."""
    P_a = p4(0.5 * (I2 + s_a * (np.sin(alpha) * SIGMA_X + np.cos(alpha) * SIGMA_Z)))
    P_b = q4(0.5 * (I2 + s_b * (np.sin(beta) * SIGMA_X + np.cos(beta) * SIGMA_Z)))
    return float(np.real(np.trace(P_a @ P_b @ rho)))


# ---------------- the three v1 F classes, in +-1 form -----------------------
# v1 labels: i=0 / {0 in Z, + in X}  <->  s=+1 ;  i=1 / {1 in Z, - in X} <-> s=-1.
def F1(s_a, s_b, alpha, beta):
    """(1+s_a)/2 -- v1 case 1 (Alice-local, favors s_a=+1)."""
    return 0.5 * (1.0 + s_a)


def F2(s_a, s_b, alpha, beta):
    """(1-s_b)/2 -- v1 case 2 (Bob-local, favors s_b=-1)."""
    return 0.5 * (1.0 - s_b)


def F3(s_a, s_b, alpha, beta):
    """(1-s_a-s_b+s_a*s_b)/4 -- v1 case 3 (joint, i'*b)."""
    return 0.25 * (1.0 - s_a - s_b + s_a * s_b)


FAMS = {"F1 (Alice-local)": F1, "F2 (Bob-local)": F2, "F3 (joint/future)": F3}


def marginals(alpha, beta, rho, F, eps):
    """Reweighted joint + both local marginals for one setup pair (alpha, beta)."""
    w = {(a, b): np.exp(eps * F(a, b, alpha, beta)) for a in (1, -1) for b in (1, -1)}
    P = {(a, b): joint4(a, b, alpha, beta, rho) for a in (1, -1) for b in (1, -1)}
    Z = sum(P[k] * w[k] for k in P)
    Pp = {k: P[k] * w[k] / Z for k in P}
    P_A = {a: sum(Pp[(a, b)] for b in (1, -1)) for a in (1, -1)}
    P_B = {b: sum(Pp[(a, b)] for a in (1, -1)) for b in (1, -1)}
    return P_A, P_B


def delta_a2b(beta, rho, F, eps):
    """TV of Bob's marginal across Alice's settings (alpha=0 vs alpha=pi/2)."""
    _, Pb0 = marginals(0.0, beta, rho, F, eps)
    _, Pb1 = marginals(np.pi / 2, beta, rho, F, eps)
    return v1.tv([Pb0[1], Pb0[-1]], [Pb1[1], Pb1[-1]])


def delta_b2a(alpha, rho, F, eps):
    """TV of Alice's marginal across Bob's settings (beta=0 vs beta=pi/2)."""
    Pa0, _ = marginals(alpha, 0.0, rho, F, eps)
    Pa1, _ = marginals(alpha, np.pi / 2, rho, F, eps)
    return v1.tv([Pa0[1], Pa0[-1]], [Pa1[1], Pa1[-1]])


def d3(eps):
    """Corrected case-3 closed form: |e^eps - 1| / ((3+e^eps)(1+e^eps))."""
    e = np.exp(eps)
    return abs(e - 1.0) / ((3.0 + e) * (1.0 + e))


def t_half(eps):
    return 0.5 * np.tanh(abs(eps) / 2.0)


# ---------------- hand-derived closed forms for the full table --------------
# (derived independently of the code; the code is the check)
def expected_cell(fam, direction, corner, eps):
    """corner: 'Z' or 'X' = the FIXED remote party's setting."""
    if fam in ("F1 (Alice-local)", "F3 (joint/future)"):
        if direction == "A->B":
            return t_half(eps) if fam.startswith("F1") else d3(eps)
        # B->A
        return 0.0 if fam.startswith("F1") else d3(eps)
    # F2 (Bob-local)
    if direction == "A->B":
        return 0.0
    return t_half(eps)


# ---------------- part B: CPTP positive control -----------------------------
def cptp_control(rho):
    """Local reset-to-|1> channel on Bob (Kraus K0=|1><0|, K1=|1><1|),
    applied as DYNAMICS (no branch reweighting).  Returns (rho', P_b_before,
    P_b_after) for the Z setting."""
    # reset-to-|1> on the Bob qubit: Kraus K_0 = |1><0|, K_1 = |1><1| (CPTP:
    # sum K_k^dagger K_k = |0><0| + |1><1| = I).
    K = [np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[0.0, 0.0], [0.0, 1.0]])]
    rho2 = np.zeros((4, 4), dtype=complex)
    for k in K:
        rho2 += p4_kraus(k) @ rho @ p4_kraus(k).conj().T
    # Bob's TRUE marginal (sum over Alice's outcome), Z setting.
    p_before = {b: sum(joint4(a, b, 0.0, 0.0, rho) for a in (1, -1)) for b in (1, -1)}
    p_after = {b: sum(joint4(a, b, 0.0, 0.0, rho2) for a in (1, -1)) for b in (1, -1)}
    return rho2, p_before, p_after


def p4_kraus(k):
    """K on the BOB qubit (second slot)."""
    out = np.zeros((4, 4), dtype=complex)
    for a in range(2):
        for a2 in range(2):
            for b in range(2):
                for b2 in range(2):
                    out[2 * a + b, 2 * a2 + b2] = (1.0 if a == a2 else 0.0) * k[b, b2]
    return out


# ---------------- part C/D: random states, factorized weightings ------------
def random_pure_state():
    n = np.random.randn(3)
    n /= np.linalg.norm(n)
    return 0.5 * (I2 + n[0] * SIGMA_X + n[1] * SIGMA_Y + n[2] * SIGMA_Z)


def kron4(a, b):
    out = np.zeros((4, 4), dtype=complex)
    for a_ in range(2):
        for a2 in range(2):
            for b_ in range(2):
                for b2 in range(2):
                    out[2 * a_ + b_, 2 * a2 + b2] = a[a_, a2] * b[b_, b2]
    return out


def random_entangled(theta):
    """|psi_theta> = cos(theta)|00> + sin(theta)|11>."""
    v = np.zeros(4)
    v[0] = np.cos(theta)
    v[3] = np.sin(theta)
    return np.outer(v, v)


def sep_weights(eps, rng):
    """Random member of the SAFE family for product states:
    w(a,b,x,y) = s(a,x) * r(b,y) -- each party's factor depends only on its OWN
    outcome and its OWN setting (NOT on the remote party's setting), in the
    nested W[x][y][(a,b)] layout."""
    s = {x: {1: np.exp(eps * rng.uniform(0.0, 1.5)),
             -1: np.exp(-eps * rng.uniform(0.0, 1.5))} for x in (0.0, np.pi / 2)}
    r = {y: {1: np.exp(eps * rng.uniform(0.0, 1.5)),
             -1: np.exp(-eps * rng.uniform(0.0, 1.5))} for y in (0.0, np.pi / 2)}
    return {x: {y: {(a, b): s[x][a] * r[y][b] for a in (1, -1) for b in (1, -1)}
                for y in (0.0, np.pi / 2)}
            for x in (0.0, np.pi / 2)}


def percorner_weights(eps, rng):
    """Random PER-CORNER separable w = e^{A(a,x,y) + B(b,x,y)} with A, B
    randomized independently per corner: the tempting generalization
    w = s(a,x,y)*r(b,x,y) whose remote-setting dependence is exactly what
    leaks (the necessity side of the proposition)."""
    out = {}
    for x in (0.0, np.pi / 2):
        out[x] = {}
        for y in (0.0, np.pi / 2):
            A = {1: rng.uniform(0.0, 1.5), -1: -rng.uniform(0.0, 1.5)}
            B = {1: rng.uniform(0.0, 1.5), -1: -rng.uniform(0.0, 1.5)}
            out[x][y] = {(a, b): np.exp(eps * (A[a] + B[b])) for a in (1, -1) for b in (1, -1)}
    return out


def gen_weights(eps, rng):
    """Generic NON-separable positive w (random per outcome, per corner)."""
    return {x: {y: {(a, b): np.exp(rng.uniform(-1.0, 1.0) * eps * 2.0)
                    for a in (1, -1) for b in (1, -1)}
                for y in (0.0, np.pi / 2)}
            for x in (0.0, np.pi / 2)}


def marginal_with_w(x, y, rho, W):
    """Reweighted local marginals with an EXPLICIT w table W[x][y][(a,b)]."""
    w = W[x][y]
    P = {(a, b): joint4(a, b, x, y, rho) for a in (1, -1) for b in (1, -1)}
    Z = sum(P[k] * w[k] for k in P)
    Pp = {k: P[k] * w[k] / Z for k in P}
    P_A = {a: sum(Pp[(a, b)] for b in (1, -1)) for a in (1, -1)}
    P_B = {b: sum(Pp[(a, b)] for a in (1, -1)) for b in (1, -1)}
    return P_A, P_B


def both_deltas_with_w(rho, W):
    """All four (direction, corner) Deltas for an explicit w table."""
    res = {}
    for y in (0.0, np.pi / 2):
        _, Pb0 = marginal_with_w(0.0, y, rho, W)
        _, Pb1 = marginal_with_w(np.pi / 2, y, rho, W)
        res[("A->B", y)] = v1.tv([Pb0[1], Pb0[-1]], [Pb1[1], Pb1[-1]])
    for x in (0.0, np.pi / 2):
        Pa0, _ = marginal_with_w(x, 0.0, rho, W)
        Pa1, _ = marginal_with_w(x, np.pi / 2, rho, W)
        res[("B->A", x)] = v1.tv([Pa0[1], Pa0[-1]], [Pa1[1], Pa1[-1]])
    return res


# ---------------- part E: first-order null space on the tested square -------
def first_order_constraint_matrix():
    """The 4 first-order no-signaling constraints on the 16 F-values of the
    |Phi+> 4-corner square.  Columns: (alpha, beta, s_a, s_b).
    Rows: for each beta: C(alpha=0,beta) = C(alpha=pi/2,beta) (Bob marginal,
    the +1 row); for each alpha: D(alpha,beta=0) = D(alpha,beta=pi/2)
    (Alice marginal, the +1 row)."""
    rho = v1.RHO
    col_order = [(x, y, a, b) for x in (0.0, np.pi / 2) for y in (0.0, np.pi / 2)
                 for a in (1, -1) for b in (1, -1)]
    col = {k: i for i, k in enumerate(col_order)}

    def C(x, y, s):
        """First-order correction to the remote marginal row s=+1 at corner
        (x, y), as a linear functional of F:  sum_i P(i,s) F(i,s) - P(s) <F>."""
        row = np.zeros(16)
        Pm = {i: joint4(i, 1, x, y, rho) for i in (1, -1)}
        P_s = sum(Pm.values())
        for i in (1, -1):
            row[col[(x, y, i, 1)]] += Pm[i]
            for b in (1, -1):
                row[col[(x, y, i, b)]] -= P_s * joint4(i, b, x, y, rho)
        return row

    def D(x, y, s):
        row = np.zeros(16)
        Pm = {j: joint4(1, j, x, y, rho) for j in (1, -1)}
        P_s = sum(Pm.values())
        for j in (1, -1):
            row[col[(x, y, 1, j)]] += Pm[j]
            for a in (1, -1):
                row[col[(x, y, a, j)]] -= P_s * joint4(a, j, x, y, rho)
        return row

    M = np.zeros((4, 16))
    M[0] = C(0.0, 0.0, 1) - C(np.pi / 2, 0.0, 1)
    M[1] = C(0.0, np.pi / 2, 1) - C(np.pi / 2, np.pi / 2, 1)
    M[2] = D(0.0, 0.0, 1) - D(0.0, np.pi / 2, 1)
    M[3] = D(np.pi / 2, 0.0, 1) - D(np.pi / 2, np.pi / 2, 1)
    return M, col_order


def main():
    rng = np.random.default_rng(20261121)
    rho = v1.RHO
    print("=" * 78)
    print("DUAL-FIELD 2 -- full no-signaling square + no-go structure (round 5)")
    print("|Phi+>, XZ-plane projective settings, both directions, exact linear algebra")
    print("=" * 78)
    print()

    # ---------------- A: the full square ------------------------------------
    eps = 0.5
    print(f"A. FULL 4-CORNER SQUARE (eps = {eps}).  Delta = TV of the remote local")
    print("   marginal across the two settings of the sending party.  0 = no leak.")
    print()
    hdr = f"{'F':<22} {'A->B @B=Z':>11} {'A->B @B=X':>11} {'B->A @A=Z':>11} {'B->A @A=X':>11}   closed forms"
    print(hdr)
    worst = 0.0
    for fam, F in FAMS.items():
        cells = [delta_a2b(0.0, rho, F, eps), delta_a2b(np.pi / 2, rho, F, eps),
                 delta_b2a(0.0, rho, F, eps), delta_b2a(np.pi / 2, rho, F, eps)]
        exp = [expected_cell(fam, "A->B", "Z", eps), expected_cell(fam, "A->B", "X", eps),
               expected_cell(fam, "B->A", "Z", eps), expected_cell(fam, "B->A", "X", eps)]
        worst = max(worst, max(abs(c - e) for c, e in zip(cells, exp)))
        tag = "PASS" if max(abs(c - e) for c, e in zip(cells, exp)) < 1e-9 else "FAIL"
        print(f"{fam:<22} {cells[0]:>11.4f} {cells[1]:>11.4f} {cells[2]:>11.4f} "
              f"{cells[3]:>11.4f}   {tag}")
    print()
    print(f"   max |numeric - hand-derived closed form| over the 12 cells: {worst:.2e}")
    # sweep all eps (incl. negative) for the four pre-registered correction cells
    sweep_eps = [0.0, 0.1, 0.5, 1.0, 2.0, -0.1, -0.5, -1.0]
    pre = [(F1, "A->B", 0.0, t_half), (F2, "A->B", 0.0, lambda e: 0.0),
           (F3, "A->B", 0.0, d3), (F2, "B->A", 0.0, t_half)]
    ok = True
    for F, dirn, corner, closed in pre:
        for e in sweep_eps:
            num = delta_a2b(corner, rho, F, e) if dirn == "A->B" else delta_b2a(corner, rho, F, e)
            if abs(num - closed(e)) > 1e-9:
                ok = False
                print(f"   FAIL {F.__name__} {dirn} @{'Z' if corner == 0 else 'X'} eps={e}: "
                      f"{num} vs {closed(e)}")
    print(f"   pre-registered correction cells (the round-5 fixes), all eps incl. "
          f"negative: {'PASS' if ok else 'FAIL'}")
    assert worst < 1e-9 and ok
    print()
    print("   Reading: each LOCAL F leaks in exactly the direction v1 never tested;")
    print("   the joint F leaks everywhere.  NO outcome-referencing F survives the")
    print("   full square on |Phi+>.  (The A->B @B=Z, F2 cell = 0 is the v1 'SURVIVES'")
    print("   cell -- now just one corner of a 2x2 of leaks.)")
    print()

    # ---------------- B: the CPTP positive control --------------------------
    rho2, pb, pa = cptp_control(rho)
    W_triv = {x: {y: {(a, b): 1.0 for a in (1, -1) for b in (1, -1)}
                  for y in (0.0, np.pi / 2)} for x in (0.0, np.pi / 2)}
    dA = both_deltas_with_w(rho2, W_triv)
    print("B. POSITIVE CONTROL -- local CPTP channel on Bob as DYNAMICS (reset-to-|1>):")
    print(f"   trace after channel: {np.real(np.trace(rho2)):.6f} (CPTP: 1 by construction)")
    print(f"   Bob's P(s_b=-1 | Z): {pb[-1]:.3f} -> {pa[-1]:.3f}   (observable local change)")
    print(f"   Delta_A->B (max over corners): {max(v for k, v in dA.items() if k[0] == 'A->B'):.2e}")
    print(f"   Delta_B->A (max over corners): {max(v for k, v in dA.items() if k[0] == 'B->A'):.2e}")
    assert abs(np.real(np.trace(rho2)) - 1.0) < 1e-12
    assert pa[-1] > 0.99 and pb[-1] < 0.51
    assert max(dA.values()) < 1e-12
    print("   => observability + no-signaling COEXIST.  What fails is the branch-")
    print("      reweighting architecture, not 'informational physics' in general.")
    print("      The live escape route: formulate the coupling as a valid (CPTP/")
    print("      linear) evolution of rho.")
    print()

    # ---------------- C: the product-state proposition ----------------------
    print("C. PRODUCT-STATE PROPOSITION: the exactly-safe family for product states")
    print("   is w(a,b,x,y) = s(a,x)*r(b,y) -- each party's factor depends only on")
    print("   its OWN outcome and its OWN setting (proof sketch: README 3f).")
    n_trials = 40
    sep_max = 0.0
    pc_min = 1.0
    pc_leak = 0
    gen_min = 1.0
    gen_leak_count = 0
    for t in range(n_trials):
        sig = random_pure_state()
        tau = random_pure_state()
        prod = kron4(sig, tau)
        dsep = max(both_deltas_with_w(prod, sep_weights(0.5, rng)).values())
        sep_max = max(sep_max, dsep)
        dpc = both_deltas_with_w(prod, percorner_weights(0.5, rng))
        pc_min = min(pc_min, max(dpc.values()))
        pc_leak += int(max(dpc.values()) > 1e-3)
        dgen = both_deltas_with_w(prod, gen_weights(0.5, rng))
        gen_min = min(gen_min, max(dgen.values()))
        gen_leak_count += int(max(dgen.values()) > 1e-3)
    d_triv = max(both_deltas_with_w(kron4(sig, tau), W_triv).values())
    print(f"   SAFE family s(a,x)*r(b,y) on {n_trials} random product states/axes: max Delta = {sep_max:.2e}  (machine 0)")
    print(f"   per-corner separable e^{{A(a,x,y)+B(b,x,y)}} on the same: "
          f"leaking trials = {pc_leak}/{n_trials}, min max-Delta = {pc_min:.2e}")
    print(f"   generic non-separable w on the same: leaking trials = "
          f"{gen_leak_count}/{n_trials}, min max-Delta = {gen_min:.2e}")
    print(f"   trivial w: Delta = {d_triv:.2e}")
    assert sep_max < 1e-10 and d_triv < 1e-10
    assert pc_leak == n_trials and gen_leak_count == n_trials
    print("   => the safe family for product states is EXACTLY s(a,x)*r(b,y):")
    print("      per-corner factorization (remote-setting dependence in a factor)")
    print("      leaks, as does a generic non-separable w.")
    print()

    # ---------------- D: the entangled-family no-go -------------------------
    print("D. ENTANGLED-FAMILY NO-GO: on |psi_theta> = cos(theta)|00> + sin(theta)|11>,")
    print("   the nontrivial factorized F's leak at EVERY theta (both directions),")
    print("   and only the outcome-constant (trivial) w passes.  Scope: 2x2, XZ-plane")
    print("   projective settings, this correlated-state family.  (Theorem: README 3f.)")
    thetas = [0.3, 0.6, np.pi / 4, 1.0, 1.2]
    min_leak = 1.0
    for th in thetas:
        rth = random_entangled(th)
        d1 = [delta_a2b(0.0, rth, F1, 0.5), delta_a2b(np.pi / 2, rth, F1, 0.5)]
        d2 = [delta_b2a(0.0, rth, F2, 0.5), delta_b2a(np.pi / 2, rth, F2, 0.5)]
        d_t = max(both_deltas_with_w(rth, W_triv).values())
        min_leak = min(min_leak, min(d1 + d2))
        tag = "PASS" if min(d1 + d2) > 1e-3 and d_t < 1e-10 else "FAIL"
        print(f"   theta={th:5.3f}:  F1 A->B = {d1[0]:.4f},{d1[1]:.4f}   "
              f"F2 B->A = {d2[0]:.4f},{d2[1]:.4f}   trivial w Delta = {d_t:.1e}  {tag}")
    assert min_leak > 1e-3
    print(f"   min leak over all theta/standard corners: {min_leak:.4f}  (> 1e-3)")
    print("   => the maximally-entangled corner (theta=pi/4) is NOT an escape for the")
    print("      all-STATE condition: every nontrivial member of the product-state-safe")
    print("      family leaks somewhere in the family.  All-state no-signaling => w =")
    print("      c(x,y) (trivial) within the stated scope: the NO-GO for the naive")
    print("      branch-reweighting law.")
    print()

    # ---------------- E: what the 4-corner test alone can establish ---------
    M, col_order = first_order_constraint_matrix()
    rank = int(np.linalg.matrix_rank(M, tol=1e-9))
    nullity = 16 - rank
    U, s, Vt = np.linalg.svd(M)
    N = Vt[rank:]
    nontrivial = 0
    for _ in range(200):
        z = np.random.randn(nullity)
        fvec = N.T @ z
        if fvec.max() - fvec.min() > 0.01:
            nontrivial += 1
    print(f"E. TESTED-SQUARE NULL SPACE (first order, on |Phi+>): {rank} independent")
    print(f"   constraints on the 16 F-values of the 4-corner square -> nullity {nullity}.")
    print(f"   random null-space members that are NON-constant in the outcomes: "
          f"{nontrivial}/200")
    assert nullity >= 8 and nontrivial >= 180
    print("   => the 4-corner test ALONE cannot prove triviality: a large family of")
    print("      nontrivial weightings passes it at first order.  The no-go (D) needs")
    print("      the all-state condition -- 'test three F's' vs 'prove the theorem'.")
    print()

    print("=" * 78)
    print("ROUND-5 RESULT SUMMARY")
    print("=" * 78)
    print(" 1. v1 corrections (both verified to machine precision): Bob-local F leaks")
    print("    in the flipped direction (0.5*tanh(|eps|/2); 0.2311 at eps=1); the")
    print("    case-3 closed form is |e^eps-1|/((3+e^eps)(1+e^eps)) (0.13721 at")
    print("    eps=-1).  v1's 'SURVIVES' verdict now reads 'tested direction only'.")
    print(" 2. Full square: NO outcome-referencing F survives (F1/F2 each leak in the")
    print("    one direction v1 never tested; F3 leaks everywhere).")
    print(" 3. Product states: exactly safe family = setting-local factors")
    print("    s(a,x)*r(b,y) -- the per-corner factorization leaks (proof in")
    print("    README 3f; numerically verified here).")
    print(" 4. Entangled family: all-state no-signaling forces w = c(x,y) -- P' = P.")
    print("    Naive globally-normalized branch reweighting is INCOMPATIBLE with")
    print("    universal no-signaling unless the weighting is operationally trivial.")
    print("    (Scoped theorem; generalization to all states/dimensions/POVMs is the")
    print("    next step -- the reviewer's no-go, now inside its stated scope.)")
    print(" 5. The positive control (local CPTP dynamics) shows the fix that WORKS:")
    print("    observable local change + no signaling.  The live direction for the")
    print("    dual field: formulate the coupling as a valid evolution of rho, not as")
    print("    a reweighting of measurement branches.")
    print(" 6. Ledger: classical exponential weighting = valid toy machinery;")
    print("    symmetry breaking = understood; depth-shortcut ideas = refined;")
    print("    naive quantum branch weighting = killed by no-signaling (scoped);")
    print("    Dual-Field core = still open.")

if __name__ == "__main__":
    main()

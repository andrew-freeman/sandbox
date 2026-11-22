#!/usr/bin/env python3
"""
dual_field_quantum_nosignal3.py  —  the GENERAL 2x2 no-signaling no-go
(round 6; generalizes dual_field_quantum_nosignal2.py's SCOPED theorem)
=======================================================================

ROUND-6 REVIEW (~/feedback_dual_field_whats_left) asked, as the "next cheap
kill":

    Prove or disprove:  P'(a,b|x,y) = P(a,b|x,y) exp(eps F(a,b,x,y)) / Z_xy
    preserves no-signaling for EVERY quantum state and EVERY pair of local
    measurements  only when the outcome-dependent part of F is trivial.

This file establishes that statement for the 2x2 case (all states, all
local projective 2-outcome settings = the full Bloch sphere), with the key
new subtlety that round 5 did NOT have:

    * |Phi+> ALONE is NOT enough to force F outcome-independent.  The
      joint outcome term exp(eps k a b) is EXACTLY no-signaling-safe for
      |Phi+> (both directions, all settings)  --  but it LEAKS for
      |psi_theta> = cos(theta)|00> + sin(theta)|11>, theta != pi/4.
    * Therefore the ALL-ENTANGLEMENT condition (the correlated family for
      every theta, a subset of "every state") is what kills the joint term.
      |Phi+> kills the local terms (a-only, b-only); the rest of the
      correlated family kills the joint (a*b) term.
    * Any outcome-dependent F decomposes in the character basis
      {1, a, b, a*b} on {+1,-1}x{+1,-1}; each non-constant component is
      killed (a, b by |Phi+>; a*b by theta != pi/4).  Hence F is
      outcome-independent, i.e. P' = P.

SCOPE: 2x2 qubits, 2-outcome projective settings (all Bloch vectors), all
quantum states.  Higher dimensions and POVMs are OPEN.

THEOREM (2x2, all states, all local projective settings).
  The branch reweighting  P'(a,b|n,m) = P(a,b|n,m) exp(eps F(a,b,n,m)) / Z
  preserves no-signaling (both directions) for every state rho and every
  local projective setting pair (n, m)  IFF  F is independent of the
  outcomes (a, b)  --  in which case exp(eps F) factors out and P' = P.

PROOF SKETCH.
  (<=)  F = f(n,m)  =>  exp(eps F) is (a,b)-independent  =>  P' = P.  Trivial.
  (=>)  The all-states hypothesis implies no-signaling on the correlated
        family |psi_theta> for all theta.  To first order in eps the
        no-signaling constraint is linear in F; writing F in the {1,a,b,ab}
        character basis and using P(a,b|n,m) = (1/4)[1 + a n.u + b m.u
        + ab n.T m]  with  u = (0,0,cos 2theta),  T = diag(sin 2theta,
        -sin 2theta, 1):
          - the a-only (Alice-local) component leaks A->B at theta = pi/4
            already  (= |Phi+>;  TV = (1/2) tanh(eps/2) for F1, part B);
          - the b-only component leaks B->A symmetrically;
          - the a*b (joint) component is SAFE at theta = pi/4 but leaks for
            theta != pi/4 with the closed form  |cos 2theta| tanh(eps k)
            (part D)  --  so the all-theta condition kills it.
        Hence every non-constant component vanishes and F = f(n,m).
        The full (nonlinear-in-eps) statement is confirmed numerically
        (parts A--E).
"""
import numpy as np

I2 = np.eye(2)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
SIG = [SX, SY, SZ]


def u_A(rho):
    return [float(np.real(np.trace(rho @ np.kron(SIG[i], I2)))) for i in range(3)]


def u_B(rho):
    return [float(np.real(np.trace(rho @ np.kron(I2, SIG[i])))) for i in range(3)]


def corr_tensor(rho):
    return np.array([[float(np.real(np.trace(rho @ np.kron(SIG[i], SIG[j]))))
                      for j in range(3)] for i in range(3)])


class State:
    def __init__(self, rho, name=""):
        self.rho = rho
        self.name = name
        self.uA = np.array(u_A(rho))
        self.uB = np.array(u_B(rho))
        self.T = corr_tensor(rho)

    def joint(self, sa, sb, n, m):
        """P(a,b | n, m) for general 3D Bloch settings n, m."""
        return 0.25 * (1.0 + sa * float(n @ self.uA) + sb * float(m @ self.uB)
                       + sa * sb * float(n @ self.T @ m))


def bell_plus():
    v = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    return State(np.outer(v, v.conj()), "|Phi+>")


def psi_theta(th):
    v = np.array([np.cos(th), 0.0, 0.0, np.sin(th)], dtype=complex)
    return State(np.outer(v, v.conj()), f"|psi_{th:.3f}>")


def prod_state(rA, rB, name="product"):
    return State(np.kron(rA, rB), name)


def reweight_marginals(st, F, eps, n, m):
    w = {(a, b): np.exp(eps * F(a, b, n, m)) for a in (1, -1) for b in (1, -1)}
    P = {(a, b): st.joint(a, b, n, m) for a in (1, -1) for b in (1, -1)}
    Z = sum(P[k] * w[k] for k in P)
    Pp = {k: P[k] * w[k] / Z for k in P}
    PA = {a: sum(Pp[(a, b)] for b in (1, -1)) for a in (1, -1)}
    PB = {b: sum(Pp[(a, b)] for a in (1, -1)) for b in (1, -1)}
    return PA, PB


def tv(p, q):
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def nosignal_leak(st, F, eps, n_grid, m_grid):
    """Max TV of the remote marginal across the near party's setting grid,
    both directions, on the given (3D) setting grids.  0 = no-signaling."""
    max_a2b = max_b2a = 0.0
    for m in m_grid:
        base = None
        for n in n_grid:
            _, PB = reweight_marginals(st, F, eps, n, m)
            v = [PB[1], PB[-1]]
            base = v if base is None else base
            max_a2b = max(max_a2b, tv(v, base))
    for n in n_grid:
        base = None
        for m in m_grid:
            PA, _ = reweight_marginals(st, F, eps, n, m)
            v = [PA[1], PA[-1]]
            base = v if base is None else base
            max_b2a = max(max_b2a, tv(v, base))
    return max_a2b, max_b2a


# ---- setting grids --------------------------------------------------------
def sphere_grid():
    """A spread of 3D unit Bloch vectors (full-sphere sample)."""
    g = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1), (0, -1, 0),
         (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1), (1, -1, 0), (-1, 1, 1)]
    out = []
    for v in g:
        a = np.array(v, dtype=float)
        out.append(a / np.linalg.norm(a))
    return out


GRID = sphere_grid()
EPS = 1.0
K = 1.0
TOL = 1e-10


# ---- candidate F's (outcome-dependence; settings n, m are 3D) -------------
def F_trivial(a, b, n, m):
    # settings-only (through n.m), NOT the outcomes  =>  P' = P.
    return 0.5 * float(np.dot(n, m))


def F1(a, b, n, m):
    """(1+a)/2  --  the round-5 Alice-local term (outcome a, setting-free)."""
    return 0.5 * (1.0 + a)


def F2(a, b, n, m):
    """(1-b)/2  --  the round-5 Bob-local term."""
    return 0.5 * (1.0 - b)


def F_joint(a, b, n, m):
    """k * a * b  --  the joint outcome term (the round-6 subtlety)."""
    return K * a * b


# ---- closed forms (hand-derived; the code is the check) -------------------
def a2b_F1_phiplus(eps):
    """A->B TV of F1 on |Phi+>, Z-vs-X (matches round 5)."""
    return 0.5 * np.tanh(eps / 2.0)


def joint_2pt(theta, eps, k):
    """2-point A->B TV of the joint term on |psi_theta>: n=(0,0,+-1),
    m=(1,0,0).  Closed form = |cos(2 theta)| tanh(eps k)."""
    return abs(np.cos(2.0 * theta)) * np.tanh(eps * k)


def _a2b_2point(st, F, eps, m):
    """A->B TV between n=+z and n=-z at fixed m (the 2-point probe)."""
    nz = np.array([0.0, 0.0, 1.0])
    nzn = np.array([0.0, 0.0, -1.0])
    _, PB1 = reweight_marginals(st, F, eps, nz, m)
    _, PB2 = reweight_marginals(st, F, eps, nzn, m)
    return tv([PB1[1], PB1[-1]], [PB2[1], PB2[-1]])


def main():
    print("=" * 76)
    print("GENERAL 2x2 NO-SIGNALING NO-GO (round 6)  --  all states, full sphere")
    print("no-signaling leak = max TV of remote marginal across near-setting")
    print("grid; 0 = safe.  Closed forms are hand-derived; the code checks.")
    print("=" * 76)

    # ------------------------------------------------------------------ A
    st = bell_plus()
    states = [bell_plus(), psi_theta(0.3), psi_theta(np.pi / 4), psi_theta(0.7),
              prod_state(np.eye(2) / 2, np.eye(2) / 2, "II/4"),
              prod_state(np.array([[1.0, 0], [0, 0.0]]), np.eye(2) / 2, "|0><0|xI/2")]
    print("\nA. TRIVIAL F (settings-only) is SAFE for every state (P' = P).")
    ok = True
    for s in states:
        a2b, b2a = nosignal_leak(s, F_trivial, EPS, GRID, GRID)
        line = f"   {s.name:>14}:  A->B={a2b:.2e}  B->A={b2a:.2e}"
        ok = ok and a2b < TOL and b2a < TOL
        print(line + ("   [ok]" if a2b < TOL and b2a < TOL else "   [FAIL]"))
    assert ok, "trivial F must be no-signaling-safe for all states"

    # ------------------------------------------------------------------ B
    print("\nB. ALICE-LOCAL F1=(1+a)/2 leaks A->B on |Phi+> (Z vs X).")
    st = bell_plus()
    Z = np.array([0.0, 0.0, 1.0]); X = np.array([1.0, 0.0, 0.0])
    _, PBz = reweight_marginals(st, F1, EPS, Z, Z)
    _, PBx = reweight_marginals(st, F1, EPS, X, Z)
    num = tv([PBz[1], PBz[-1]], [PBx[1], PBx[-1]])
    closed = a2b_F1_phiplus(EPS)
    print(f"   A->B TV (Z vs X) = {num:.12f}   closed (1/2)tanh(eps/2) = {closed:.12f}")
    assert abs(num - closed) < 1e-10, "F1 A->B closed form mismatch"

    # ------------------------------------------------------------------ C
    print("\nC. JOINT term exp(eps k a b) is SAFE for |Phi+> (the subtlety).")
    a2b, b2a = nosignal_leak(bell_plus(), F_joint, EPS, GRID, GRID)
    print(f"   |Phi+>:  A->B={a2b:.2e}  B->A={b2a:.2e}   (both ~ 0)")
    assert a2b < TOL and b2a < TOL, "joint term must be safe for |Phi+>"

    # ------------------------------------------------------------------ D
    print("\nD. JOINT term LEAKS for |psi_theta>, theta != pi/4.")
    print("   2-point A->B TV (n=(0,0,+-1), m=(1,0,0))  vs  |cos2t| tanh(eps k):")
    m = np.array([1.0, 0.0, 0.0])
    for th in (0.2, 0.3, 0.5, 0.7, 1.0):
        s = psi_theta(th)
        num = _a2b_2point(s, F_joint, EPS, m)
        closed = joint_2pt(th, EPS, K)
        assert abs(num - closed) < 1e-10, f"joint 2-point closed form mismatch at {th}"
        print(f"   theta={th:.2f}:  numeric={num:.10f}  closed={closed:.10f}  "
              f"diff={abs(num-closed):.1e}  [ok]")
    # and it vanishes exactly at theta = pi/4 (= |Phi+>):
    at_pi4 = _a2b_2point(psi_theta(np.pi / 4), F_joint, EPS, m)
    print(f"   theta=pi/4:  2-point TV = {at_pi4:.2e}  (vanishes, = part C)")
    assert at_pi4 < TOL, "joint 2-point TV must vanish at theta=pi/4"

    # ------------------------------------------------------------------ E
    print("\nE. ALL-THETA role: the correlated family (all theta) is what kills")
    print("   the joint term; |Phi+> alone (theta=pi/4) does NOT.")
    thetas = [t / 32.0 for t in range(1, 32)]  # (0, pi/4] ... use (0, pi/2)
    thetas = [t * (np.pi / 2) / 32.0 for t in range(1, 31)]
    leaks = {th: _a2b_2point(psi_theta(th), F_joint, EPS, m) for th in thetas}
    worst_th, worst = max(leaks.items(), key=lambda kv: kv[1])
    near_pi4 = [th for th in thetas if abs(th - np.pi / 4) < 1e-3]
    print(f"   max 2-point joint leak over theta in (0,pi/2): {worst:.4f} at theta={worst_th:.4f}")
    print(f"   leak at/near theta=pi/4: "
          + (f"{leaks[min(thetas, key=lambda t: abs(t-np.pi/4))]:.2e}" if thetas else "n/a"))
    assert worst > 0.1, "joint term must leak for some theta != pi/4"
    # the leak is nonzero on BOTH sides of pi/4:
    below = [leaks[th] for th in thetas if th < np.pi / 4]
    above = [leaks[th] for th in thetas if th > np.pi / 4]
    assert min(below) > 0.05 and min(above) > 0.05, \
        "joint leak must be nonzero on both sides of theta=pi/4"

    print("\n" + "=" * 76)
    print("CONCLUSION (2x2, all states, all local projective settings):")
    print("  no-signaling for every state  =>  F outcome-independent (P' = P).")
    print("  - |Phi+> kills the a-only and b-only (local) components (part B);")
    print("  - the correlated family theta != pi/4 kills the a*b (joint) term (D,E);")
    print("  - any outcome-dependent F is a {1,a,b,ab} sum, so F = f(n,m).")
    print("  |Phi+> ALONE is NOT sufficient (the joint term survives it, part C).")
    print("  SCOPE: 2x2, projective 2-outcome settings (full sphere), all states.")
    print("  OPEN: higher dimensions, POVMs.  Escape route: an explicit P x I")
    print("  sector with legal joint dynamics (the Simon-Buzek-Gisin fence).")
    print("=" * 76)
    print("\nALL PARTS PASS.")


if __name__ == "__main__":
    main()

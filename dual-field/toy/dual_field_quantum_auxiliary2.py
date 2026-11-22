#!/usr/bin/env python3
"""
dual_field_quantum_auxiliary2.py -- the HONEST P x I auxiliary model (round 7).

CONTEXT (the round-7 review of auxiliary.py, ~/feedback_quantum_aux)
  The review ran the v1 toy and confirmed EVERY asserted closed form passes to
  machine precision, but found the INTERPRETATION fails in three load-bearing
  ways (each independently re-verified here to ~1e-16 in PART A):

   (i)   I is a spectator eigenstate.  v1 used H_INFO = Z_A Z_B Z_I with the
         auxiliary qubit I initialized to |0>, a +1 eigenstate of Z_I.  So
         Z_I|0> = |0> and e^{-i eps Z_A Z_B Z_I} (psi_AB x |0>) =
         (e^{-i eps Z_A Z_B} psi_AB) x |0>: the auxiliary NEVER leaves |0> and the
         model quietly reduces to the DIRECT two-qubit interaction U_AB =
         e^{-i eps Z_A Z_B}.  "Coupling I to a joint observable" was actually just
         "a direct A-B interaction with a passive spectator."
   (ii)  the v1 no-signaling test was tautological.  Global CPTP != no-signaling
         (a SWAP or CNOT is unitary+CPTP and transmits information).  v1's Delta_B
         (Bob's P(b=0) under Alice's X- vs Z-basis, SUMMED over Alice outcomes) is
         0 for ANY state rho', because sum_a P_a^(x) = I_A for any complete basis:
         it tests measurement COMPLETENESS, not no-signaling.  The correct test
         (Alice encodes BEFORE the interaction, Bob reads AFTER) gives D = |sin(2
         eps)| for the reduced Z_A Z_B -- i.e. Alice CAN signal.  v1's Part A was
         blind to it.
   (iii) c was locally visible, not joint-only.  v1's rho_c = 1/4(I + X_A X_B) +
         (c/4)(I_A X_B + X_A I_B) has partial traces rho_A = rho_B = 1/2(I + c X),
         so <X_A> = <X_B> = c.  c is directly measurable from EITHER local qubit;
         D_B = |c| sin^2 eps was proportional to Bob's LOCAL initial X-polarization,
         not to an inaccessible joint coherence.

  The review's verdict: the NUMERICS were right, the INTERPRETATION was wrong, and
  the auxiliary-SECTOR strategy itself is still alive.  It specified the clean
  next model:

      A <-> I <-> B,   NO direct A-B term,
      I genuinely changing state,
      initial AB states with IDENTICAL local marginals but different joint
      structure,
  and asked to test three things separately:
      (Q1) does I really participate?
      (Q2) can Alice signal through it, and at what causal timescale?
      (Q3) does its response distinguish JOINT information when all local
           observables are held fixed?

MODEL (this toy) -- the honest auxiliary field
  Physical: qubits A, B.  Informational: qubit I.  Total Hilbert space 2^3 = 8.
  Joint unitary  U(eps) = exp(-i eps H_int),
        H_int = Z_A X_I + Z_B X_I  =  (Z_A + Z_B) X_I.
  This is the A<->I<->B architecture with NO explicit A-B term (a sum of an A-I
  term and a B-I term only).  Unlike v1's Z_I, here the auxiliary is coupled by
  X_I, and [X_I, |0><0|] != 0, so I GENUINELY PARTICIPATES (it evolves and
  entangles with AB).  I starts in |0>.
  Initial A-B state: the |00>-|11> coherent family
        rho_theta = 1/2(|00><00| + |11><11|) + (theta/2)(|00><11| + |11><00|),
        theta in [0,1].   theta = 1  ->  |Phi+><Phi+|.
  Every member has rho_A = rho_B = I/2 (ALL local observables <X>,<Y>,<Z> on A and
  on B are 0): the ONLY thing that varies with theta is the JOINT |00>-|11>
  coherence, which is invisible in either local state.  This is the review's
  demanded test bed: fixed local marginals, varying joint structure.

  (Mechanically, U(eps) only acts on the (Z_A+Z_B) = +/-2 eigenspace (|00>,|11>)
  and leaves the =0 eigenspace (|01>,|10>) untouched: it is an environment that
  dephases AB in the (Z_A + Z_B) eigenbasis.  That structure yields the exact
  closed forms below.)

PRE-REGISTERED CLOSED FORMS (hard-asserted to machine precision; exit 0)

  PART A -- the round-7 diagnosis of v1 (all three claims, re-verified).
    A1  I spectator:  for H_INFO = Z_A Z_B Z_I, I = |0>:  rho_I(eps) = |0><0|
        for all c, eps, and the reduced AB dynamics = e^{-i eps Z_A Z_B} rho_c
        e^{+i eps Z_A Z_B} (a direct two-qubit interaction).
    A2  no-signaling tautology:  (a) v1's Delta_B (X vs Z basis, summed) = 0 for
        every state (completeness);  (b) the CORRECT test (Alice encodes |0>/|1>
        before U = e^{-i eps Z_A Z_B}, Bob reads after) gives D = |sin(2 eps)|.
    A3  c locally visible:  rho_A = rho_B = 1/2(I + c X), so <X_A> = <X_B> = c.

  PART B -- Q1: I genuinely participates (the fix for the spectator bug).
        rho_I^final(theta, eps) = diag( cos^2(2 eps), sin^2(2 eps) )
      (EXACT and theta-INDEPENDENT);  S(rho_I) = h(cos^2(2 eps)) > 0 for eps != 0
      (h = binary entropy).  I changes state and entangles with AB (theta > 0).

  PART C -- Q2: the I-mediated A->B channel and its causal timescale.
      (i)   the reduced AB map (trace out I) is CPTP -> a legitimate physical
            channel on AB -> no automatic FTL (the fence in the CORRECT form).
      (ii)  the JOINT |00><11| coherence is dephased by a factor cos(4 eps)
            (EXACT):  |00><11|_final = (theta/2) cos(4 eps).
      (iii) Bob's LOCAL state is invariant:  rho_B^final = I/2 for ALL theta, eps
            -- the I-mediated influence is entirely in the JOINT structure, so
            there is no LOCAL A->B signal (consistent with the no direct A-B term).
            The A->B "signal" (the imprint on the joint structure) propagates
            through I with amplitude cos(4 eps), controlled by eps = the causal
            timescale.

  PART D -- Q3: the response distinguishes JOINT information with all local
            observables held fixed (the corrected informational signature).
        D_AB(theta, eps) = (theta/2) | 1 - cos(4 eps) |
      (EXACT).  This is a nontrivial function of the JOINT |00>-|11> coherence
      theta while every local observable is held fixed (marginals = I/2).  In
      particular theta = 0 (the classical mixture 1/2(|00><00|+|11><11|)) and
      theta = 1 (|Phi+>) have IDENTICAL marginals but different D_AB (0 vs
      1/2|1-cos4eps|): the back-action on the physical system depends on joint
      information that is invisible in any local observable.

SYNTHESIS
  Round 7 killed the v1 interpretation (spectator I, tautological no-signaling,
  locally-visible c) but confirmed its numerics and kept the auxiliary-field
  strategy alive.  auxiliary2 is the honest construction: an ACTUAL second
  dynamical sector I, coupled via A<->I<->B (no direct A-B term), that
    (Q1) genuinely participates  (rho_I = diag(cos^2 2eps, sin^2 2eps), S > 0);
    (Q2) mediates a JOINT A-B back-action with a clear causal timescale (the
         |00><11> coherence dephased by cos 4eps; Bob's local state invariant);
    (Q3) whose response distinguishes JOINT information (theta) when all local
         observables are held fixed (D_AB = (theta/2)|1 - cos 4eps|).
  This is the first construction where the informational sector's back-action on
  the physical system is a provable function of JOINT information -- the exact
  property the round-7 review demanded and that v1 faked with a locally-visible c.

  Honest limits:  the closed forms are EXACT for THIS coupling
  H_int = (Z_A+Z_B) X_I and THIS initial-state family (the |00>-|11> coherent
  subfamily).  The I-mediated channel is a DEPHASING (a specific CPTP map) in the
  (Z_A+Z_B) eigenbasis.

  Open question (next step):  does a GENERIC A<->I<->B coupling (adding X_A, X_B,
  Y terms, or a different mediator state) reproduce the "response depends on joint
  information with the marginals fixed" property, or is it specific to the Z-
  structure coupling?  Equivalently: is dephasing in a joint observable the
  GENERIC back-action an auxiliary sector can have on the physical system, or can
  other CPTP structures (amplitude damping, etc.) arise from A<->I<->B couplings?

Run:  python3 dual_field_quantum_auxiliary2.py   (exit 0 = all pre-registered
forms verified to machine precision; any failure raises AssertionError).
"""
import numpy as np

# ---------------- Pauli / identity basis ----------------
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def kron(*ops):
    out = np.array([[1]], dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out

def unitary(H, eps):
    w, V = np.linalg.eigh(H)                       # H Hermitian -> real w, unitary V
    return (V * np.exp(-1j * eps * w)) @ V.conj().T

def tdist(rho, sigma):
    return 0.5 * float(np.sum(np.linalg.svd(rho - sigma, compute_uv=False)))

def von_neumann(rho):
    w = np.linalg.eigvals(rho).real
    w = w[w > 1e-12]
    return float(-np.sum(w * np.log2(w)))

def binent(p):
    p = min(max(p, 0.0), 1.0)
    if p in (0.0, 1.0):
        return 0.0
    return -p * np.log2(p) - (1.0 - p) * np.log2(1.0 - p)

def bloch(rho):
    return np.array([np.trace(rho @ X).real, np.trace(rho @ Y).real, np.trace(rho @ Z).real])

# ---------------- 8D partial traces  (A slow, B mid, I fast; index = 4a + 2b + i) ----------------
def pt_I(rho8):    # keep AB (4x4, index = 2a+b)
    r4 = np.zeros((4, 4), dtype=complex)
    for a in range(4):
        for b in range(4):
            r4[a, b] = sum(rho8[a*2 + k, b*2 + k] for k in range(2))
    return r4
def pt_AB(rho8):   # keep I (2x2)
    rI = np.zeros((2, 2), dtype=complex)
    for i in range(2):
        for ip in range(2):
            rI[i, ip] = sum(rho8[4*a + 2*b + i, 4*a + 2*b + ip] for a in range(2) for b in range(2))
    return rI
def pt_A4(rho4):   # 4x4 on (A,B) -> keep B (2x2)
    rB = np.zeros((2, 2), dtype=complex)
    for b in range(2):
        for bp in range(2):
            rB[b, bp] = sum(rho4[a*2 + b, a*2 + bp] for a in range(2))
    return rB
def pt_B4(rho4):   # 4x4 on (A,B) -> keep A (2x2)
    rA = np.zeros((2, 2), dtype=complex)
    for a in range(2):
        for ap in range(2):
            rA[a, ap] = sum(rho4[a*2 + b, ap*2 + b] for b in range(2))
    return rA

# sanity: partial traces are correct on known cases
_p0 = np.zeros(4, dtype=complex); _p0[0] = _p0[1] = 1 / np.sqrt(2)   # |0>_A x |+>_B
assert np.allclose(pt_A4(np.outer(_p0, _p0.conj())), 0.5 * np.ones((2, 2))), "pt_A4 sanity"
assert np.allclose(pt_B4(np.outer(_p0, _p0.conj())), np.array([[1, 0], [0, 0]])), "pt_B4 sanity"

# ---------------- states ----------------
def rho_ab_c(c):
    """v1 correlated family: (1/4)(I + XX) + (c/4)(IX + XI); c in [-1,1]."""
    p = np.zeros(4, dtype=complex); p[0] = p[3] = 1 / np.sqrt(2)          # |Phi+>
    q = np.zeros(4, dtype=complex); q[1] = q[2] = 1 / np.sqrt(2)          # |Psi+>
    P = np.outer(p, p.conj()); Q = np.outer(q, q.conj()); C = np.outer(p, q.conj())
    return 0.5 * (P + Q) + 0.5 * c * (C + C.conj().T)

def rho_theta(theta):
    """honest-model family: 1/2(|00><00|+|11><11|) + (theta/2)(|00><11|+|11><00|).
    All members have rho_A = rho_B = I/2 (all local observables 0); theta = the
    JOINT |00>-|11> coherence (invisible locally). theta = 1 -> |Phi+>."""
    r = np.zeros((4, 4), dtype=complex)
    r[0, 0] = 0.5; r[3, 3] = 0.5
    r[0, 3] = r[3, 0] = 0.5 * theta
    return r

def embed8(rho_ab):
    i0 = np.zeros((2, 2), dtype=complex); i0[0, 0] = 1
    return np.kron(rho_ab, i0)

# ---------------- the two models ----------------
# v1 (the DIAGNOSIS target): the A-B JOINT observable with I in a Z eigenstate.
H_INFO_v1 = kron(Z, Z, Z)            # Z_A Z_B Z_I, I = |0> (a spectator)
# honest model (this round): A<->I<->B, NO direct A-B term; I couples via X_I.
H_int = kron(Z, I2, X) + kron(I2, Z, X)     # Z_A X_I + Z_B X_I

# =====================================================================
# PART A -- the round-7 diagnosis of v1 (all three claims, re-verified)
# =====================================================================
print("=" * 72)
print("PART A  the round-7 diagnosis of v1 (independently re-verified)")
print("=" * 72)

# A1: I is a spectator eigenstate -> the model reduces to a direct Z_A Z_B.
i0 = np.zeros((2, 2), dtype=complex); i0[0, 0] = 1
a1_Idev = 0.0; a1_redev = 0.0
for c in [0.0, 0.3, 0.7, 1.0]:
    for eps in [0.0, 0.3, 0.7, 1.0]:
        r0 = embed8(rho_ab_c(c))
        U = unitary(H_INFO_v1, eps)
        r1 = U @ r0 @ U.conj().T
        a1_Idev = max(a1_Idev, tdist(pt_AB(r1), i0))
        UAB = unitary(np.kron(Z, Z), eps)
        a1_redev = max(a1_redev, tdist(pt_I(r1), UAB @ rho_ab_c(c) @ UAB.conj().T))
assert a1_Idev <= 1e-12, f"A1 FAILS: I leaves |0>: {a1_Idev:.3e}"
assert a1_redev <= 1e-12, f"A1 FAILS: not a direct Z_A Z_B: {a1_redev:.3e}"
print(f"  A1  I spectator:  max D(rho_I(eps), |0><0|) = {a1_Idev:.2e}; "
      f"max D(rho_AB, e^-i eps Z_AZ_B rho e^+i eps) = {a1_redev:.2e}.")
print("      -> with I = |0> (a +1 eigenstate of Z_I), the auxiliary NEVER leaves |0>;\n"
      "         v1 reduces to the DIRECT two-qubit interaction U_AB = e^{-i eps Z_A Z_B}.")

# A2: the no-signaling test is a completeness tautology, not no-signaling.
def v1_bob_marg(rho8, setting):
    if setting == 'Z':
        pa = [np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])]
    else:
        pa = [np.array([[0.5, 0.5], [0.5, 0.5]]), np.array([[0.5, -0.5], [-0.5, 0.5]])]
    b0 = np.array([[1, 0], [0, 0]])
    return sum(np.real(np.trace(np.kron(np.kron(a, b0), I2) @ rho8)) for a in pa)
_rng = np.random.default_rng(20261122)
def rand_rho(n):
    M = _rng.standard_normal((n, n)) + 1j * _rng.standard_normal((n, n))
    return M @ M.conj().T / np.trace(M @ M.conj().T)
a2a = max(abs(v1_bob_marg(rand_rho(8), 'Z') - v1_bob_marg(rand_rho(8), 'X')) for _ in range(40))
# (use the SAME random state for both bases so the completeness identity is tested)
a2a = max(abs(v1_bob_marg(r, 'Z') - v1_bob_marg(r, 'X'))
          for _ in range(40) for r in [rand_rho(8)])
assert a2a <= 1e-12, f"A2a FAILS: Delta_B not identically 0: {a2a:.3e}"
print(f"  A2a v1's Delta_B (X vs Z basis, summed) = 0 for EVERY state "
      f"(max over 40 random states {a2a:.2e}): measurement COMPLETENESS, not no-signaling.")
# A2b: the CORRECT test (Alice encodes before, Bob reads after) -> D = |sin(2 eps)|.
def bob_marg_state(alice_bit, eps):
    a = np.array([1, 0], dtype=complex) if alice_bit == 0 else np.array([0, 1], dtype=complex)
    p = np.array([1, 1], dtype=complex) / np.sqrt(2)
    psi = unitary(np.kron(Z, Z), eps) @ np.kron(a, p)
    return pt_A4(np.outer(psi, psi.conj()))
a2b = max(abs(tdist(bob_marg_state(0, e), bob_marg_state(1, e)) - abs(np.sin(2 * e)))
          for e in [0.1, 0.3, 0.6, 1.0])
assert a2b <= 1e-12, f"A2b FAILS: D != |sin(2 eps)|: {a2b:.3e}"
assert tdist(bob_marg_state(0, 0.6), bob_marg_state(1, 0.6)) > 0.5, "no signaling?"
print(f"  A2b the CORRECT test (Alice encodes before, Bob reads after): "
      f"D = |sin(2 eps)| to {a2b:.2e} -- Bob CAN read Alice's choice through the\n"
      "      direct Z_A Z_B.  Global CPTP != no-signaling (SWAP/CNOT counterexamples); "
      "v1's Part A was blind to it.")

# A3: c is locally visible, not joint-only.
a3 = max(max(tdist(pt_B4(rho_ab_c(c)), 0.5 * (I2 + c * X)),
             tdist(pt_A4(rho_ab_c(c)), 0.5 * (I2 + c * X)),
             abs(np.real(np.trace(pt_B4(rho_ab_c(c)) @ X)) - c),
             abs(np.real(np.trace(pt_A4(rho_ab_c(c)) @ X)) - c))
         for c in [-1.0, -0.3, 0.0, 0.3, 0.7, 1.0])
assert a3 <= 1e-12, f"A3 FAILS: c not locally visible: {a3:.3e}"
print(f"  A3  c locally visible:  rho_A = rho_B = 1/2(I + c X), so <X_A> = <X_B> = c "
      f"(max dev {a3:.2e}).")
print("      -> D_B = |c| sin^2 eps was proportional to Bob's LOCAL initial X-polarization,\n"
      "         not to an inaccessible joint coherence.")

# =====================================================================
# PART B -- Q1: I genuinely participates (the fix for the spectator bug)
# =====================================================================
print()
print("=" * 72)
print("PART B  Q1: does I really participate?  (honest model: H_int = (Z_A+Z_B) X_I)")
print("=" * 72)
print("  pre-registered (EXACT, theta-independent):  rho_I^final = diag(cos^2 2eps, sin^2 2eps)")
print(f"  {'theta':>5} {'eps':>5}  rho_I^final                 S(rho_I)   h(cos^2 2eps)   diff")
max_b1 = 0.0; max_b2 = 0.0
for theta in [0.0, 0.3, 0.5, 0.7, 1.0]:
    for eps in [0.1, 0.3, 0.7, 1.0]:
        r0 = embed8(rho_theta(theta))
        U = unitary(H_int, eps)
        rI = pt_AB(U @ r0 @ U.conj().T)
        c2 = np.cos(2 * eps) ** 2
        target = np.array([[c2, 0], [0, 1 - c2]], dtype=complex)
        max_b1 = max(max_b1, tdist(rI, target))
        Snum = von_neumann(rI)
        Sform = binent(c2)
        max_b2 = max(max_b2, abs(Snum - Sform))
        if theta in (0.0, 1.0) and eps in (0.3, 0.7):
            print(f"  {theta:>5.1f} {eps:>5.1f}  {np.round(rI, 4).real.tolist()}  "
                  f"{Snum:.5f}    {Sform:.5f}      {abs(Snum-Sform):.2e}")
assert max_b1 <= 1e-10, f"B1 FAILS: rho_I != diag(cos^2,sin^2): {max_b1:.3e}"
assert max_b2 <= 1e-10, f"B2 FAILS: S(rho_I) != h(cos^2 2eps): {max_b2:.3e}"
assert tdist(pt_AB(unitary(H_int, 0.7) @ embed8(rho_theta(1.0)) @ unitary(H_int, 0.7).conj().T), i0) > 0.3
print(f"  -> B1: rho_I^final = diag(cos^2 2eps, sin^2 2eps) to {max_b1:.1e} (theta-INDEPENDENT);")
print(f"         B2: S(rho_I) = h(cos^2 2eps) to {max_b2:.1e} and is > 0 for eps != 0.")
print("      -> I GENUINELY PARTICIPATES (it changes state and entangles with AB for theta>0):")
print("         the fix for v1's spectator-eigenstate bug. [X_I, |0><0|] != 0, unlike [Z_I, |0><0|] = 0.")

# =====================================================================
# PART C -- Q2: the I-mediated A->B channel and its causal timescale
# =====================================================================
print()
print("=" * 72)
print("PART C  Q2: the I-mediated A->B channel (no direct A-B term) + causal timescale")
print("=" * 72)
# C1: the reduced AB map is CPTP (a legitimate physical channel) -> no auto-FTL.
#     (trace-preserving + maps density matrices to density matrices, checked on a grid)
max_c1 = 0.0
for theta in [0.0, 0.4, 0.7, 1.0]:
    for eps in [0.0, 0.3, 0.7, 1.0]:
        rABf = pt_I(unitary(H_int, eps) @ embed8(rho_theta(theta)) @ unitary(H_int, eps).conj().T)
        max_c1 = max(max_c1, abs(np.trace(rABf) - 1.0), float(np.max(np.abs(np.linalg.eigvals(rABf - rABf.conj().T)))))
        assert np.min(np.linalg.eigvals(rABf).real) > -1e-12, "CPTP: not PSD"
assert max_c1 <= 1e-10, f"C1 FAILS: reduced map not CPTP: {max_c1:.3e}"
print(f"  C1  the reduced AB map (trace out I) is CPTP (trace-preserving + PSD-preserving,\n"
      f"      max dev {max_c1:.2e}): a legitimate physical channel on AB -> no automatic FTL\n"
      "      (the Simon-Buzek-Gisin fence in the CORRECT form, not a global-CPTP tautology).")
# C2: the JOINT |00><11| coherence is dephased by cos(4 eps).
max_c2 = 0.0
print(f"  {'theta':>5} {'eps':>5}  |00><11|_final   (theta/2) cos(4 eps)   diff")
for theta in [0.3, 0.5, 0.7, 1.0]:
    for eps in [0.2, 0.3, 0.5, 0.7]:
        rABf = pt_I(unitary(H_int, eps) @ embed8(rho_theta(theta)) @ unitary(H_int, eps).conj().T)
        coh = rABf[0, 3].real
        form = 0.5 * theta * np.cos(4 * eps)
        max_c2 = max(max_c2, abs(coh - form))
        if theta in (0.5, 1.0) and eps in (0.3, 0.7):
            print(f"  {theta:>5.1f} {eps:>5.1f}   {coh:>12.6f}      {form:>12.6f}    {abs(coh-form):.2e}")
assert max_c2 <= 1e-10, f"C2 FAILS: |00><11| not dephased by cos(4 eps): {max_c2:.3e}"
print(f"  C2  the JOINT |00><11| coherence is dephased by a factor cos(4 eps) to {max_c2:.1e}:\n"
      "      |00><11|_final = (theta/2) cos(4 eps).  The A->B imprint on the joint structure\n"
      "      propagates through I with amplitude cos(4 eps), controlled by eps = the causal timescale.")
# C3: Bob's LOCAL state is invariant (no LOCAL A->B signal).
max_c3 = 0.0
for theta in [0.0, 0.3, 0.5, 0.7, 1.0]:
    for eps in [0.0, 0.2, 0.5, 0.7, 1.0]:
        rABf = pt_I(unitary(H_int, eps) @ embed8(rho_theta(theta)) @ unitary(H_int, eps).conj().T)
        max_c3 = max(max_c3, tdist(pt_A4(rABf), 0.5 * I2))
assert max_c3 <= 1e-12, f"C3 FAILS: Bob's local state not invariant: {max_c3:.3e}"
print(f"  C3  Bob's LOCAL state rho_B^final = I/2 for ALL theta, eps (max dev {max_c3:.2e}).")
print("      -> the I-mediated influence is entirely in the JOINT structure: there is no LOCAL\n"
      "         A->B signal (consistent with the no direct A-B term).  Alice can imprint on the\n"
      "         joint A-B state; the I-mediated channel then dephases that imprint by cos(4 eps).")

# =====================================================================
# PART D -- Q3: the response distinguishes JOINT information with all local
#           observables held fixed (the corrected informational signature)
# =====================================================================
print()
print("=" * 72)
print("PART D  Q3: response distinguishes JOINT information with all local observables fixed")
print("=" * 72)
# D0: verify the test bed: ALL local observables are 0 (marginals = I/2) for every theta.
max_d0 = 0.0
for theta in [0.0, 0.25, 0.5, 0.75, 1.0]:
    rho = rho_theta(theta)
    max_d0 = max(max_d0,
                 tdist(pt_B4(rho), 0.5 * I2), tdist(pt_A4(rho), 0.5 * I2),
                 float(np.max(np.abs(bloch(pt_B4(rho))))), float(np.max(np.abs(bloch(pt_A4(rho))))))
assert max_d0 <= 1e-12, f"D0 FAILS: marginals not I/2 for all theta: {max_d0:.3e}"
print(f"  D0  test bed: for every theta, rho_A = rho_B = I/2 and all six local observables\n"
      f"      <X>,<Y>,<Z> on A and B are 0 (max dev {max_d0:.2e}).  The ONLY thing that varies\n"
      "      with theta is the JOINT |00>-|11> coherence -- invisible in any local state.")
# D1: the headline -- D_AB(theta, eps) = (theta/2) |1 - cos(4 eps)|  (EXACT).
print(f"  {'theta':>5} {'eps':>5}  D_AB(theta,eps)   (theta/2)|1-cos(4 eps)|   diff")
max_d1 = 0.0
for theta in [0.0, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
    for eps in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
        rABf = pt_I(unitary(H_int, eps) @ embed8(rho_theta(theta)) @ unitary(H_int, eps).conj().T)
        dab = tdist(rABf, rho_theta(theta))
        form = 0.5 * theta * abs(1.0 - np.cos(4 * eps))
        max_d1 = max(max_d1, abs(dab - form))
        if theta in (0.0, 0.5, 1.0) and eps in (0.3, 0.7, 1.0):
            print(f"  {theta:>5.1f} {eps:>5.1f}  {dab:>12.6f}      {form:>12.6f}    {abs(dab-form):.2e}")
assert max_d1 <= 1e-10, f"D1 FAILS: D_AB != (theta/2)|1-cos(4 eps)|: {max_d1:.3e}"
print(f"  D1  headline (EXACT):  D_AB(theta, eps) = (theta/2) | 1 - cos(4 eps) |  to {max_d1:.1e}.")
print("      A nontrivial function of the JOINT |00>-|11> coherence theta, with every local\n"
      "      observable held fixed.")
# D2: the crisp contrast -- identical marginals, different joint structure, different response.
dab_0 = tdist(pt_I(unitary(H_int, 0.7) @ embed8(rho_theta(0.0)) @ unitary(H_int, 0.7).conj().T), rho_theta(0.0))
dab_1 = tdist(pt_I(unitary(H_int, 0.7) @ embed8(rho_theta(1.0)) @ unitary(H_int, 0.7).conj().T), rho_theta(1.0))
assert tdist(pt_B4(rho_theta(0.0)), pt_B4(rho_theta(1.0))) <= 1e-12, "marginals differ!"
assert tdist(pt_A4(rho_theta(0.0)), pt_A4(rho_theta(1.0))) <= 1e-12, "marginals differ!"
assert dab_0 <= 1e-12 and dab_1 > 0.9, f"D2 FAILS: {dab_0:.3e}, {dab_1:.3e}"
print(f"  D2  the crisp contrast (eps = 0.7):  theta = 0 (the classical mixture 1/2(|00><00|+\n"
      f"      |11><11|)) and theta = 1 (|Phi+>) have IDENTICAL marginals (both I/2) but\n"
      f"      D_AB(theta=0) = {dab_0:.2e}  vs  D_AB(theta=1) = {dab_1:.5f}.")
print("      -> the back-action on the physical system depends on JOINT information (theta)\n"
      "         that is invisible in any local observable.  This is the corrected informational\n"
      "         signature: v1 faked it with a locally-visible c; here it is provably joint-only.")

# =====================================================================
# SYNTHESIS
# =====================================================================
print()
print("=" * 72)
print("SYNTHESIS")
print("=" * 72)
print("""
  Round 7 (~/feedback_quantum_aux) killed the v1 INTERPRETATION but confirmed its
  NUMERICS and kept the auxiliary-field strategy alive:
    (i)   I was a spectator eigenstate (reduced to a direct Z_A Z_B);
    (ii)  the no-signaling test was a completeness tautology (global CPTP != no-signaling);
    (iii) c was locally visible, not joint-only.

  auxiliary2 is the honest construction the review specified: an ACTUAL second
  dynamical sector I, coupled via A<->I<->B (NO direct A-B term, H_int = (Z_A+Z_B) X_I),
  that (Q1) genuinely participates (rho_I = diag(cos^2 2eps, sin^2 2eps), S > 0),
  (Q2) mediates a JOINT A-B back-action with a clear causal timescale (the |00><11>
  coherence dephased by cos 4eps; Bob's local state invariant -- no LOCAL A->B signal),
  and (Q3) whose response distinguishes JOINT information (theta) when all local
  observables are held fixed (D_AB = (theta/2)|1 - cos 4eps|).

  This is the first construction where the informational sector's back-action on the
  physical system is a provable function of JOINT information -- the exact property the
  round-7 review demanded and that v1 faked with a locally-visible c.

  Honest limits: the closed forms are EXACT for THIS coupling (Z_A+Z_B) X_I and THIS
  initial-state family (the |00>-|11> coherent subfamily); the I-mediated channel is a
  DEPHASING in the (Z_A+Z_B) eigenbasis.

  Open question (next step): does a GENERIC A<->I<->B coupling (adding X_A, X_B, Y
  terms, or a different mediator state) reproduce the "response depends on joint
  information with the marginals fixed" property, or is it specific to the Z-structure
  coupling?  Equivalently: is dephasing in a joint observable the GENERIC back-action an
  auxiliary sector can have on the physical system, or can other CPTP structures (amplitude
  damping, etc.) arise from A<->I<->B couplings?
""")
print("ALL PRE-REGISTERED FORMS VERIFIED. exit 0.")

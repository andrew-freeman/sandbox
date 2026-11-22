#!/usr/bin/env python3
"""
dual_field_quantum_auxiliary.py -- the P x I auxiliary model (round 6, commit #2).

The round-6 review's SURVIVING route. After rounds 4-6 killed the *reweighting*
architecture (P' ~ P e^{eps F}: a post-hoc nonlinear map on measured branches, which
the general 2x2 no-signaling no-go forces to be trivial), the review's central
proposal is to take "Dual Field" LITERALLY: instead of rescaling branch
probabilities AFTER quantum mechanics generates them, introduce an ACTUAL additional
dynamical subsystem I (the informational sector) coupled to the physical system P
(A, B) by a joint unitary. The reduced physical statistics rho_P = Tr_I rho_{P I}
then evolve under a CPTP map (the Simon-Buzek-Gisin fence), so no-signaling holds
BY CONSTRUCTION. The question becomes: does I have an OBSERVABLE, REPRODUCIBLE,
and INFORMATIONAL back-action on P?

MODEL
  Physical: qubits A, B.  Informational: qubit I.  Total Hilbert space 2^3 = 8.
  Joint unitary   U(eps) = exp(-i eps H_int)     (free H_AB = 0; t = 1).
  I starts in |0> (the informational sector "at rest"; a Z eigenstate).
  Two coupling families:
    GEN  = Z_A I_B Z_I   : I couples to a LOCAL observable of A  (ordinary env).
    INFO = Z_A Z_B Z_I   : I couples to the A-B JOINT observable Z_A Z_B (informational).
  Initial A-B state: a correlated family rho_c with tunable joint coherence c in [-1,1]:
        rho_c = 0.5(|Phi+><Phi+| + |Psi+><Psi+|) + 0.5 c (|Phi+><Psi+| + |Psi+><Phi+|)
              = (1/4)(I + X X) + (c/4)(I X + X I)          [identity, XX, and the
                                                            single-flip coherence c]
    c = 0  -> a Bell-state mixture (classically X-correlated, <XX>=1, <ZZ>=0).
    c = +1 -> |+>|+>  (X-polarized product).   c = -1 -> |->|->.
    c is the A-B single-flip (I X + X I)/2 coherence amplitude -- a property of the
    JOINT state, not of either local state alone.

THREE PARTS  (numpy-only, exact; pre-registered closed forms hard-asserted; exit 0)

  A. NO-SIGNALING  (the architecture holds -- no automatic FTL).
     For GEN, INFO, and a RANDOM 8D coupling (a generic CPTP unitary), Bob's
     marginal is independent of Alice's local setting (X vs Z):  Delta_B = 0.
     This is the round-5 CPTP positive control, now in the auxiliary architecture:
     a joint unitary is CPTP, so it does NOT auto-signal (the reweighting did,
     because it was a post-hoc NON-CPTP map).

  B. OBSERVABLE, REPRODUCIBLE BACK-ACTION.
     The informational sector changes the physical statistics in a locally
     observable, reproducible way. The headline (pre-registered, exact):
        D_B(INFO, c, eps) = |c| sin^2(eps)        [trace distance of Bob's local state]
     i.e. Bob's Bloch vector stays on the x-axis and its x-component is c cos(2 eps);
     D_B = |c| sin^2(eps) follows exactly. The joint A-B state also changes,
     D_AB = O(eps). This is the back-action the reweighting was SUPPOSED to give
     but could only fake by breaking no-signaling.

  C. THE INFORMATIONAL (NONLOCAL) SIGNATURE  (I != ordinary noise).
     Discriminate a LOCAL coupling from a JOINT one by the back-action on the
     REMOTE party B (the party H_int reaches only THROUGH A, via Z_A Z_B):
        GEN  (Z_A I_B Z_I):  D_B = 0   for ALL c and all eps  (a local coupling
                             never touches B; Bob's state is exactly invariant).
        INFO (Z_A Z_B Z_I):  D_B = |c| sin^2(eps)  -- a nontrivial function of the
                             JOINT-state coherence c; even in c; zero at c = 0.
     Signature: a coupling to a JOINT observable produces a back-action on the
     remote party that a local/ordinary-environment coupling CANNOT (D_B = 0).
     That is the structural property ordinary (local) environmental noise lacks:
     the informational sector, coupled to a joint observable, reaches both parties,
     and the back-action is set by the joint state's coherence.

SYNTHESIS
  Reweighting (rounds 4-6): P' ~ P e^{eps F} was a post-hoc NON-CPTP map on measured
  branches -> it signaled (the general no-go). The auxiliary P x I model is CPTP
  (a joint unitary) -> it does NOT signal (Part A), while still carrying an
  OBSERVABLE back-action (Part B) that is INFORMATIONAL/nonlocal (Part C). "Dual
  Field" = an actual second dynamical sector coupled to a joint observable -- not
  "ordinary physics + an informational score". The honest open question this toy
  sharpens (next step): can a GENERIC H_int reproduce the c-dependent back-action
  on B, or is the joint-observable coupling (coupling I to Z_A Z_B rather than Z_A)
  the structural property that makes the back-action reach the remote party?

Run:  python3 dual_field_quantum_auxiliary.py     (exit 0 = all pre-registered
forms verified to machine precision; any failure raises AssertionError).
"""
import numpy as np

# ---------------- Pauli / identity basis ----------------
I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1], [1, 0]], dtype=complex)
Y  = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z  = np.array([[1, 0], [0, -1]], dtype=complex)

def kron(*ops):
    out = np.array([[1]], dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out

# ---------------- 8x8 couplings  (A = slow, B = mid, I = fast) ----------------
H_GEN  = kron(Z, I2, Z)    # local on A  (ordinary environment)
H_INFO = kron(Z, Z, Z)     # the A-B JOINT observable Z_A Z_B (informational)
# a random generic coupling (for the Part-A CPTP-genericity check)
_rng = np.random.default_rng(20261122)
_ar = _rng.standard_normal((8, 8)) + 1j * _rng.standard_normal((8, 8))
H_RAND = (_ar + _ar.conj().T) / 2
H_RAND = H_RAND / np.linalg.norm(H_RAND, 2)

# ---------------- states ----------------
def bell_phi():            # |Phi+> = (|00>+|11>)/sqrt2  on A,B  (index = 2a+b)
    v = np.zeros(4, dtype=complex); v[0] = v[3] = 1 / np.sqrt(2); return v

def bell_psi():            # |Psi+> = (|01>+|10>)/sqrt2
    v = np.zeros(4, dtype=complex); v[1] = v[2] = 1 / np.sqrt(2); return v

def rho_ab_c(c):
    """correlated family: (1/4)(I+XX) + (c/4)(IX+XI); c in [-1,1]."""
    p, q = bell_phi(), bell_psi()
    P = np.outer(p, p.conj()); Q = np.outer(q, q.conj()); C = np.outer(p, q.conj())
    return 0.5 * (P + Q) + 0.5 * c * (C + C.conj().T)

def embed8(rho_ab):
    """(rho_AB 4x4) x |0><0|_I  ->  8x8 on (A B) x I, I = fast index."""
    i0 = np.zeros((2, 2), dtype=complex); i0[0, 0] = 1
    return np.kron(rho_ab, i0)

# ---------------- partial traces ----------------
def pt_I(rho8):
    """trace out I (fast index): 8x8 -> 4x4 on A,B (index = 2a+b)."""
    r4 = np.zeros((4, 4), dtype=complex)
    for a in range(4):
        for b in range(4):
            r4[a, b] = sum(rho8[a * 2 + k, b * 2 + k] for k in range(2))
    return r4

def pt_A(rho4):
    """trace out A (slow index) of a 4x4 on (A,B): -> 2x2 on B."""
    rB = np.zeros((2, 2), dtype=complex)
    for b in range(2):
        for bp in range(2):
            rB[b, bp] = sum(rho4[a * 2 + b, a * 2 + bp] for a in range(2))
    return rB

# sanity: partial traces are correct on known cases
_p0 = np.zeros(4, dtype=complex); _p0[0] = _p0[1] = 1 / np.sqrt(2)   # |0>_A x |+>_B
assert np.allclose(pt_A(np.outer(_p0, _p0.conj())), 0.5 * np.ones((2, 2))), "pt_A sanity"
assert np.allclose(pt_I(embed8(rho_ab_c(0.3))), rho_ab_c(0.3)), "pt_I sanity"

# ---------------- unitary (numpy-only, via eig of the Hermitian H) ----------------
def unitary(H, eps):
    w, V = np.linalg.eigh(H)                       # H Hermitian -> real w, unitary V
    return (V * np.exp(-1j * eps * w)) @ V.conj().T

# ---------------- observables ----------------
def tdist(rho, sigma):
    return 0.5 * float(np.sum(np.linalg.svd(rho - sigma, compute_uv=False)))

def bloch(rho):
    return np.array([np.trace(rho @ X).real, np.trace(rho @ Y).real, np.trace(rho @ Z).real])

def bob_marg(rho8, setting):
    """P_B(b=0) averaged over Alice's outcomes, given Alice's `setting` (X or Z).
    Computed with explicit projectors (faithful to the round-4/5 setup); for CPTP
    this is independent of `setting` by completeness -> Delta_B = 0."""
    if setting == 'Z':
        pa = [np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])]
    else:  # X basis: |+><+|, |-><-|
        pa = [np.array([[0.5, 0.5], [0.5, 0.5]]), np.array([[0.5, -0.5], [-0.5, 0.5]])]
    b0 = np.array([[1, 0], [0, 0]])
    total = 0.0
    for a in pa:
        op = np.kron(np.kron(a, b0), I2)          # A x B x I
        total += np.real(np.trace(op @ rho8))
    return total

def deltab(rho8):
    return abs(bob_marg(rho8, 'Z') - bob_marg(rho8, 'X'))

def concurrence(rho4):
    """Wootters concurrence of a 2-qubit state."""
    sy = Y
    yy = np.kron(sy, sy)
    R = rho4 @ (yy @ rho4.conj() @ yy)
    w = np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)), 0.0, None)))[::-1]
    return max(0.0, w[0] - w[1] - w[2] - w[3])

def rhoB_of(H, c, eps):
    r0 = embed8(rho_ab_c(c))
    U = unitary(H, eps)
    return pt_A(pt_I(U @ r0 @ U.conj().T))

def rhoAB_of(H, c, eps):
    r0 = embed8(rho_ab_c(c))
    U = unitary(H, eps)
    return pt_I(U @ r0 @ U.conj().T)

# =====================================================================
# PART A -- NO-SIGNALING (the architecture holds: no automatic FTL)
# =====================================================================
print("=" * 72)
print("PART A  no-signaling positive control (CPTP joint unitary -> no auto-FTL)")
print("=" * 72)
print(f"  {'coupling':<10} {'c':>6} {'eps':>6}  Delta_B  (Bob marginal, Alice X vs Z)")
max_db = 0.0
for H, nm in [(H_GEN, "GEN"), (H_INFO, "INFO"), (H_RAND, "RAND")]:
    for c in [0.0, 0.5, 1.0]:
        for eps in [0.0, 0.3, 1.0]:
            r0 = embed8(rho_ab_c(c))
            U = unitary(H, eps)
            r1 = U @ r0 @ U.conj().T
            db = deltab(r1)
            max_db = max(max_db, db)
            print(f"  {nm:<10} {c:>6.2f} {eps:>6.2f}  {db:.3e}")
assert max_db <= 1e-10, f"no-signaling violated: max Delta_B = {max_db:.3e}"
print(f"  -> max Delta_B over all couplings/settings = {max_db:.3e}  (<= 1e-10): "
      f"a joint unitary is CPTP, so Bob's marginal is independent of Alice's "
      f"setting BY CONSTRUCTION. No automatic FTL.")

# =====================================================================
# PART B -- OBSERVABLE, REPRODUCIBLE BACK-ACTION
# =====================================================================
print()
print("=" * 72)
print("PART B  observable, reproducible back-action")
print("=" * 72)
# headline: D_B(INFO, c, eps) = |c| sin^2(eps)  (exact)
print("  headline (pre-registered, EXACT):  D_B(INFO, c, eps) = |c| sin^2(eps)")
print("  (Bob's Bloch vector stays on the x-axis; x-component = c cos(2 eps).)")
print(f"  {'c':>5} {'eps':>6} {'D_B numeric':>13} {'|c| sin^2(eps)':>15} {'diff':>10}")
max_form_err = 0.0
for c in [0.3, 0.5, 0.7, 1.0]:
    for eps in [0.1, 0.3, 0.7, 1.0]:
        db_num = tdist(rhoB_of(H_INFO, c, eps), rhoB_of(H_INFO, c, 0.0))
        db_form = abs(c) * np.sin(eps) ** 2
        err = abs(db_num - db_form)
        max_form_err = max(max_form_err, err)
        print(f"  {c:>5.2f} {eps:>6.2f} {db_num:>13.8f} {db_form:>15.8f} {err:>10.2e}")
assert max_form_err <= 1e-10, f"D_B closed form violated: max |num-form| = {max_form_err:.3e}"
print(f"  -> D_B(INFO,c,eps) = |c| sin^2(eps) holds to {max_form_err:.1e} "
      f"machine precision. Bob's local statistics change observably and "
      f"reproducibly (the back-action the reweighting was supposed to give).")

# the joint A-B state also changes, D_AB = O(eps)
print("\n  joint A-B state change D_AB (O(eps)):")
c0 = rhoB_of(H_INFO, 1.0, 0.0)
for eps in [0.01, 0.05, 0.1]:
    dab = tdist(rhoAB_of(H_INFO, 1.0, eps), rhoAB_of(H_INFO, 1.0, 0.0))
    print(f"    eps={eps:.2f}:  D_AB={dab:.6f}   D_AB/eps={dab/eps:.4f}")
# O(eps) check: D_AB/eps ~ constant as eps -> 0
r1 = [tdist(rhoAB_of(H_INFO, 1.0, e), rhoAB_of(H_INFO, 1.0, 0.0)) / e for e in (0.01, 0.05, 0.1)]
assert max(r1) / min(r1) < 1.15, f"D_AB not O(eps): ratios {r1}"
print(f"    -> D_AB/eps ~ constant ({r1[0]:.3f}..{r1[-1]:.3f}): the back-action on the "
      f"joint state is O(eps).")
# leading order of D_B: D_B/eps^2 -> |c| as eps -> 0  (the virtual/2nd-order process)
print("\n  leading order of the Bob back-action (I starts in |0>, a Z eigenstate):")
for c in [0.3, 1.0]:
    row = [tdist(rhoB_of(H_INFO, c, e), rhoB_of(H_INFO, c, 0.0)) / e**2 for e in (0.01, 0.02, 0.05)]
    print(f"    c={c:.1f}:  D_B/eps^2 = {row[0]:.4f} {row[1]:.4f} {row[2]:.4f}  -> |c| = {abs(c)}")
    assert max(row) / min(row) < 1.02 and abs(row[0] - abs(c)) < 0.01, \
        f"D_B leading order != |c|: {row}"
print("    -> D_B = |c| eps^2 + O(eps^4): a second-order ('virtual') process, because "
      "[Z_I, |0><0|] = 0 kills the first order. The |c|-proportionality is the "
      "robust signature.")

# =====================================================================
# PART C -- THE INFORMATIONAL (NONLOCAL) SIGNATURE
# =====================================================================
print()
print("=" * 72)
print("PART C  the informational signature: local vs joint coupling")
print("=" * 72)
print("  Back-action on the REMOTE party B (H_int reaches B only through Z_A Z_B):")
print(f"  {'coupling':<8} {'c':>6}  D_B (eps=0.3)     [local coupling: B invariant;")
for nm in ["GEN", "INFO"]:
    H = H_GEN if nm == "GEN" else H_INFO
    for c in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        db = tdist(rhoB_of(H, c, 0.3), rhoB_of(H, c, 0.0))
        print(f"  {nm:<8} {c:>6.1f}  {db:.3e}")
# C1: GEN (local) leaves Bob EXACTLY invariant, for all c and eps
gmax = max(tdist(rhoB_of(H_GEN, c, e), rhoB_of(H_GEN, c, 0.0))
           for c in [-1.0, -0.5, 0.0, 0.5, 1.0] for e in [0.1, 0.3, 1.0])
assert gmax <= 1e-12, f"GEN back-action on B nonzero: {gmax:.3e}"
print(f"  -> GEN (Z_A I_B Z_I, local):  max D_B over all c,eps = {gmax:.3e} (<= 1e-12). "
      f"A LOCAL coupling never touches B -> Bob's state is exactly invariant.")
# C2: INFO even in c
emax = max(abs(tdist(rhoB_of(H_INFO, c, 0.3), rhoB_of(H_INFO, c, 0.0))
               - tdist(rhoB_of(H_INFO, -c, 0.3), rhoB_of(H_INFO, -c, 0.0)))
           for c in [0.3, 0.7])
assert emax <= 1e-12, f"INFO not even in c: {emax:.3e}"
print("  -> INFO back-action is even in c (set by |c|, the correlation magnitude).")
# C3: INFO vanishes at c = 0 (the Bell-mixture state: no single-flip coherence)
d0 = tdist(rhoB_of(H_INFO, 0.0, 0.3), rhoB_of(H_INFO, 0.0, 0.0))
assert d0 <= 1e-12, f"INFO D_B(c=0) nonzero: {d0:.3e}"
print(f"  -> INFO D_B(c=0) = {d0:.3e} (<= 1e-12): the back-action on B is set by the "
      f"JOINT-state coherence c, not by either local state alone.")

# =====================================================================
# SYNTHESIS
# =====================================================================
print()
print("=" * 72)
print("SYNTHESIS")
print("=" * 72)
print("""
  Reweighting (rounds 4-6):  P' ~ P e^{eps F} was a post-hoc NON-CPTP map on measured
    branches  ->  it signaled (the general 2x2 no-go).
  Auxiliary P x I model:      a joint UNITARY is CPTP  ->  it does NOT signal (Part A),
    while carrying an OBSERVABLE back-action (Part B) that is INFORMATIONAL/nonlocal
    (Part C): a coupling to the JOINT observable Z_A Z_B reaches the remote party B
    (D_B = |c| sin^2 eps) in a way a LOCAL coupling cannot (D_B = 0).

  "Dual Field" = an actual second dynamical sector coupled to a joint observable --
  not "ordinary physics + an informational score".

  Open question this toy sharpens (next step): can a GENERIC H_int reproduce the
  c-dependent back-action on B, or is coupling I to the joint observable (Z_A Z_B
  rather than Z_A) the structural property that lets the back-action reach the remote
  party?  (If every interesting H_int just looks like an ordinary hidden environment,
  that is a USEFUL failure: Dual Field -> ordinary extra field.)
""")
print("ALL PRE-REGISTERED FORMS VERIFIED. exit 0.")

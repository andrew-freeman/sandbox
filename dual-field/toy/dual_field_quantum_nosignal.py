#!/usr/bin/env python3
"""
Dual-Field toy -- two-qubit no-signaling check (program-level test, 2026-11-21).

Question (round-4 review, README next-steps item 6)
---------------------------------------------------
The dual field reweights branch probabilities:  P' ~ P * exp(eps * F),  with
F a "downstream informational consequence" functional.  Put the reweighting
on an entangled two-qubit system and ask whether Alice's choice of local
measurement basis leaks into Bob's marginal statistics (no-signaling):

    standard QM:          Delta_B = 0   (for all eps)
    dual-field candidate: Delta_B(eps, F) =? 0

Setup (exact linear algebra -- a two-qubit state is a length-4 complex
vector; no quantum hardware anywhere in this test)
--------------------------------------------------
    state:   |Phi+> = (|00> + |11>)/sqrt(2)          (maximally entangled)
    Alice:   chooses her measurement basis, Z {|0>,|1>} or X {|+>,|->}
    Bob:     always measures Z {|0>,|1>}, never communicates
    branch:  the FULL joint outcome (a, i, b): Alice's basis a, her outcome
             i, Bob's outcome b.  This is the toy's stand-in for a physical
             history; the reweighting acts on branch probabilities.
    reweight (pre-registered):  P'(i,b|a) = P(i,b|a) exp(eps F_a(i,b)) / Z_a
             with Z_a = sum over (i,b) at FIXED a (per-setup normalization:
             for a fixed experimental arrangement the outcomes must sum to 1)
    test:    Delta_B = TV( P'_B(b|X), P'_B(b|Z) )    (total variation distance)

The three F cases (round-4 spec) -- concrete non-constant representatives
-------------------------------------------------------------------------
    1. Alice-local:   F references only Alice's outcome (the upstream branch)
                      (favors the {0, +} branch).
    2. Bob-local:     F references only Bob's outcome (F = b).
    3. Joint/future:  F couples the upstream branch to the downstream outcome
                      (F = i' * b, i' labels the {1, +} branch) -- the
                      on-hypothesis "downstream consequence" case.

Semantic assumptions (stated, per house method):
    (i)  reweighting at the level of the chosen arrangement's joint branches
         (the operational reading -- the only reading in which eps is
         observable in this scenario; see the dichotomy in README 3e);
    (ii) per-setup normalization Z_a (outcomes of a fixed arrangement sum to 1).

Pre-registered predictions (derived analytically BEFORE running)
----------------------------------------------------------------
    baseline:  rho_B = Tr_A(|Phi+><Phi+|) = I/2 exactly; Delta_B(eps=0) = 0
               for every F.  Exact joint branch tables:
                   Z basis: P(0,0)=1/2, P(0,1)=0, P(1,0)=0, P(1,1)=1/2
                   X basis: P(+,b)=P(-,b)=1/4  for b=0,1
    case 1 (Alice-local, favors {0,+}):
        P'_B(0|Z) = e^eps/(1+e^eps),  P'_B(0|X) = 1/2
        Delta_B(eps) = (e^|eps| - 1) / (2 (e^|eps| + 1)) = 0.5*tanh(|eps|/2)
        first order: eps/4                       -> LEAKS
    case 2 (Bob-local, F = b):
        exp(eps*f(b)) factors out of the sum over i:
        sum_i P(i,b) e^{eps f(b)} = e^{eps f(b)} P_B(b)
        =>  Delta_B(eps) = 0 EXACTLY, all orders, in the TESTED DIRECTION ONLY
            (round-5: this toy fixes Bob's measurement at Z; flipping the
            experiment -- Alice fixed Z, Bob chooses Z/X -- makes it LEAK with
            Delta_A(eps) = 0.5*tanh(|eps|/2); see v2 part A)
    case 3 (joint, F = i'*b):
        P'_B(0|Z) = 1/(1+e^eps),  P'_B(0|X) = 2/(3+e^eps)
        Delta_B(eps) = |e^eps - 1| / ((3+e^eps)(1+e^eps))     (round-5: the
        denominator uses e^eps, NOT e^|eps| -- the old form was wrong for
        eps < 0: at eps=-1 actual 0.13721 vs old 0.08081)
        first order: eps/8 (eps>0)                     -> LEAKS

First-order condition (recorded; SCOPED to this setup: one Bell state, Bob's
measurement fixed, Alice->Bob direction -- the full no-signaling condition is
both directions for ALL states/settings, which is what v2 establishes):
    dP'_B(b|a) = eps * [ sum_i P_a(i,b) F_a(i,b)
                         - P_B(b) sum_{i,b'} P_a(i,b') F_a(i,b') ]

Known-limit tells (hard asserts)
--------------------------------
    rho_B == I/2 (exact); joint tables == the exact values above (exact);
    Delta_B(eps=0) = 0 in all three cases; the three closed forms reproduced
    by the numerical reweighting to < 1e-9 (exact linear algebra).
"""
import numpy as np

# ---------------- two-qubit Hilbert space -----------------------------------
# index = 2*a + b   (a = Alice qubit, b = Bob qubit);  |00>=0, |01>=1,
# |10>=2, |11>=3.

def ket(a, b):
    v = np.zeros(4, dtype=complex)
    v[2 * a + b] = 1.0
    return v

PSI = (ket(0, 0) + ket(1, 1)) / np.sqrt(2.0)          # |Phi+>
RHO = np.outer(PSI, PSI.conj())

# Alice projectors (4x4, act on the Alice qubit)
P_AZ = {0: np.diag([1.0, 1.0, 0.0, 0.0]),            # |0><0|
        1: np.diag([0.0, 0.0, 1.0, 1.0])}            # |1><1|
P_AX = {}
for s in (0, 1):                                      # 0 -> |+>, 1 -> |->
    m = np.full((2, 2), 0.5) if s == 0 else np.array([[0.5, -0.5], [-0.5, 0.5]])
    P = np.zeros((4, 4), dtype=complex)
    for a in range(2):
        for a2 in range(2):
            for b in range(2):
                P[2 * a + b, 2 * a2 + b] = m[a, a2]
    P_AX[s] = P
# Bob projectors (fixed Z basis)
Q_B = {0: np.diag([1.0, 0.0, 1.0, 0.0]),             # b=0
       1: np.diag([0.0, 1.0, 0.0, 1.0])}             # b=1

def joint_p(a_proj, b):
    """P(a-outcome, b) = Tr[ a_proj * Q_b * rho ] for the chosen state."""
    return float(np.real(np.trace(a_proj @ Q_B[b] @ RHO)))

def partial_trace_A(r):
    """Bob's reduced state: (Tr_A r)_{b,b'} = sum_a r[2a+b, 2a+b']."""
    out = np.zeros((2, 2), dtype=complex)
    for b in range(2):
        for b2 in range(2):
            for a in range(2):
                out[b, b2] += r[2 * a + b, 2 * a + b2]
    return out

# ---------------- the three F cases ------------------------------------------
# F[a_basis][ (i, b) ]  with i = 0 for the {0, +} branch, 1 for the {1, -}.
F_CASES = {
    # 1: Alice-local, favors the {0, +} branch (upstream reference)
    1: {"Z": {(0, 0): 1, (0, 1): 1, (1, 0): 0, (1, 1): 0},
        "X": {(0, 0): 1, (0, 1): 1, (1, 0): 0, (1, 1): 0}},
    # 2: Bob-local (F = b; downstream local outcome)
    2: {"Z": {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 1},
        "X": {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 1}},
    # 3: joint, F = i' * b with i' = 1 for the {1, +} branch
    3: {"Z": {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1},
        "X": {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 0}},
}

def bob_marginal(a_basis, F, eps):
    """Reweighted Bob marginal P'_B(b | a): reweight the full joint branches
    P(i,b|a) * exp(eps F), per-setup normalization, marginalize over i."""
    projs = P_AZ if a_basis == "Z" else P_AX
    num = np.zeros(2)
    z = 0.0
    for i in (0, 1):
        for b in (0, 1):
            p = joint_p(projs[i], b)
            w = p * np.exp(eps * F[a_basis][(i, b)])
            num[b] += w
            z += w
    return num / z

def tv(p, q):
    """Total variation distance between two probability vectors."""
    return 0.5 * float(np.sum(np.abs(np.asarray(p) - np.asarray(q))))

def delta_numeric(case, eps):
    F = F_CASES[case]
    return tv(bob_marginal("X", F, eps), bob_marginal("Z", F, eps))

def delta_closed(case, eps):
    """ROUND-5 CORRECTION (case 3): the round-4 form substituted e^|eps| into
    the WHOLE expression -- wrong for eps < 0, because the denominator
    (3+e^eps)(1+e^eps) is NOT invariant under x -> 1/x (at eps=-1: actual
    0.13721 vs the old 0.08081; caught in the round-5 review).  Case 1 is
    symmetric (pure tanh), so it was unaffected."""
    e = np.exp(eps)
    if case == 1:
        return 0.5 * (np.exp(abs(eps)) - 1.0) / (np.exp(abs(eps)) + 1.0)  # 0.5 tanh(|eps|/2)
    if case == 2:
        return 0.0
    return abs(e - 1.0) / ((3.0 + e) * (1.0 + e))

# ---------------- ASCII plot (house convention) ------------------------------
def ascii_plot(xs, ys, title, width=56, height=15):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    xmin, xmax = xs.min(), xs.max(); ymin, ymax = ys.min(), ys.max()
    if ymax - ymin < 1e-12:
        ymax = ymin + 1e-12
    grid = [[" "] * width for _ in range(height)]
    for x, y in zip(xs, ys):
        cx = int((x - xmin) / (xmax - xmin + 1e-15) * (width - 1))
        cy = int((y - ymin) / (ymax - ymin + 1e-15) * (height - 1))
        grid[height - 1 - cy][cx] = "*"
    for i in range(width):
        grid[height - 1][i] = "-"
    for rr in range(height):
        grid[rr][0] = "|"
    lines = [title, ""]
    step = max(1, height // 4)
    for rr in range(height - 1, -1, -1):
        val = ymin + (height - 1 - rr) / (height - 1) * (ymax - ymin)
        tag = (f"{val: .4g}".rjust(9) if (height - 1 - rr) % step == 0 else " " * 9)
        lines.append(tag + " " + "".join(grid[rr]))
    lines.append(f"{'':9} " + "eps ->")
    return "\n".join(lines)

# ---------------- main --------------------------------------------------------
def main():
    print("=" * 78)
    print("DUAL-FIELD -- two-qubit no-signaling check (exact linear algebra)")
    print("                P' ~ P exp(eps F) on |Phi+>; does Alice's basis leak?")
    print("=" * 78)
    print()

    # --- baseline: reduced state + exact joint tables ---
    rho_b = partial_trace_A(RHO)
    assert np.allclose(rho_b, np.eye(2) / 2.0, atol=1e-12), "rho_B must be I/2"
    print("BASELINE (standard QM):")
    print("  rho_B = Tr_A(|Phi+><Phi+|) = I/2 exactly [asserted]")
    print("  Bob's Z-stats are 1/2, 1/2 regardless of Alice's basis (no-signaling).")
    ztab = {i: {b: joint_p(P_AZ[i], b) for b in (0, 1)} for i in (0, 1)}
    xtab = {i: {b: joint_p(P_AX[i], b) for b in (0, 1)} for i in (0, 1)}
    exact_z = {0: {0: 0.5, 1: 0.0}, 1: {0: 0.0, 1: 0.5}}
    exact_x = {0: {0: 0.25, 1: 0.25}, 1: {0: 0.25, 1: 0.25}}
    assert all(abs(ztab[i][b] - exact_z[i][b]) < 1e-12 for i in (0, 1) for b in (0, 1)), \
        "Z joint table mismatch"
    assert all(abs(xtab[i][b] - exact_x[i][b]) < 1e-12 for i in (0, 1) for b in (0, 1)), \
        "X joint table mismatch"
    print("  joint branch tables (exact, asserted):")
    print(f"    Z basis: P(0,0)={ztab[0][0]:.1f} P(0,1)={ztab[0][1]:.1f} "
          f"P(1,0)={ztab[1][0]:.1f} P(1,1)={ztab[1][1]:.1f}")
    print(f"    X basis: P(+,b)=P(-,b)={xtab[0][0]:.4f} (all four = 1/4)")
    print()

    # --- the test ---
    # round-5: negative eps included (the old list hid the case-3 |eps| bug)
    eps_list = [0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, -0.1, -0.5, -1.0]
    names = {1: "Alice-local (F on the upstream branch)",
             2: "Bob-local (F = b, downstream local outcome)",
             3: "Joint/future (F = i'*b, couples upstream x downstream)"}
    worst = 0.0
    print(f"{'case':<46} {'eps':>5} {'Delta_B num':>13} {'Delta_B closed':>15}  verdict")
    for case in (1, 2, 3):
        for eps in eps_list:
            num = delta_numeric(case, eps)
            clo = delta_closed(case, eps)
            dev = abs(num - clo)
            worst = max(worst, dev)
            ok = "PASS" if dev < 1e-9 else "FAIL"
            if eps in (0.0, 0.1, 1.0, -1.0):
                print(f"{names[case]:<46} {eps:>5.2f} {num:>13.2e} {clo:>15.2e}  {ok}")
    print()
    print(f"max |numeric - closed form| over all cases/eps: {worst:.2e}  "
          f"({'PASS' if worst < 1e-9 else 'FAIL'} -- exact linear algebra, tol 1e-9)")
    assert worst < 1e-9, "numerical reweighting deviates from the closed forms"

    # --- known-limit tells ---
    for case in (1, 2, 3):
        assert delta_numeric(case, 0.0) < 1e-12, f"case {case}: Delta_B(0) must be 0"
    print("known-limit tells: Delta_B(eps=0) = 0 in all three cases [asserted] "
          "(standard-QM baseline survives any F at eps=0).")
    print()

    # --- Delta_B(eps) curves ---
    grid = np.linspace(0.0, 2.0, 201)
    for case in (1, 3):
        ys = [delta_numeric(case, e) for e in grid]
        print(ascii_plot(grid, ys, f"Delta_B(eps)  case {case}: {names[case]} "
                                   f"(closed form, verified above)"))
        print()
    print("case 2 (Bob-local): Delta_B(eps) = 0 for all eps (the flat line at 0; "
          "the factorization, asserted in the table).")
    print()

    print("RESULT (round-4 test, 2026-11-21; SCOPED by the round-5 review):")
    print("  case 1 Alice-local:   Delta_B(eps) = 0.5*tanh(|eps|/2) ~ eps/4  -> LEAKS")
    print("  case 2 Bob-local:     Delta_B(eps) = 0 in the TESTED direction only")
    print("                        (Alice->Bob, Bob's Z fixed; factorization).")
    print("                        FLIPPED (Alice fixed Z, Bob chooses Z/X) it LEAKS:")
    print("                        Delta_A(eps) = 0.5*tanh(|eps|/2), 0.2311 at eps=1")
    print("                        (round-5 correction; v2 part A).")
    print("  case 3 Joint/future:  Delta_B(eps) = |e^eps-1|/((3+e^eps)(1+e^eps))")
    print("                        ~ eps/8 (eps>0), ~ |eps|/8 (eps<0)          -> LEAKS")
    print("                        (round-5: the old e^|eps| form was wrong for eps<0)")
    print()
    print("Round-5 reading (full square + both directions in v2): NO outcome-referencing")
    print("F survives the full test -- Alice-local, Bob-local (flipped) and joint all")
    print("leak.  The all-state no-signaling condition forces the weighting to be")
    print("outcome-constant per setup pair (w = c(x,y), absorbed by normalization:")
    print("P' = P) within the v2 scope (2x2, XZ-plane settings, the correlated-state")
    print("family) -- the no-go for the naive branch-reweighting law.  The live escape")
    print("route is to formulate the coupling as a valid (CPTP/linear) evolution of")
    print("rho: observable AND no-signaling-safe (v2 part B, the positive control).")

if __name__ == "__main__":
    main()

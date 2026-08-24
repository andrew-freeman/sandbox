#!/usr/bin/env python3
"""
Dual-Field toy — open problem (d): a direction-dependent (S-odd) information
functional that breaks the symmetry of an otherwise-symmetric drive.

Theory
------
Let S = [ring reversal (i -> -i mod 3) + phase swap (A<->B) + time reversal].
The net current J is ODD under S (a cw hop maps to a ccw hop, so J -> -J).
The base physics P_phys is S-even (the symmetric ratchet).  The dual field
modifies transitions by  P_DF ∝ P_phys * exp(eps*I).  For P_DF to break S (and
hence allow J != 0), the factor exp(eps*I) must be S-odd, i.e. I must be S-ODD:
    I(S(h, y)) = - I(h, y).
Any I DERIVED FROM the symmetric P_phys (e.g. excess predictive information
log[P_phys(y|a,b)/P_null(y|b)]) is S-EVEN, so it CANNOT break S -> J = 0.
That is the control result of the ratchet model.

To get a current, I must itself carry a handedness.  The minimal S-odd
candidate that is still a genuine information measure is CHIRAL PREDICTIVE
INFORMATION: the predictive information signed by the direction of the memory
    I_chir(a,b,y;phase) = sgn(a->b) * log[ P_phys(y|a,b,phase) /
                                           P_null(phase)(y|b) ]
    sgn(a->b) = +1 if a->b is cw, -1 if ccw, 0 if a stay.
Under S: the memory direction flips (sgn -> -sgn) while the log-ratio is
invariant, so I_chir -> -I_chir  (S-odd).  The dual field then reads, for eps>0:
  - after a cw hop:  favour INFORMATIVE outcomes (r**+eps)
  - after a ccw hop: favour ANTI-informative outcomes (r**-eps)
a chiral selection.  The current must come from the handedness in I (flip the
handedness -> flip J).  This is 'information + a chiral reference', NOT
'information from nothing': the direction is an INPUT to I, not an output.

Deliverables: J for (a) the symmetric I (control, =0), (b) chiral I, (c)
anti-chiral I (expect sign flip); the O(eps) scaling; and the chirality-flip
test that localizes the source of the direction.
"""
import numpy as np
import dual_field_toy_ratchet as m

N = m.N
rng = np.random.default_rng(20260823)

def sgn_dir(a, b):
    if b == (a + 1) % N: return +1
    if b == (a + 2) % N: return -1
    return 0

def chiral_table(eps, chirality=1.0):
    """P_DF with I_chir = chirality * sgn(a->b) * log[P_phys/P_null]."""
    if eps == 0.0:
        return m.BASE_TB
    T_ = {}
    for ph in ('A', 'B'):
        for a in range(N):
            for b in range(N):
                Pb = m.BASE_TB[(ph, a, b)]
                e = chirality * sgn_dir(a, b) * eps
                w = np.zeros(N)
                for y in range(N):
                    if Pb[y] > 0:
                        r = Pb[y] / m.PN[(ph, b, y)]
                        w[y] = Pb[y] * (r ** e)
                T_[(ph, a, b)] = w / w.sum()
    return T_

def current(eps, chirality=1.0):
    tb = chiral_table(eps, chirality)
    mats = [m.phase_matrix(ph, tb) for ph in m.phase_seq()]
    pis = m.periodic_ss(mats)
    J = 0.0
    for t in range(m.T):
        pi = pis[t]; ph = m.phase_seq()[t]
        for a in range(N):
            for b in range(N):
                J += pi[m.sidx(a, b)] * (tb[(ph, a, b)][(b + 1) % N]
                                         - tb[(ph, a, b)][(b + 2) % N])
    return J / m.T

def main():
    print("=" * 74)
    print("DUAL-FIELD — open problem (d): direction-dependent (S-odd) information")
    print("=" * 74)
    print("symmetric ratchet (T_A=T_B).  S = [ring reversal + phase swap + time rev].")
    print("J is S-odd; exp(eps*I) must be S-odd (I S-odd) to allow J != 0.")
    print()
    print(f"{'I type':<22} {'eps':>6} {'J(net curr)':>14}")
    print("  [control] symmetric I (S-even):")
    for eps in [0.5, 1.0, 2.0]:
        # symmetric I = the ratchet's own dual field (not chiral)
        J = m.current(eps)
        print(f"{'symmetric (S-even)':<22} {eps:>6.2f} {J:+14.8f}")
    print("  [chiral] I_chir = sgn(a->b) * log[P_phys/P_null]   (S-odd):")
    for eps in [0.5, 1.0, 2.0]:
        print(f"{'chiral  +1 (S-odd)':<22} {eps:>6.2f} {current(eps, +1.0):+14.8f}")
    print("  [anti-chiral] handedness flipped (chirality=-1):  expect J -> -J")
    for eps in [0.5, 1.0, 2.0]:
        print(f"{'chiral  -1 (S-odd)':<22} {eps:>6.2f} {current(eps, -1.0):+14.8f}")

    print("\n  O(eps) scaling of the chiral current (eps=0.1/0.2/0.5):")
    for eps in [0.1, 0.2, 0.5]:
        Jp = current(eps, +1.0); Jm = current(eps, -1.0)
        print(f"    eps={eps:4.2f}  J(+1)={Jp:+.7f} (J/eps={Jp/eps:+.5f})   "
              f"J(-1)={Jm:+.7f}   [J(+1)+J(-1)]={Jp+Jm:+.2e}  (should be ~0)")

    print("\n  VERDICT:")
    print("  - symmetric (S-even) I  -> J = 0  (information alone cannot break S)")
    Jp = current(1.0, +1.0); Jm = current(1.0, -1.0)
    print(f"  - chiral (S-odd) I     -> J = {Jp:+.6f}  (nonzero! S is broken)")
    print(f"  - flip handedness      -> J = {Jm:+.6f}  (sign flips with the chirality)")
    print("  => the direction comes from the HANDEDNESS put into I, not from a")
    print("     neutral information measure.  'information from nothing' is ruled")
    print("     out; 'information + a chiral reference' is realized.")

if __name__ == "__main__":
    main()

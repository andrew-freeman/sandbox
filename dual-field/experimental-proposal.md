# Dual-Field Hypothesis — Experimental Proposal

**Author:** Andrey Bushuev (hypothesis) · drafted with Letta Code
**Date:** 2026-08-23
**Status:** proposal for the "Steps 6+7" of the research program (derive one
quantitative deviation; estimate bounds on ε). Companion to
`README.md` (findings) and `toy/dual_field_toy_ratchet.py` (the model this
proposal operationalizes).

---

## 0. The dominant signal (read this first)

**You cannot yet turn ε on and off in nature — so a direct "measure ε"
experiment is not the near-term play.** ε is (if it exists) a tiny universal
coupling, and the survey's two hardest lessons apply: (a) the collapse-model
lesson — existing interferometry/astrophysics/precision data may *already* bound
the accessible ε to nearly zero; (b) the Valentini lesson — any such deviation is
*hidden by relaxation to equilibrium* and only surfaces in extreme regimes.

**What *is* testable now, and valuable, is a two-track program:**

- **Track 1 — the analog (mechanism, testable in ~1–2 yrs, publishable on its
  own).** Build a real ratchet in which the "information coupling" is a
  **controllable knob** (a feedback "demon" whose gain κ plays the role of ε).
  It runs **three sub-experiments**: (1a) a **symmetric** ratchet + **symmetric**
  feedback — the model predicts J=0 for *all* κ (a neutral information coupling
  cannot rectify a symmetric drive; confirms the symmetry argument); (1a′) a
  **symmetric** ratchet + **chiral** feedback — the model predicts **J≈0.16·κ**,
  and *flipping the handedness flips J* (information + a chiral reference drives a
  current; the direction is an input to the feedback rule); (1b) a **geometry-
  asymmetric** ratchet (nonzero J₀) + feedback — the ε-knob *modulates* the existing
  current (J(κ)=J₀+δJ(κ)). Together these (i) prove the mechanism is real and
  *measurable*, (ii) cleanly separate the three cases — "create from nothing" (no,
  by symmetry), "create with a chiral reference" (yes), "modulate" (yes) — and (iii)
  give a **calibrated template of the ε-signature** (current + information +
  dissipation, moving together).
- **Track 2 — the bounds (fundamental, mostly analysis + one precision
  measurement).** Use the theory + existing high-precision data to **upper-bound
  the fundamental ε**, and design a targeted search in the regime where ε would
  be largest.

**The load-bearing connection:** Track 1 teaches you the *shape* of the
ε-signature (current + information + dissipation, moving together); Track 2
searches for that *same shape, unforced, at tiny amplitude*, in a precision
small-system experiment. The analog is the calibration for the fundamental
search. **Bottom line in one line:** build a ratchet with a real ε-knob, prove
the effect is real and measurable, then use it to point the fundamental search.

---

## 1. What we're actually testing (two levels — don't conflate)

- **Level 1 — the mechanism (testable now, via the analog).** *Does a
  history-dependent (information) bias rectify a symmetric drive into a directed
  current?* If **no** → the hypothesis's core mechanism is wrong and the program
  stops here (a clean, valuable negative). If **yes** → the mechanism is real;
  proceed to Level 2.
- **Level 2 — the fundamental (bounds only).** *Is there a universal ε in
  nature?* Not a detection experiment near-term; a **bounding + targeted-search**
  program.

This separation is the whole ballgame. Most bad "new physics" experiments fail by
pretending Level 2 is a detection when it's a bound. We won't.

---

## 2. Track 1 — the analog information ratchet

### 2.1 Core design idea

The dual-field coupling is a **history-dependent modification of transition
probabilities**: `P_DF(y|past) ∝ P_phys(y|past)·exp(ε·I(past,y))`. The natural
physical realization of "modify transitions based on the past" is a **Maxwell's
demon / feedback-controlled ratchet**: a controller measures the system's
*history* and applies a **history-dependent kick**. The **feedback gain κ is the
ε-analog** — and crucially, it's a knob you can turn up and down. That
on/off capability is exactly what's missing in any fundamental test.

**The single most important design decision — the reparameterization
discriminator** (this is the #1 kill from the survey, and the experiment must
kill it *by construction*):

- A feedback that depends **only on the present state** can be absorbed into a
  different effective potential → it's a **reparameterization**, not an
  information effect.
- A feedback that depends on the **past beyond the present** (the excess
  predictive information) is **non-Markovian and not absorbable** → a genuine
  information effect.

So the device must implement **history-dependent** feedback, and the experiment
must *also* run the **memoryless (state-only) control** and show it **cannot**
reproduce the effect. "No state-only feedback can do it" is the direct,
experimental version of "it's not a reparameterization." This control is not
optional — it's what makes the result mean something.

### 2.2 Platforms (ranked)

| | Colloidal (holographic optical) | Superconducting qutrit | Single-electron box |
|---|---|---|---|
| 3 states | 3-well ring potential (optics) | 3 levels of a qutrit | 3 charge configs |
| drive | periodic rocking of the wells | periodic modulation of qutrit freqs | periodic gate modulation |
| memory | tracked position history (last 2 sites) | qutrit state + ancilla qubit | charge history |
| demon (feedback) | position/history-dependent optical force | real-time readout → history-dependent control pulse | charge readout → history-dependent gate |
| κ (ε-analog) | feedback gain | feedback gain | feedback gain |
| measurability | good (position, heat from trajectory); ~µm, room temp | **best** (µs, kT-scale, real-time feedback is mature) | moderate |
| maturity | **very high** (information engines are an established field) | high (qutrits + real-time Q feedback are active) | moderate (demon theory mature; closed loop harder) |
| time-to-first-data | **months** | ~1–2 yrs (cryo + microwave stack) | ~1–2 yrs |

**Recommendation:** **lead with colloidal** (first data in months, the
mechanism is proven or falsified fast, lowest cost), and **build the
superconducting qutrit in parallel** for the highest-SNR, cleanest TUR +
information measurement — it's also the most "fundamental-looking" realization
and doubles as the hardware for Track 2's precision search. Single-electron box
is a reasonable middle path if either of the above is inaccessible.

### 2.3 Mapping (toy model → experiment)

| toy model | colloidal | superconducting |
|---|---|---|
| states {0,1,2} | 3 optical wells (ring) | qutrit levels \|0\r,\|1\r,\|2\r |
| 2nd-order memory (a,b) | last 2 sites, tracked | qutrit state + ancilla |
| rocking drive (A/B) | periodic well rocking | periodic freq modulation |
| `exp(ε·I)` coupling | history-dependent optical force | history-dependent control pulse |
| ε | feedback gain κ | feedback gain κ |
| I (excess pred. info) | MI(history → future site) | MI(history → future state) |
| current J | net hopping rate around ring | net transition rate around ring |
| Sdot | heat to bath (from trajectory) | heat/work (from control + state) |

### 2.4 Predicted signatures (pre-registered, from the toy models)

**Sub-experiment 1a — symmetric ratchet (control).** Measured vs κ:
1. **J(κ) = 0 for *all* κ** — the information coupling does *not* rectify a
   symmetric drive (the model's §3c control result, now verified to machine
   precision). A nonzero J here would *break* the symmetry argument — that would
   be the "powering from nothing" signal, treated as the open hypothesis (d).
2. **I(κ) rises monotonically** — information selection, independent of current.

**Sub-experiment 1a′ — symmetric ratchet + chiral feedback (the §3d result).**
The feedback rule is *chiral* (S-odd): after a cw hop it favors informative
outcomes, after a ccw hop it favors anti-informative ones (chirality = the
handedness). Measured vs κ:
2′. **J(κ) ≈ 0.16·κ** (clean O(κ)) — information + a chiral reference *drives* a
   current from a symmetric drive.
3′. **Flip the handedness → J flips sign** (J(+handed)+J(−handed)≈0) — the current
   is an *odd function of the chirality*, localizing the source of the direction to
   the feedback rule's handedness, not to the information per se.

**Sub-experiment 1b — geometry-asymmetric ratchet (nonzero J₀).** Measured vs κ:
4. **J(κ) = J₀ + δJ(κ)**, J₀≠0 (standard physics), and **δJ(κ) ≈ c·κ** for small κ
   (toy 3-state: c≈−0.003 in model units; sign parameter-dependent) — the ε-knob
   *modulates* an existing current.
5. **I(κ) rises monotonically** (information selection).
6. **TUR satisfied:** E = 2J²/(D·Sdot) ≤ 1, and the device **trades efficiency for
   information** (E↓ while I↑ as κ↑).

The joint (J, I, Sdot) manifold vs κ is what carries the signal — a single number
at a single κ is not. The 1a / 1a′ / 1b split is the whole point: it separates
*create-from-nothing* (no), *create-with-a-chiral-reference* (yes), and *modulate*
(yes).

### 2.5 Decision rules (what the data means)

- **1a: J(κ)=0 for all κ** → the symmetry holds (a *neutral* information coupling
  does *not* create a current from a symmetric drive). A nonzero J(κ) *here* (with
  symmetric feedback) would contradict the symmetry argument — it would mean the
  feedback is secretly chiral, so check the rule's handedness.
- **1a′: J(κ)≈0.16·κ and flipping the handedness flips J** → the §3d result
  reproduced: information + a chiral reference drives a current; the direction is
  an input to the feedback rule (the Onsager–Casimir / reciprocity content).
- **1b: J(κ)=J₀+δJ(κ) with δJ∝κ, and (J, I, Sdot) vs κ all trace the toy curve
  jointly** → theory confirmed at the mechanism level (information *modulates* the
  current; a reparameterization can fit one number, not the whole manifold).
- **A state-only (memoryless) feedback reproduces it** → it was a
  reparameterization; the hypothesis's mechanism is *weakened* (important
  negative — keep it).
- **State-only feedback fails, history-dependent succeeds** → the information
  effect is real and non-absorbable (the reparameterization kill is closed).
- **E > 1** → would be a generalized-second-law violation (won't happen; it's a
  consistency check on the apparatus).

### 2.6 Killing the reparameterization confound (explicit)

Two independent lines, both must hold:
1. **The knob argument.** κ is a genuine control you turn; a reparameterization
   has no κ. A coordinated (J, I, Sdot) *response* to κ is by construction not a
   reparameterization.
2. **The history argument.** The effect requires *past-beyond-present* feedback;
   the state-only control is the null. Both are measured; only the history
   channel survives.

---

## 3. Track 2 — bounds on the fundamental ε

**Where ε would be largest.** The coupling scales with I (information), so ε's
footprint is largest in **small, nonequilibrium, memory-rich,
least-relaxed** systems — and hidden where relaxation to equilibrium is fast
(the Valentini hiding mechanism). That points at exactly the precision
small-system thermodynamics platforms from Track 1 (minus the feedback).

**Mine existing data first (cheap, and it may end the question).** If ε were
present at a detectable level, these high-precision tests would already show a
deviation — their null results are **upper bounds**:
- Precision **fluctuation-theorem / TUR** tests (any residual beyond standard
  theory → bound).
- **Born-rule** tests — the Valentini program (arXiv:2505.07510; NMR three-path
  arXiv:1207.2321; high-energy-collision test).
- **Collapse-model** interferometry / condensed-matter / astrophysics bounds
  (the method template — §7 of the survey).

**The targeted experiment.** Run a precision TUR / current-fluctuation
measurement in an **unforced** small system (the superconducting qutrit, no
feedback), and search for a tiny residual deviation from the standard prediction
— **interpreting the residual through the Track-1 template** (the exact (J, I,
Sdot) shape ε would imprint). A null → a quantitative **bound on ε**; a
consistent signal → the first detection claim.

**"Why hasn't ε been seen yet" (the hiding mechanism to predict):** relaxation
to equilibrium washes out the information bias at low driving / low energy; the
bias survives where the system is driven and memory-rich. The theory must
predict *where it hides and where it leaks* — that prediction is what makes Track
2 a test rather than a hope.

---

## 4. The knobs (agency-first: what changes outcomes, what to measure, what next)

| knob | what it does | measure | expected δ (toy units) | N to resolve | do next |
|---|---|---|---|---|---|
| κ (feedback gain = ε-analog) | turns the information effect up/down | J, D, Sdot, I | 1a: J stays 0; 1b: δJ≈c·κ (3-state c≈−0.003, sign param-dep); I rises ~340% (κ 0→2) | ~10³–10⁴ hops (κ is large → easy) | sweep κ; fit δJ(κ) + the (J,I,Sdot) manifold |
| memory depth (1→2 states) | sets how much history the demon uses | J, I | 2nd-order > 1st-order | ~10⁴ | confirm I needs the 2nd order |
| drive asymmetry / duration | sets the rectification ceiling | J(κ=0) | J(0) should stay ≈0 | ~10³ | verify the null (symmetric) |
| history vs state-only feedback | the reparameterization discriminator | J | state-only can't reach the history value | ~10⁴ | run both; compare |
| (Track 2) ε, unforced | the fundamental coupling | residual J, D, Sdot | ~0 (bound), or tiny | 10⁵–10⁶ hops | fit a bound on ε |

**Read:** in the analog, κ is a *large, controllable* number, so the signal is
easy (10³–10⁴ hops). The 10⁵–10⁶-hop requirement is for the *fundamental* ε
(Track 2), where the signal is tiny — that's why Track 2 is a bounds program.

---

## 5. Risks & failure modes

| risk | what it means | mitigation |
|---|---|---|
| state-only feedback also works | it was a reparameterization; mechanism claim weakened | keep the null run as the headline control; report honestly |
| colloidal heat/entropy accounting is noisy | Sdot/TUR leg is soft on the colloidal platform | superconducting qutrit for the clean TUR; treat colloidal as the mechanism proof, not the precision instrument |
| feedback latency smears the history channel | the demon can't actually read the past fast enough | verify κ-bandwidth >> hopping rate; otherwise the "history" collapses to "state" (a tell) |
| ε already bounded to ~0 by Track-2 existing data | fundamental detection is dead near-term | the bounds are still the result; pivot the program to the mechanism (Track 1) + the hiding-mechanism prediction |
| the analog is "just a known Maxwell's demon" | novelty questioned | the contribution is the *ratchet + the (J,I,Sdot) ε-signature template + the clean symmetry/modulation separation (1a vs 1b)*, not "a demon exists" |

---

## 6. Timeline & resources (engineering realism)

- **Phase 0 (now, ~weeks):** finalize this proposal; pick platform; literature
  lock-down for the feedback-ratchet + TUR-precision refs (see Appendix, flag the
  "verify" items).
- **Phase 1 (months): colloidal build.** Holographic optical trap, 3-well ring,
  real-time tracking + feedback loop. First data: J(κ), the memoryless control,
  the (J, I, Sdot) manifold. *Goal: mechanism proven or falsified.*
- **Phase 2 (parallel, ~1–2 yrs): superconducting qutrit.** Cryo + microwave +
  real-time readout/feedback. Clean TUR + information at kT scale; becomes the
  Track-2 precision-search instrument.
- **Phase 3 (parallel, analysis): Track 2 bounds.** Mine existing FT/TUR/Born-rule
  data; derive the ε bound; write the hiding-mechanism prediction.
- **Resources:** Phase 1 = 1 optical-tweezers table + 1–2 postdocs (optics +
  stochastic-thermo analysis). Phase 2 = a cryo/microwave superconducting group
  (collaboration, not solo). Phase 3 = analysis (cheap, mostly me + you).

---

## 7. Bottom line

You can't switch ε on in nature yet — so **build it as a knob in a real ratchet
(Track 1)**: prove the effect is real and measurable, and learn the exact shape of
the signature. The model's honest predictions: a *neutral* information coupling
**modulates** an existing current, **selects** information, but does **not** rectify
a symmetric drive (J=0 for all κ); a *chiral* one **does** drive a current (J≈
0.16·κ), with the direction an input to the rule. So Track 1 runs all three — the
symmetric control (1a), the chiral drive (1a′), and the asymmetric ratchet (1b) —
which cleanly separates create-from-nothing / create-with-a-reference / modulate.
Then **point that template at an unforced precision system (Track 2)** and either
detect ε or bound it. The reparameterization kill is closed *by design*
(history-dependent feedback + the state-only null). This turns a speculative seed
into a two-track, falsifiable, instrumented program.

---

## Appendix — references (with confidence flags)

**Confident (cited in the survey):**
- Single-electron demon (theory): Strasberg et al., arXiv:1210.5661.
- Information thermodynamics / generalized 2nd law: Sagawa & Ueda, arXiv:1111.5769.
- TUR: Horowitz & Esposito, Nat. Phys. 10, 144 (2014); Maes & Netroy, EPL 126, 30005 (2019).
- Born-rule test (Valentini template): arXiv:2505.07510; NMR three-path, arXiv:1207.2321.
- Collapse-model bounds method: Bassi & Ghirardi, Phys. Rep. 379, 257 (2003); arXiv:1601.03672, arXiv:1901.10963, arXiv:2406.04463.

**Established paradigm, specific refs to verify before citing in a paper:**
- Feedback-driven Brownian ratchets / information engines (the colloidal
  platform): the Toyabe–Sasaki–Horibe–Ueda line (information-to-energy
  conversion; feedback ratchets). *Verify exact IDs.*
- Superconducting real-time measurement + feedback / quantum feedback control
  (the qutrit platform): active field. *Verify exact IDs + which groups have
  closed-loop qutrit feedback.*
- Precision TUR / fluctuation-theorem experiments (the Track-2 data source).
  *Verify which platforms have the tightest current-fluctuation bounds.*

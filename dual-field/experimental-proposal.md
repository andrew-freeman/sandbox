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
  This (i) proves the mechanism is real — information *powers* the motor, (ii)
  proves the signature is *measurable*, (iii) identifies the cleanest observable
  and the confounds, and (iv) gives you a **calibrated template of exactly what
  the ε-signature looks like**. It's a genuine new device: an
  *information-powered ratchet*.
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

### 2.4 Predicted signatures (pre-registered, from the ratchet model)

Measured as functions of κ (the ε-analog):

1. **J(κ=0) = 0** — the symmetric drive rectifies nothing (control).
2. **J(κ>0) > 0** — information rectifies the drive.
3. **δJ = J(κ)−J(0) > 0**, and **δJ ≈ c·κ** for small κ (toy: c≈+0.004 in model
   units; +20% at κ=1) — *information powers the motor*.
4. **I(κ) rises monotonically** (toy: ~340% from κ=0→2) — information selection.
5. **TUR satisfied:** E = 2J²/(D·Sdot) ≤ 1, and the device **trades efficiency
   for information** (E↓ while I↑ as κ↑).

### 2.5 Decision rules (what the data means)

- **J(0)=0, J(κ)>0, δJ∝κ** → mechanism validated (information powers the motor).
- **(J, I, Sdot) vs κ all trace the toy curve jointly** → theory confirmed at the
  mechanism level (a reparameterization can fit one number, not the whole
  manifold).
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
| κ (feedback gain = ε-analog) | turns the information effect up/down | J, D, Sdot, I | δJ≈+0.004·κ; I +340% (κ 0→2) | ~10³–10⁴ hops (κ is large → easy) | sweep κ; fit δJ(κ) |
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
| the analog is "just a known Maxwell's demon" | novelty questioned | the contribution is the *ratchet + information-powers-the-current* result + the ε-signature template, not "a demon exists" |

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
(Track 1)**: prove information powers the motor, prove it's measurable, and learn
the exact shape of the signature. Then **point that template at an unforced
precision system (Track 2)** and either detect ε or bound it. The reparameterization
kill is closed *by design* (history-dependent feedback + the state-only null).
This turns a speculative seed into a two-track, falsifiable, instrumented program.

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

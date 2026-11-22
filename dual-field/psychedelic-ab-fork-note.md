# Psychedelic phenomenology as a diagnostic for the D_causal / D_min fork

**Date:** 2026-11-21
**Status:** argument (§1–4) + 2-layer formalization toy (`toy/dual_field_toy_2layer.py`,
pre-registered closed-form predictions in §5, results in §6) + **round-4 external
review and corrections (§9–10, same day)** — toy metrics corrected (H_1 vs H_∞,
persistence), one-pager revised (`ab-fork-one-pager.md`).
**Companion to:** the depth4 fork (the open branch since 2026-08-26). This note adds
one argument to the fork's decision record: **under the stated "experience
assumption", the experience-relevant branch of the fork selects D_min (B).**

## 1. The claim

Psychedelic action is a natural, low-energy, reproducible demonstration of which
layer "reality-as-experienced" tracks.

Pharmacology (the established part — the "biology"):

- **LSD:** 5-HT2A agonism at the entorhinal cortex → the entorhinal–hippocampal
  *disconnection* dissolves (stale/random input bleeds into ongoing cognition);
  REBUS: the free-energy landscape flattens, top-down priors lose grip; the
  "ego dissolution" peak correlates with DMN suppression + increased global
  integration.
- **Ketamine:** NMDA antagonism → disinhibition of glutamatergic transmission;
  thalamocortical sensory gating disrupted → dissociation.

In both cases: **the substrate (the brain's causal dynamics) is nearly unchanged;
what changes are parameters of the generative model** (receptor gain / gating).
The experienced "reality" changes drastically, and the change tracks the *model*
parameters, not the substrate. Sobriety and the altered state are two "realities"
sharing one substrate, differing in the mapping.

**Claim: "reality-as-experienced" is an object of the generative/description
layer (B) — the model output — not of the causal-process layer (A) — what
physically happened.**

## 2. The inference to the fork (assumption stated)

The depth4 fork: does the dual field weight **D_causal** (how the universe really
propagates, = N; a property of what happened; layer A) or **D_min** (the shallowest
circuit that reproduces the trajectory, = O(log N); a property of the space of
laws/descriptions; layer B)?

1. If the dual field is meant to bear on experience — and the "what is reality"
   question *is* an experience question — the depth it weights should be the one
   experience tracks.
2. By §1, experience tracks B.
3. **Therefore, under the experience assumption, the experience-relevant branch of
   the fork selects D_min (B).**

**Stated assumption (the entire force of the argument):** this diagnoses the fork
*only if* the dual field is meant to bear on experience. If the dual field is purely
about the substrate (independent of experience), the psychedelic is a model-layer
datum and does not arbitrate the fork.

**Status of the argument:** analogical / structural, not a proof. The psychedelic is
a *biological instance* of "fixed base, variable mapping." It demonstrates (i) the
structure (a free parameter between substrate and experience) and (ii) which layer
experience tracks. It does *not* establish that the substrate-level ε is the same
parameter, nor anything about the substrate's ontology.

## 3. The free-parameter rhyme (structural observation, not a theorem)

"Free parameter on a fixed base" recurs at each layer:

- **substrate layer:** the dual field's ε on the fixed P_phys;
- **model layer:** the psychedelic gain (5-HT2A / NMDA tuning) on the fixed substrate;
- **description layer:** the A/B fork *is* "which description do you weight" — a
  free choice of description.

Open question: same parameter, or similar structures? The rhyme is real; the
identity is open. The psychedelic is the cheapest reproducible demonstration of the
structure — the "Bicycle Day" of the free-parameter claim.

## 4. Brutal limits — what the psychedelic does NOT do

- It is a **model-layer probe, not a substrate-layer probe.** Silent on the
  substrate's ontology ("why this physics, why a fact of the matter at all").
- It **constrains** the A/B choice (→ B, under the experience assumption); it does
  not **answer** the substrate question.
- It is **not** one of the "hundreds of similar hypotheses": it is a *datum* (a
  natural model-layer phenomenon), not a *hypothesis* about the substrate.
  Different kinds of objects. The dual field's distinctiveness against the hundreds
  is the falsifiable ε (one universal coupling predicting residuals across
  experiments); the psychedelic is a datum to be explained or borne on, not a
  competitor.

## 5. 2-layer formalization toy — design + pre-registered predictions

`toy/dual_field_toy_2layer.py` (numpy only, ASCII plots; self-contained).

- **Layer A (substrate):** a 1st-order Markov chain, P(stay) = s = 0.99 (the
  depth2/3 family; ξ ≈ 50). ONE realized trajectory H (fixed seed) = the actual
  causal history. D_causal(H) = N sequential steps — a property of what happened,
  invariant.
- **Layer B (experience):** a binary symmetric channel (BSC) on H with crossover
  γ ∈ [0,1] = the "gate" — a direct formalization of entorhinal disconnection
  (with probability γ, independent random input bleeds into the ongoing model).
  γ=0 = perfect copy (sobriety); γ=1 = deterministic inversion (a mirror world —
  stable but alien); γ=0.5 = maximum disconnection (the experience is white noise:
  no information, no temporal structure).
- **A/B illustration:** H is identical across all γ (checksum-asserted); the output
  statistics Y(γ) vary freely.

**Pre-registered predictions** (closed forms; fair substrate p(x=1)=0.5, h = binary
entropy in bits, ρ_X = 2s−1 = 0.98 — the toy verifies each empirically):

| γ    | I(X;Y) = 1 − h(γ) | ρ_Y = ρ_X(1−2γ)² | H_rate(Y) = h((1+ρ_X(1−2γ)²)/2) |
|------|-------------------|------------------|--------------------------------|
| 0.00 | 1.000             | +0.980           | 0.0808                         |
| 0.10 | 0.531             | +0.627           | 0.694                          |
| 0.25 | 0.189             | +0.245           | 0.956                          |
| 0.50 | 0.000             | 0.000            | 1.000                          |
| 0.75 | 0.189             | +0.245           | 0.956                          |
| 1.00 | 1.000             | +0.980           | 0.0808                         |

Shapes (sign/shape pre-registered, per house method): I(γ) and ρ(γ) are U-shaped
(minimum at 0.5, symmetric in γ); H_rate(γ) is ∩-shaped (maximum at 0.5,
symmetric); the compression ratio is ∩-shaped (incompressible at γ=0.5,
γ=0 and γ=1 comparable — the mirror world compresses like the original). A derived
quantity of interest: the experience's persistence
ξ_Y = 1/|ln ρ_Y| collapses from ≈50 (substrate) to ≈2 already at γ=0.1 — the
substrate's long-range temporal structure dissolves at a *small* gate opening.

**Round-4 corrections to the metrics above (see §9):** (1) the channel is the
bit-flip channel with crossover γ (the "random input bleed" wording of §5's
design text describes a γ/2 channel); (2) the H_rate column is H_1 = the
1-step conditional entropy — Y is a hidden-Markov process, and its true entropy
rate H_∞ (Bayes filter) is 0.534 at γ=0.1 / 0.358 at γ=0.05, below H_1's
0.694 / 0.479 (the ∩-shape survives, the magnitudes do not); (3) the ξ_Y line
is a metric artifact — the corrected 1/e memory scale runs 49.5 → 27.4 at
γ=0.1 (−45%), is absent for γ ∈ (0.19, 0.81), and the long-lag decay rate is
**invariant** (amplitude ×(1−2γ)² only): the substrate's time is hidden, not
destroyed.

**Known-limit tells (hard asserts in the toy):** γ=0 → Y≡H exactly; γ=1 → Y≡1−H
exactly; γ=0.5 → I_emp≈0 and H_emp≈1 (within MC tolerance).

**Expected reading (what the toy does / does not establish):**

1. A is invariant under γ (same trajectory, same causal unfolding); B is freely
   parameterized → the experience is a B-object.
2. The experienced "reality" is *not monotone* in the gate: the extremes (γ=0,1)
   are both stable, low-entropy, information-bearing realities (one yours, one an
   alien mirror); psychedelic destabilization lives in the *intermediate* regime
   and — phenomenologically — in *fluctuating* γ(t). A static BSC captures the
   free-parameter structure; the destabilization phenomenology needs time-varying γ
   (natural extension, §7.1).
3. Information retention ≠ perceptual stability: at γ=1, I = 1 (the experience
   carries full information about the substrate) but the mapping is inverted; a
   learned inversion could make it fully stable. "Alienness" is not captured by I
   or ρ alone.
4. S/D taxonomy at the experience layer: at γ=0.5 the experience has maximum S
   (incompressible, H_rate=1, I=0) and minimum generative structure (white noise →
   D_min → 0) — the S/D fork is *maximized at the experience layer* under maximum
   disconnection.

**Limitations:** static, memoryless channel; 1-D substrate; the toy shows
structure, not ontology (by design: silent on the substrate).

## 6. Results (2026-11-21, `python3 toy/dual_field_toy_2layer.py`)

**All pre-registered predictions confirmed.** Layer A invariant across all rows
(checksum `2ef5809aebc5a119`; ρ_A=+0.9797 vs theory +0.98; H_rate=0.0818 vs
0.0808; ξ_A=48.7; D_causal=N=200 000). Empirical vs closed form, all 13 γ rows
PASS (max deviation 0.17 tolerance units):

| γ | I_emp / I_theory | ρ_emp / ρ_theory | H_rate_emp / theory | zlib ratio | ξ_Y |
|---|---|---|---|---|---|
| 0.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.121 | 48.7 |
| 0.10 | 0.5336 / 0.5310 | +0.6293 / +0.6270 | 0.6915 / 0.6941 | 0.665 | 2.2 |
| 0.30 | 0.1177 / 0.1187 | +0.1541 / +0.1568 | 0.9827 / 0.9822 | 0.973 | 0.5 |
| 0.50 | 0.0000 / 0.0000 | −0.0012 / 0.0000 | 1.0000 / 1.0000 | 1.001 | 0.0 |
| 0.90 | 0.5302 / 0.5310 | +0.6269 / +0.6270 | 0.6940 / 0.6941 | 0.668 | 2.1 |
| 1.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.121 | 48.7 |

(full 13-row table + 4 ASCII plots in the toy output; known-limit asserts
γ=0→Y≡H and γ=1→Y≡1−H pass exactly.)

Readings:

1. **A invariant, B freely parameterized** — the same trajectory H (one causal
   unfolding, D_causal=N) yields 13 different experienced statistics. The
   experience is a B-object.
2. **The predicted shapes all hold**: I(γ) and ρ(γ) U-shaped (min at 0.5),
   H_rate(γ) and the zlib ratio ∩-shaped (max at 0.5). The γ→1−γ mirror symmetry
   of the U-shape is empirically visible (γ=0.1 vs γ=0.9 rows agree to MC noise:
   I 0.5336/0.5302, ρ +0.6293/+0.6269, zlib 0.665/0.668).
3. **Temporal structure dissolves at a SMALL gate opening**: ξ_Y collapses
   48.7 → 2.2 already at γ=0.1 (and 0.53 by γ=0.3). The substrate's long-range
   persistence — the "world's temporal structure" — is the first thing to go.
   *(Round-4: the run's numbers are correct; the ξ metric was a 1st-order
   extrapolation on a hidden-Markov process. Corrected statement: the
   experienced correlation amplitude is ×(1−2γ)² (the 1/e memory scale
   49.5 → 27.4 at γ=0.1, absent for γ ∈ (0.19, 0.81)) while the long-lag DECAY
   RATE is invariant — the substrate's time is hidden, not destroyed. §9.3.)*
4. **Information retention ≠ perceptual stability**: γ=1 keeps I≈1 (the
   experience carries essentially full information about the substrate) under an
   inverted mapping, with the same persistence and compressibility as γ=0
   (zlib 0.121 at both extremes). A stable-but-alien mirror world is
   information-theoretically indistinguishable from sobriety — "alienness" is
   not captured by I, ρ, H_rate, or compressibility.
   *(Round-4: re-framed — I/ρ/H/zlib are all invariant under symbol relabeling,
   so the indistinguishability holds BY CONSTRUCTION; the finding is that the
   four standard measures are blind to representation, and "alienness" is a
   fourth quantity. §9.)*
5. **S/D at the experience layer**: at γ=0.5 the experience is maximally
   incompressible (zlib→1.001, H_rate=1, I=0) — maximum S — while its
   generative structure is white noise (D_min→0). The S/D fork is maximized at
   the experience layer under maximum disconnection, exactly as pre-registered.

Caveats carried over from §5: static, memoryless channel; 1-D substrate;
structure, not ontology (the toy is silent on the substrate by design).

## 7. Next steps

1. **Fluctuating-γ extension:** γ(t) as a slow meta-process; measure the
   destabilization signature (local time-varying I, fragmentation of temporal
   structure) — formalizes "the bad trip is not the maximum of the parameter but
   the intermediate/fluctuating regime."
2. **Andrey's call on the fork is still pending.** This note adds a B-leaning
   argument under the experience assumption; it does not settle the fork.
3. (Open) Does the dual field predict a *substrate-level* free parameter analogous
   to the model-level gain? Caveat: ε changes P_phys's dynamics by definition, so
   the "fixed substrate" analogy is strained at that layer — the clean reading is
   that the experience-relevant weight lives in description space (B), i.e. the
   D_min side of the fork.
4. **Two-knob (γ, M) toy (round-4 reviewer proposal, 2026-11-21):**
   B = M(A) ⊕ E_γ with γ ∈ [0, ½] = noise/disconnection and M = a deterministic
   remapping. "Stable alien world" = (γ≈0, M≠I) — high fidelity, high stability,
   radically transformed mapping. Replaces the 1-D BSC's artificial U-turn with
   a 2-D phenomenological phase space; the 1-D toy remains the
   M ∈ {identity, inversion} slice. Build after the fluctuating-γ extension
   (or instead of it, if the review's "park the psychedelic extension"
   guidance wins — the ε-program's two-qubit check is the program-level
   priority, §9).

## 8. Recreational mapping (2026-11-21, requested translation)

γ = the "disconnection gate". LSD/psilocybin/DMT (5-HT2A) and ketamine (NMDA) are
the same axis via different receptors with different bleed content: LSD bleeds in
memory/meaning (entorhinal); ketamine bleeds in sensory/self-model disruption
(thalamocortical). Experience is set by position on the axis + γ's dynamics
(stable vs fluctuating), not by which drug.

Toy variable -> trip-speak: I = fidelity; xi_Y = temporal binding; H_rate =
novelty/meaning-generation; zlib = predictability of the experienced stream.

- **Time goes first, at small gamma** (xi_Y 48.7->2.2 at gamma=0.1): microdose
  "looser time" = LSD "eternal now" = k-hole "time stop", same effect at
  different gamma.
- **The peak is the middle, not the maximum** (gamma=0.5 = max novelty, zero
  fidelity/structure): past the peak, "more" yields a NEW STABLE reality (the
  gamma=1 mirror world: stable, structured, alien, full fidelity = the structural
  signature of the dome/tunnel/cosmic-geometry reports), not more chaos. The
  gamma=1 bit-flip is a minimal stand-in for "reorganization".
- **The bad trip is dynamical, not amplitudinal**: high *stable* gamma = a stable
  (possibly terrifying) mirror world; the bad trip = *fluctuating* gamma (oscillating
  between real and alien without resolving). Set/setting = gamma-stabilizers -> the
  mechanistic reason set/setting is the #1 outcome lever, not "take less".
- **Flashbacks/HPP = gamma stuck half-open** (residual bleed of mirror-world
  structure). **Ego death** = self-model dissolution in the high-gamma regime; a
  "lastingly changed self" = the baseline gamma shifted (plasticity); integration
  = re-tuning to the new baseline.
- **Three-axis shelf:** (a) GAIN controls — substrate volume, mapping intact
  (alcohol down = dull/blur; caffeine/amphetamines up = sharpen); (b) GATE
  controls — gamma (LSD family: slow, meaning/vision; ketamine: fast,
  dissociation/self; DMT = a fast gamma spike, a 15-40 min sweep through the
  axis); (c) SOCIAL channel — MDMA ~ close the gate + amplify the social signal
  (amplifier of the other-model, not destabilizer of the self-model: why it is an
  empathogen, not a psychedelic).

Limits: single-gate lumping (real drugs hit several receptors; the toy folds them
into one gamma); the gamma<->dose map is structural, not calibrated; the
fluctuating-gamma claim is a prediction pending the fluctuating-gamma extension
(S7.1).

## 9. Round-4 review — two external reviews + agent re-verification (2026-11-21)

**Provenance.** The one-pager was sent to two external models (ChatGPT/
OpenAI-5.6 and Claude Sonnet 5 — the "big brothers"; raw files
~/ab_toy_feedback_chatgpt, ~/ab_toy_feedback_claude). The agent re-verified
every numerical claim with its own code before integrating. **Verdict: all four
technical objections hold, and the two reviewers agree with each other almost
completely** (their 0.533 vs 0.536 discrepancy is their own MC noise). The
corrections make the A/B idea better, not worse; the "weirdest part" (alienness
as a fourth quantity) survives and strengthens.

**The four technical objections (each agent-verified):**

1. **The verbal channel ≠ the implemented channel.** The one-pager text
   ("replaced by an independent random bit") describes a channel with
   effective crossover γ/2 — it tops out at white noise and never reaches the
   mirror; the toy implements the bit flip (crossover γ). Agent check:
   random replacement measured an effective flip rate of 0.0491 at γ=0.1
   (≈γ/2) and 0.4983 at γ=1. Fix: text now says bit-flip channel (crossover γ);
   the trap is noted in the toy docstring.
2. **H_rate was actually H_1, the 1-step conditional entropy.** Y is a
   hidden-Markov process (BSC observation of a 1st-order chain), so the true
   entropy rate H_∞ = E[h(q_t)] (Bayes filter) < H_1. Agent check (independent
   filter, correct predict→observe order): H_∞ = 0.5338 at γ=0.1 (reviewers:
   0.533 / 0.536) vs H_1 = 0.6904; H_∞ = 0.3579 at γ=0.05 (Claude: 0.355) vs
   0.4750. The ∩-shape survives; the magnitudes did not. Fix: the toy reports
   both — H_1 with its closed form; H_∞ filter-measured with limits
   (0.0808/1/0.0808) + γ↔1−γ symmetry asserted.
3. **"Time goes first" (the best headline) is a metric artifact.** The old
   ξ_Y = −1/ln ρ_Y(1) extrapolated 1st-order Markov from lag 1, but Y is not
   1st-order. True correlation: C_Y(k) = (1−2γ)²ρ_A^k for k≥1 — noise scales
   the AMPLITUDE, not the decay rate. Agent check: C_Y(k)/C_X(k) flat at
   0.643–0.656 over lags 1–40 at γ=0.1 (theory 0.64); measurable-lag slope of
   ln C_Y = −0.0212 vs ln ρ_A = −0.0202. Corrected result: the 1/e memory
   scale (crossing from the C(0)=1 baseline) runs 49.5 → 27.4 at γ=0.1 (−45%)
   and is ABSENT for the whole middle band γ ∈ (0.19, 0.81); the decay rate is
   invariant. "Which erodes first" is measure-dependent: at γ=0.1 — amplitude
   −36%, 1/e scale −45%, single-symbol I −47%, information rate −20% (agent
   check: I_rate(A;Y)/T = H_∞ − h(γ) = 0.0647 vs A's rate 0.0808 = 80%
   retained, matching Claude's "80% of A's"). What survives — and is stronger:
   **the substrate's time is hidden, not destroyed** (Y is a hidden-Markov
   process; the rate is recoverable by a filter).
4. **13/13 PASS = verification, not evidence.** The simulation verifies the
   implementation against the closed forms; the claim enters as an assumption.
   Fix: one-pager wording ("verification tests", not "evidence for the claim").

**Conceptual corrections adopted:**

- **Single-knob artifact:** for a BSC, γ>0.5 is anticorrelation, not more
  disconnection (I(γ) = I(1−γ)); the U-shapes are partly built into the
  parameterization. The honest object is the 2-D phase space (γ = noise ∈
  [0,½], M = remapping), B = M(A) ⊕ E_γ; "stable alien world" = (γ≈0, M≠I).
  Queued as the next toy (§7.4).
- **"Indistinguishable from sobriety" is by construction:** I, ρ, H, zlib are
  all invariant under symbol relabeling, so the finding is that the four
  standard measures are BLIND to representation — **alienness = a fourth
  quantity** (the reviewers independently converged on it: "alienness cannot
  be represented by noise"; "make it one").
- **The substrate sentence:** "the substrate is nearly unchanged" →
  abstraction-level statement (the model is implemented by the substrate
  dynamics; the first-person change is organizational, not of content).
  Legitimate bridge = REBUS (attenuated precision of high-level priors).
  Reviewer note: a 2026 Nat Med study (DOI 10.1038/s41591-026-04287-9,
  reviewer-cited, not independently verified) reports widespread connectivity
  reconfiguration under LSD — the "fixed substrate" phrasing is further
  weakened.
- **Headline changed (reviewer proposal):** "One substrate, many
  representations: a closed-form two-layer model of latent dynamics and
  experienced streams." Main result: identical latent dynamics do not uniquely
  determine observational phenomenology; the interesting work is classifying
  the transformations T by what they preserve (fidelity, temporal structure,
  entropy, compressibility, geometry, self-model stability).
- **Psychedelic-bridge haircut:** speculative mappings demoted to §10
  (candidate interpretations, not derived); the "set/setting is the #1 lever"
  and "microdose ≈ γ 0.05–0.1" claims cut from the one-pager; prior-art
  paragraph added (REBUS 2019, the thalamocortical filter/CSTC line
  (Vollenweider et al.), Huxley's reducing valve as ancestor).

**Claude's smaller points (resolved):** (a) the D_min = log N construction —
the log depth comes from the associative (parallel-prefix) composition of the
Markov transition map: a property of this substrate class, not of "the same
trajectory" in general; stated as limit §6.6 in the one-pager. (b) The
ratchet's `periodic_ss` fix verified IN: the ratchet runs clean (exit 0,
2026-11-21), so README §3a–d is safe to send physics readers to.

**Program level (Claude, adopted into the README next steps):** the
**two-qubit no-signaling check** as the program's next step — take
P_i' ∝ P_i·exp(εF_i), define F by downstream consequences, put it on an
entangled two-qubit system, and test whether the reweighting leaks signal
across a causal cut. If it leaks for every F of that shape → a no-go result
for the whole class (fits the seed's "success even if ε = 0"); if some F
survives → the first sign the idea is more than a template. Bounded, cheap,
and it targets the question most likely to KILL the hypothesis — so it runs
BEFORE more classical toys (every toy so far is classical and cannot touch
that question). Claude also expects ε = 0 or an inconsistency ("nearly every
positive-looking result turned out to be a bug, a symmetry artifact, or a
tautology once checked — that's the process working, not a failing of the
project") and proposed the claim-status table below. Adopted.

**Claim-status table (adopted as a standing practice; kept current as the
program grows):**

| claim | status |
|---|---|
| A invariant / B freely parameterized (13 rows) | verified (implementation vs closed form) |
| ρ_Y(k) = (1−2γ)²ρ_A^k; decay rate invariant | verified (closed form + measured) |
| 1/e scale 49.5 → 27.4 at γ=0.1; absent for γ∈(0.19, 0.81) | verified (analytic + asserted) |
| H_∞(0.1) = 0.534; H_∞(0.05) = 0.358 | verified (filter; reviewers 0.533/0.536, 0.355) |
| experience tracks B (the claim) | interpretation (stated experience assumption) |
| fork leans D_min (under the experience assumption) | argument (analogical) |
| "time goes first" (old headline) | artifact (1st-order extrapolation) — corrected |
| "indistinguishable from sobriety" (γ=1) | by construction (relabeling invariance) |
| alienness = a fourth quantity | robust (measure blind-spot) |
| bad trip = fluctuating γ | prediction (extension pending) |
| psychedelic mappings (trip-speak) | candidate interpretations (§10) |
| two-qubit no-signaling for the class of F | open (queued, program-level next) |

## 10. Speculative mappings (demoted 2026-11-21 — candidate interpretations, not derived)

Demoted from the one-pager per the round-4 review: fun and useful, but the
model does not derive them and neuroscience does not establish them (HPPD in
particular has heterogeneous symptoms and limited mechanistic evidence per
reviewer-cited reviews):

- **Bad trip = fluctuating γ** (not high stable γ — high *stable* γ is a
  stable, possibly terrifying mirror world; the bad trip oscillates between
  real and alien without resolving; the mind cannot build a model because the
  gate keeps moving). Set/setting = γ-stabilizers. Pending the fluctuating-γ
  extension (§7.1) — that build turns this from prediction into measurement.
- **Flashbacks/HPP = γ stuck half-open** — residual bleed of mirror-world
  structure (the geometrics).
- **Ego death** = self-model dissolution in the high-γ regime; a "lastingly
  changed self" = the *baseline* γ shifted (plasticity); integration =
  re-tuning to the new baseline.
- **MDMA ≈ close the gate + amplify the social channel** — an amplifier of the
  *other-model*, not a destabilizer of the *self-model* (why it is an
  empathogen, not a psychedelic).
- **Gain vs gate:** alcohol = substrate volume down (dull/blur);
  caffeine/amphetamines = up (sharpen) — the mapping is intact; they are not
  on the γ dial at all.
- **Microdose ≈ γ 0.05–0.1** — a positional statement, not a calibration.

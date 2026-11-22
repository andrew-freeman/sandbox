# Psychedelic phenomenology as a diagnostic for the D_causal / D_min fork

**Date:** 2026-11-21
**Status:** argument (§1–4) + 2-layer formalization toy (`toy/dual_field_toy_2layer.py`,
pre-registered closed-form predictions in §5, results in §6).
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
4. **Information retention ≠ perceptual stability**: γ=1 keeps I≈1 (the
   experience carries essentially full information about the substrate) under an
   inverted mapping, with the same persistence and compressibility as γ=0
   (zlib 0.121 at both extremes). A stable-but-alien mirror world is
   information-theoretically indistinguishable from sobriety — "alienness" is
   not captured by I, ρ, H_rate, or compressibility.
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

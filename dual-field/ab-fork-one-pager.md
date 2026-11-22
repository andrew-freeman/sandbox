# One substrate, many realities

**A closed-form demonstration that experience tracks the description layer.**

**What this page is:** a self-contained artifact of the dual-field pressure-test
program (author: Andrey Bushuev; pressure-tested 2026-11-21). No backstory
required — no hypothesis, no prior parameters, no prior reading.
**What it is not:** a new law of physics (the math below is textbook). The *claim*
is the point; the toy is evidence that the claim makes non-trivial,
pre-registered, verified predictions.
**Status:** all predictions pre-registered (stated before the run) and verified —
13/13 PASS, known-limit asserts exact. Reproduce:
`python3 toy/dual_field_toy_2layer.py` (numpy only, < 5 s).

## 1. The question

"Reality" has at least two layers that most discussions silently conflate:

- **Layer A — the causal process:** what physically happened — matter unfolding
  step by step. Ask "how deep is this?" and the honest answer is the number of
  sequential steps actually taken: N.
- **Layer B — the generative description:** the shallowest law/model that could
  reproduce what is experienced. A ten-line law can produce 10^100 events; its
  "depth" is the size of the description, and can be far smaller than N.

The same trajectory has *both* depths, and they differ by N / log N (constructed
and measured in `toy/dual_field_toy_depth4.py`: the sequential realization and the
parallel-prefix realization of the same trajectory are verified identical, both
depths measured). **Which depth "reality" is** is an open choice, and the two
choices give different physics. We call this the **A/B fork**.

## 2. The claim — and its natural demonstration

Psychedelic pharmacology hands the A/B question a free experiment:

- **LSD** (5-HT2A): the entorhinal–hippocampal *disconnection* dissolves —
  stale/random input bleeds into the ongoing model; priors lose grip.
- **Ketamine** (NMDA): thalamocortical sensory gating disrupted — dissociation.

In both, **the substrate (the brain's causal dynamics) is nearly unchanged; what
changes are parameters of the generative model.** And the experienced "reality"
changes accordingly — it tracks the *model* parameters, not the substrate.
Sobriety and the altered state are two "realities" sharing one substrate,
differing in the mapping.

**Claim: reality-as-experienced is a B-object (the generative/description layer),
not an A-object (what happened).**

**Stated assumption (the entire force of the argument):** this diagnoses the fork
*only if* what we care about is *experience* — and "what is reality" is an
experience question. If the question were purely about the substrate, this
demonstration is silent by design.

## 3. The demonstration — two layers, one dial

**Layer A (fixed):** one realized trajectory of a 1st-order Markov chain,
P(stay)=0.99 (persistence ≈ 50 steps). One trajectory, one causal unfolding,
depth N. Identical in every row below (checksum-asserted).

**Layer B (the dial):** a binary symmetric channel (BSC) on A with crossover
γ ∈ [0,1] — the "gate." With probability γ the experienced symbol is replaced by
an independent random bit: uncontrolled input bleeds into the model. A minimal
formalization of entorhinal disconnection.

- γ=0 — perfect copy (sobriety)
- γ=0.5 — maximum disconnection (the experience is white noise)
- γ=1 — exact inversion (a stable, structured, alien world: the mirror)

**Pre-registered predictions** (stated before the run; fair substrate;
h = binary entropy in bits; ρ_A = 2s−1 = 0.98):

| quantity | meaning | closed form | shape |
|---|---|---|---|
| I(A;B) | "how much of A is actually in the experience" | 1 − h(γ) | U-shaped, 0 at γ=0.5 |
| ρ(B) | "how far the experience reaches in time" | ρ_A(1−2γ)² | U-shaped, 0 at γ=0.5 |
| H_rate(B) | "how novel each moment is" | h((1+ρ_A(1−2γ)²)/2) | ∩-shaped, max at γ=0.5 |
| zlib ratio | "predictability of the stream you're living in" | — | ∩-shaped (incompressible at 0.5) |

**Results (2026-11-21, N = 200 000):**

| γ | I_emp / I_theory | ρ_emp / ρ_theory | H_emp / H_theory | zlib | persistence ξ_B |
|---|---|---|---|---|---|
| 0.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.121 | 48.7 |
| 0.10 | 0.5336 / 0.5310 | +0.6293 / +0.6270 | 0.6915 / 0.6941 | 0.665 | 2.2 |
| 0.50 | 0.0000 / 0.0000 | −0.0012 / 0.0000 | 1.0000 / 1.0000 | 1.001 | 0.0 |
| 1.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.121 | 48.7 |

All 13 γ rows PASS (max deviation 0.17 tolerance units); the predicted
γ↔1−γ mirror symmetry holds empirically; the known-limit asserts
(γ=0 → B≡A; γ=1 → B≡¬A) pass exactly. Full table + plots: the toy's output.

## 4. What the demonstration shows — three counterintuitive results

1. **Time goes first, at small γ.** Persistence collapses 48.7 → 2.2 at
   γ=0.1 — long before information is lost (I still 0.53). The substrate's
   long-range temporal structure — the world's narrative connective tissue — is
   the first thing to dissolve. (Trip-speak: microdose "looser time" ≈ LSD's
   eternal now ≈ ketamine's time-stop: the same effect at different γ.)
2. **Information retention ≠ perceptual stability.** At γ=1 the experience
   retains *full* information about the substrate — under an inverted mapping:
   the mirror world compresses exactly like sobriety (zlib 0.121 at both
   extremes). A stable, structured, alien reality is
   information-theoretically indistinguishable from sobriety. "Alienness" is a
   fourth quantity, not captured by I, ρ, H, or compressibility.
3. **The peak is the middle, not the maximum.** Novelty and incompressibility
   peak at γ=0.5; information bottoms out there; **both extremes are stable,
   low-entropy, information-bearing realities.** "More" past the peak does not
   produce more chaos — it produces a *new stable reality*. (Trip-speak: the
   dome/tunnel/cosmic-geometry reports — more ordered, not more chaotic. The
   bad trip is *fluctuating* γ — oscillating between real and alien without
   resolving — not high *stable* γ, which is a stable (possibly terrifying)
   mirror world. Set/setting = γ-stabilizers: the mechanistic reason
   set/setting is the #1 outcome lever, not "take less.")

## 5. The psychedelic hook (one paragraph)

The same brain, one dial, several "realities." γ is the *disconnection gate* —
how much uncontrolled input bleeds into the ongoing model. LSD turns it via
5-HT2A (bleed content: memory/meaning); ketamine via NMDA (bleed content:
sensory/self-model); DMT spikes it in 15–40 minutes. The model's trip-speak
predictions: time-loosening is a small-γ effect; the peak of "everything is new
and meaningful" sits at γ≈0.5 (max novelty, zero fidelity); the deep structures
(dome, tunnel) are the *past-the-peak* regime, where the experience
re-organizes into a new stable reality; the bad trip is a dynamical, not an
amplitudinal, phenomenon; flashbacks/HPP = a gate stuck half-open; ego death =
the self-model dissolving at high γ; a "lastingly changed self" = the
*baseline* γ shifted — and integration is re-tuning to it. MDMA is not on this
dial at all: it closes the gate and amplifies the social channel — an amplifier
of the *other-model*, not a destabilizer of the *self-model* (why it is an
empathogen, not a psychedelic). Alcohol and caffeine turn the substrate's
volume, not the gate.

## 6. Honest limits (read before quoting)

1. **The math is textbook** — a BSC on a Markov chain. A sharp reader will say
   "of course." That's fine: the *claim* (experience is a B-object; the fork
   leans B under the experience assumption) is the point, and the toy is the
   evidence that the claim makes non-trivial, pre-registered, verified
   predictions. Do not oversell the math as new physics.
2. **Single-gate lumping.** Real drugs hit several receptors (LSD:
   5-HT2A/1A/2C, weak D2; ketamine: NMDA + σ1 + Na+); the toy folds them into
   one γ.
3. **γ↔dose is structural, not calibrated.** "Microdose ≈ γ 0.05–0.1" is a
   positional statement, not a measurement.
4. **The γ=1 "inversion" is a minimal stand-in for "reorganization."** The dome
   is not a literal bit flip; the structural claim is "stable + faithful +
   reorganized," and the *content* of the reorganization is out of scope.
5. **The demonstration is silent on the substrate by design.** It shows which
   layer *experience* tracks. It does not answer "why this physics, why a fact
   of the matter at all" — that is the substrate's question, and this page does
   not touch it.
6. **Fluctuating γ is a prediction, not yet a measurement.** "Bad trip =
   fluctuating γ" awaits the extension build (γ(t) as a slow process).

## 7. Positioning (how to use this page)

- **Reach room** (talk / blog / general / consciousness): this page is the
  artifact. §1 (the fork) → §3 (the demonstration) → §4 (the three results) →
  §5 (the hook).
- **Physics room:** use this page as the opener ("what is this even about, and
  why should I care"), then bring the falsifiable numbers of the ε-program —
  reversibility resonance, TUR-consistent efficiency↔information trade, chiral
  reciprocity (`README.md` §3a–d).
- **The fork is still open.** This page adds a B-leaning argument under the
  stated experience assumption; it does not settle the fork.

## 8. Reproduce and go deeper

- `toy/dual_field_toy_2layer.py` — the demonstration (numpy only, < 5 s;
  13/13 PASS; exact asserts; 4 ASCII plots).
- `psychedelic-ab-fork-note.md` — the full argument: pre-registered predictions,
  all 13 rows, the free-parameter rhyme, the S/D note, open extensions.
- `README.md` — the full program: the hypothesis, the ε-program results, the
  depth rounds, the S/R/K/D taxonomy.
- `toy/dual_field_toy_depth4.py` — the A≡B construction that makes the fork
  concrete: same trajectory, D_causal = N measured and D_min = log2 N measured.

# One substrate, many representations

**A closed-form two-layer model of latent dynamics and experienced streams.**

**What this page is:** a self-contained artifact of the dual-field pressure-test
program (author: Andrey Bushuev; built 2026-11-21; **round-4 external review
applied the same day** — two independent reviewers, every numerical claim
re-verified by the agent before integration; the review and the claim-status
table are in `psychedelic-ab-fork-note.md` §9). No backstory required — no
hypothesis, no prior parameters, no prior reading.
**What it is not:** a new law of physics (the math below is textbook —
deliberately: the *claim* is the point, and the toy is evidence that the claim
makes non-trivial, pre-registered predictions. The 13/13 below are
**verification tests** — implementation vs closed form — not experimental
evidence for the claim.)
**Main result:** **identical latent dynamics do not uniquely determine
observational phenomenology.** B = T(A); properties of B depend strongly on T.
The interesting work is classifying transformations T by what they preserve:
fidelity, temporal structure, entropy, compressibility, geometry,
self-model stability.
**Status:** all pre-registered predictions verified (13/13, exact known-limit
asserts). Reproduce: `python3 toy/dual_field_toy_2layer.py` (numpy only, < 10 s).

## 1. The question

"Reality" has at least two layers that most discussions silently conflate:

- **Layer A — the causal process:** what physically happened — matter unfolding
  step by step. Ask "how deep is this?" and the honest answer is the number of
  sequential steps actually taken: N.
- **Layer B — the generative description:** the shallowest law/model that could
  reproduce what is experienced. A ten-line law can produce 10^100 events; its
  "depth" is the size of the description, and can be far smaller than N.

The same trajectory has *both* depths, and they differ by N / log N (constructed
and measured in `toy/dual_field_toy_depth4.py`: the sequential realization and
the parallel-prefix realization of the same trajectory are verified identical,
both depths measured — with the generality caveat in §6.6). **Which depth
"reality" is** is an open choice, and the two choices give different physics.
We call this the **A/B fork**.

## 2. The claim — and its natural demonstration

Psychedelic pharmacology hands the A/B question a free experiment:

- **LSD** (5-HT2A): the entorhinal–hippocampal *disconnection* dissolves —
  stale/random input bleeds into the ongoing model; REBUS: the precision of
  high-level priors attenuates, top-down grip loosens.
- **Ketamine** (NMDA): thalamocortical sensory gating disrupted — dissociation.

**The honest version (round-4):** in a physical brain the generative model is
implemented *by* the substrate dynamics — the drug changes A physically (recent
human imaging shows widespread connectivity reconfiguration under LSD, not a
clean isolated gate). The claim is therefore made at the level of *abstraction*:
from the first-person vantage, the **content** of the experienced world stays
constant (objects, people, layout) while its **organization** changes (meaning,
narrative, reality-feel) — the first-person change is organizational, not of
content, and it tracks *model-level* parameters (precision, gating).

**Claim: reality-as-experienced is a B-object (the generative/description
layer), not an A-object (what happened)** — an interpretation of the
construction below, not a theorem of it; the toy demonstrates the structure
(free parameter between substrate and experience) and which layer experience
tracks.

**Stated assumption (the entire force of the argument):** this diagnoses the
fork *only if* what we care about is *experience* — and "what is reality" is an
experience question. If the question were purely about the substrate, this
demonstration is silent by design.

**Prior art (read before calling it new):** REBUS (Carhart-Harris & Friston
2019 — attenuated prior precision under 5-HT2A), the older thalamocortical
filter / CSTC line (Vollenweider et al.), with Huxley's "reducing valve" as
ancestor. New here is the **A/B depth fork** + the closed-form demonstration,
not the "psychedelics alter predictive processing" story.

## 3. The demonstration — two layers, one dial

**Layer A (fixed):** one realized trajectory of a 1st-order Markov chain,
P(stay)=0.99 (1/e memory scale ≈ 50 steps). One trajectory, one causal
unfolding, depth N. Identical in every row below (checksum-asserted).

**Layer B (the dial):** a **bit-flip channel (BSC) with crossover γ** — with
probability γ the symbol is flipped (B = A ⊕ E, E i.i.d. Bernoulli(γ)).
(Round-4 fix: the original wording said "replaced by an independent random bit"
— that mechanism has effective crossover **γ/2** and never reaches the mirror.
The toy implements the flip; the closed forms below are for the flip channel.)

- γ=0 — perfect copy (sobriety)
- γ=0.5 — maximum disconnection (the experience is white noise)
- γ=1 — exact inversion (a stable, structured, alien world: the mirror)

**Scope note (round-4):** for a BSC, γ>0.5 is *not* "more disconnection" —
I(γ) = I(1−γ); γ=1 is perfect transmission followed by a *known* inversion.
The U-shapes are built into the single-knob parameterization. The honest phase
space is 2-D: **γ = noise/disconnection ∈ [0, ½]** and **M = remapping**
(deterministic transform of A), with B = M(A) ⊕ E_γ. The "stable alien world"
then has an honest location: **(γ≈0, M≠I)** — high fidelity, high stability,
radically transformed mapping. The 1-D BSC is the slice M ∈ {identity,
inversion}; the 2-knob version is the next build (note §7).

**Pre-registered predictions** (stated before the run; fair substrate;
h = binary entropy in bits; ρ_A = 2s−1 = 0.98):

| quantity | meaning | closed form | shape |
|---|---|---|---|
| I(A;B) | fidelity: "how much of A is actually in the experience" | 1 − h(γ) | U-shaped, 0 at γ=0.5 |
| ρ_B(k) | experienced correlation at lag k | ρ_A^k (1−2γ)² (k≥1) | amplitude ×(1−2γ)²; **decay rate invariant** |
| H_1(B) = H(B_t\|B_{t−1}) | 1-step conditional entropy ("surprise per moment") | h((1+ρ_A(1−2γ)²)/2) | ∩-shaped, max at γ=0.5 |
| H_∞(B) | **true entropy rate** of the hidden-Markov process B (Bayes filter) | none — measured | ∩-shaped; limits + symmetry asserted |
| zlib ratio | "predictability of the stream you're living in" | — | ∩-shaped (incompressible at 0.5) |

(Round-4 fix: H_∞ ≠ H_1 — B is a *hidden-Markov* process, not 1st-order
Markov, so H_∞ = E[h(q_t)] via the Bayes filter and H_∞ < H_1 for 0<γ<½.
E.g. at γ=0.1: H_∞ = 0.534 vs H_1 = 0.694. The ∩-shape survives; the
magnitudes of the old table were the H_1 values.)

**Results (2026-11-21 round-4 re-run, N = 200 000):**

| γ | I_emp / I_th | ρ_emp / ρ_th | H_1_emp / H_1_th | H_∞ (filter) | zlib | 1/e scale ξ̂ |
|---|---|---|---|---|---|---|
| 0.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.0808 | 0.121 | 48.7 |
| 0.10 | 0.5336 / 0.5310 | +0.6293 / +0.6270 | 0.6915 / 0.6941 | 0.5338 | 0.665 | 27.0 |
| 0.50 | 0.0000 / 0.0000 | −0.0012 / 0.0000 | 1.0000 / 1.0000 | 1.0000 | 1.001 | — |
| 1.00 | 0.9990 / 1.0000 | +0.9797 / +0.9797 | 0.0818 / 0.0818 | 0.0808 | 0.121 | 48.7 |

All 13 γ rows PASS (max deviation 0.17 tolerance units); H_∞ limits
(0.0808 / 1 / 0.0808) and γ↔1−γ symmetry asserted; the amplitude tell
(C_B(k)/C_A(k) = (1−2γ)² flat at lags 1–40) asserted; known-limit asserts
(γ=0 → B≡A; γ=1 → B≡¬A) exact. Full table + 5 plots: the toy's output.

## 4. What the demonstration shows — three findings

1. **Time: amplitude, not rate.** (The round-4-corrected finding; the old
   "persistence collapses 48.7 → 2.2" headline was an artifact of treating the
   hidden-Markov process B as if it were 1st-order Markov.) The experienced
   correlation **amplitude** is scaled by (1−2γ)²: −36% at γ=0.1; the 1/e
   memory scale runs 48.7 → 27.0 at γ=0.1 and is **absent for the whole middle
   band γ ∈ (0.19, 0.81)**; the long-lag **decay rate is unchanged** (the
   amplitude tell). The substrate's time is **hidden, not destroyed** — B is a
   hidden-Markov process and a Bayes filter recovers the rate from B alone.
   And "what erodes first, time or information?" is measure-dependent and
   comparable, not a robust ordering — at γ=0.1: amplitude −36%, 1/e scale
   −45%, single-symbol I −47%, information rate −20% (80% of A's rate retained).
2. **Information retention ≠ perceptual stability — by construction, which is
   the point.** I, ρ, H_1 and zlib are all invariant under symbol relabeling,
   so the mirror at γ=1 is indistinguishable from sobriety *by these measures,
   by design*. The finding: **the four standard measures are blind to
   representation** — "alienness" is a fourth quantity that noise (any γ)
   cannot represent and that γ=1 is noise-free yet alien.
3. **The peak is the middle, not the maximum** (within the M ∈ {I, ¬} slice).
   Novelty (H_1, H_∞, zlib) peaks at γ=0.5; information bottoms out there;
   both extremes are stable, low-entropy, information-bearing. In the 2-D
   phase space, "more past the peak" = a *new stable remapping M*, not more
   noise — the structural signature of the deep-structure reports (dome,
   tunnel, cosmic geometry): more ordered, not more chaotic.

## 5. The psychedelic hook (one paragraph)

The same brain, one dial, several "realities." γ is the *disconnection gate* —
how much uncontrolled input bleeds into the ongoing model. LSD turns it via
5-HT2A (bleed content: memory/meaning; REBUS: prior precision attenuates);
ketamine via NMDA (bleed content: sensory/self-model); DMT spikes it in
15–40 minutes — a fast sweep through the axis. The model's trip-speak
predictions: time-loosening and the dissolution of the experienced 1/e memory
scale are small-to-moderate-γ effects (the experienced stream loses its
observable long-range structure while the substrate's stays recoverable); the
peak of "everything is new and meaningful" sits at mid-γ (max novelty, zero
fidelity); the deep structures are the *past-the-peak* regime, where the
experience re-organizes into a new stable reality (a new M, in the 2-D
phase space) — more ordered, not more chaotic. MDMA is not on this dial at
all: it amplifies the *other-model* (the social channel) rather than
destabilizing the self-model — why it is an empathogen, not a psychedelic.
Alcohol and caffeine turn the substrate's volume, not the gate. The
speculative mappings (bad trip = fluctuating γ, HPPD, ego death, set/setting)
live in the note under *Speculative mappings* (note §10) — candidate
interpretations, not derived.

## 6. Honest limits (read before quoting)

1. **The math is textbook** — a BSC on a Markov chain. A sharp reader will say
   "of course." That's fine: the *claim* (experience is a B-object; the fork
   leans B under the experience assumption) is the point, and the toy is the
   evidence that the claim makes non-trivial, pre-registered, verified
   predictions. The 13/13 are **verification of the implementation against the
   closed forms**, not evidence for the claim.
2. **Single-knob artifact (round-4):** γ>0.5 = anticorrelation, not
   disconnection; the U-shapes are partly built into the parameterization. The
   honest object is the 2-D (γ, M) phase space — the next build.
3. **Single-gate lumping.** Real drugs hit several receptors (LSD:
   5-HT2A/1A/2C, weak D2; ketamine: NMDA + σ1 + Na+); the toy folds them into
   one γ. And the neural substrate is *not* literally fixed under the drug —
   the claim is an abstraction-level statement (§2).
4. **γ↔dose is structural, not calibrated.** "Microdose ≈ γ 0.05–0.1" is a
   positional statement, not a measurement (demoted to speculative).
5. **The γ=1 "inversion" is a minimal stand-in for "reorganization."** The
   dome is not a literal bit flip; the structural claim is "stable + faithful +
   reorganized," and the *content* of the reorganization is out of scope.
6. **The fork's generality caveat:** the D_min = log N construction rests on
   the parallel-prefix composition of the Markov transition map (associative
   composition) — a property of this substrate class, not of "the same
   trajectory" in general; the fork hinges on exactly that.
7. **The demonstration is silent on the substrate by design.** It shows which
   layer *experience* tracks. It does not answer "why this physics, why a fact
   of the matter at all."
8. **Fluctuating γ is a prediction, not yet a measurement.** "Bad trip =
   fluctuating γ" awaits the extension build (γ(t) as a slow process).
9. **Citation provenance:** REBUS (2019) and the thalamic-filter line are
   background knowledge confirmed by the reviewers (who could not open the
   abstracts from their environment); the 2026 Nat Med LSD-connectivity study
   is reviewer-cited (DOI in note §9), not independently verified.

## 7. Positioning (how to use this page)

- **Reach room** (talk / blog / general / consciousness): this page is the
  artifact. §1 (the fork) → §3 (the demonstration) → §4 (the three findings) →
  §5 (the hook).
- **Physics room:** use this page as the opener ("what is this even about, and
  why should I care"), then bring the falsifiable numbers of the ε-program —
  reversibility resonance, TUR-consistent efficiency↔information trade, chiral
  reciprocity (`README.md` §3a–d; the ratchet was verified runnable
  2026-11-21).
- **The fork is still open.** This page adds a B-leaning argument under the
  stated experience assumption; it does not settle the fork. The claim-status
  table (verified / artifact / tautology / interpretation / prediction) is in
  note §9.

## 8. Reproduce and go deeper

- `toy/dual_field_toy_2layer.py` — the demonstration (numpy only, < 10 s;
  13/13 PASS; exact asserts; H_∞ Bayes-filter column; 5 ASCII plots).
- `psychedelic-ab-fork-note.md` — the full argument + **§9 round-4 review**
  (the two external reviews, the re-verified corrections, the claim-status
  table) + §10 speculative mappings.
- `README.md` — the full program: the hypothesis, the ε-program results, the
  depth rounds, the S/R/K/D taxonomy.
- `toy/dual_field_toy_depth4.py` — the A≡B construction that makes the fork
  concrete: same trajectory, D_causal = N measured and D_min = log2 N measured.

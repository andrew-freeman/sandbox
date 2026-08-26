Yes. I ran both extracted scripts against the existing `dual_field_toy.py`. They execute cleanly and reproduce exactly the intended numerical behavior. But I would **not merge the present interpretation into the theory yet**. There are two important conceptual errors, one implementation mismatch, and one genuinely useful discovery hiding underneath them.

The strongest result is actually that the attempt has separated several things we had been conflating.

### 1. `depth2` does **not** measure computational depth

This is the biggest issue.

The script defines “depth” as the autocorrelation decay length

$$
C(k)=(2s-1)^k,
$$

so analytically

$$
\xi=-\frac{1}{\ln|2s-1|}.
$$

Your numerical values are right: as \(s\rightarrow1\), entropy rate falls while \(\xi\) grows. The code explicitly interprets this as long causal depth and then concludes that the quantity is global and cannot be captured by local Markov dynamics. 

But here is the problem:

$$
P(x_t|x_{t-1},x_{t-2},\ldots)=P(x_t|x_{t-1}).
$$

It is a **first-order Markov chain**.

The arbitrarily long autocorrelation is generated completely by one local number, \(s\). The distant past remains statistically correlated with the present because the influence propagates through many successive local transitions—not because the transition law needs access to the distant past.

So this conclusion in the script:

> long-range depth ⇒ GLOBAL ⇒ NOT localizable

doesn't follow. 

What you have demonstrated is instead:

$$
\boxed{\text{surprisal} \neq \text{persistence/correlation time}}
$$

which is useful, but weaker.

In fact, the phrase “independent axes” is also too strong. In this particular one-parameter family,

$$
H=h_2(1-s)
$$

and

$$
\xi=-1/\ln(2s-1),
$$

so \(H\) and \(\xi\) are both deterministic functions of the same \(s\). They run in opposite directions, but they are **not independent**.

A better second toy would use a two-parameter asymmetric Markov chain so you can hold entropy rate approximately fixed while changing correlation length, and vice versa.

---

### 2. More seriously: surprisal is not computational difficulty

The first script uses

$$
-\log P(x_t|x_{t-1},x_{t-2})
$$

as the “local computational difficulty.” 

That is **surprisal/code length**, not computation time.

Generating a rare random bit isn't computationally harder than generating a likely random bit.

For instance, a physical RNG producing

```text
011011001...
```

may have huge surprisal but trivial computational generation cost: sample once per bit.

Conversely, something generated deterministically by a tiny program after \(10^{15}\) sequential operations has essentially zero entropy rate but potentially enormous computational depth.

So I think `depth2` accidentally discovered precisely why the first proposed replacement doesn't work.

Your own two scripts actually contradict each other here:

`depth.py` concludes:

> “per-step surprise is exactly that surrogate [for depth]” 

while `depth2.py` concludes:

> low surprise can coexist with high “depth.” 

I think **the second intuition is closer to what we actually want**, although autocorrelation length still isn't the right depth.

---

### 3. There is also an actual implementation mismatch in `depth.py`

This one is worth fixing immediately.

You define:

```python
def nll(traj):
    ...
    t += -np.log(p)
```

which really does compute total surprisal. 

But in the section that claims to test the *local surprise-weighted dynamics*, you never use `nll()`.

Instead you call:

```python
m2.steady(eps)
m2.pop1(eps)
```



And `dual_field_toy.py` uses your previous **excess predictive information**

$$
I=\log\frac{P_{\rm phys}(y|a,b)}
{P_{\rm null}(y|b)},
$$

not

$$
I=-\log P_{\rm phys}(y|a,b).
$$

There's a very easy diagnostic.

If you literally implement the claimed surprise weighting,

$$
P_\epsilon(y|s)
\propto
P(y|s)e^{\epsilon[-\ln P(y|s)]},
$$

then

$$
P_\epsilon(y|s)\propto P(y|s)^{1-\epsilon}.
$$

At

$$
\epsilon=1,
$$

every possible binary outcome gets weight \(1\):

$$
P_{\epsilon=1}(0|s)
=
P_{\epsilon=1}(1|s)
=
\frac12.
$$

But your current run at \(\epsilon=1\) gives the old EPI model's stationary population,

$$
P(x=1)=0.3590,
$$

which immediately proves that section isn't actually executing the equation printed above it.

So that needs to be separated into two experiments.

---

### 4. The ESS catastrophe is real; its explanation is not

Your result is quite clear:

$$
\mathrm{ESS}/N
$$

collapses badly as trajectory length and \(\epsilon\) grow. I reproduced:

$$
\begin{array}{c|ccc}
L & \epsilon=.1 & .5 & 1.0\\
\hline
200 & .800 & .058 & .0032\\
2000& .410& .0026& .0008
\end{array}
$$

That's real.

But this statement is too strong:

> compressed length is non-additive ⇒ no local transition rule ⇒ you MUST importance-reweight. 

Naive exponential importance sampling can suffer an ESS catastrophe for **additive extensive observables too**. If

$$
A_T=\sum_t a_t
$$

has variance growing roughly as \(T\), then

$$
e^{\epsilon A_T}
$$

becomes increasingly concentrated on rare trajectories.

So the catastrophe is fundamentally a **measure-overlap problem**, not a consequence of non-additivity.

Additivity is valuable because it often gives you tilted operators and efficient driven-process constructions. But it isn't what prevents importance-sampling collapse.

---

### 5. And I'd stop calling simple row normalization a Doob transform

You currently write approximately

$$
P_{\rm DF}(y|x)
\propto
P(y|x)e^{\epsilon a(x,y)}
$$

and call that the Doob solution.

That's a perfectly legitimate **locally normalized exponential tilt**.

But the genuine driven process corresponding to an exponentially tilted long-time trajectory ensemble generally contains an additional dominant-eigenvector factor:

$$
W_\epsilon(x,y)
\propto
W(x,y)e^{\epsilon a(x,y)}
\frac{r_\epsilon(y)}{r_\epsilon(x)}.
$$

That eigenfunction/eigenvector correction is central to the generalized Doob construction. ([arXiv][1])

So I'd reserve “Doob transform” for the moment when we actually solve the tilted operator.

That will matter a lot if you implement cloning/population dynamics.

---

## But something rather good fell out of this failure

We now have at least four genuinely different candidates that shouldn't be called by the same symbol:

$$
\boxed{
\begin{array}{rcl}
S &:& \text{surprisal / entropy rate}\\
R &:& \text{persistence / correlation time}\\
K &:& \text{description length}\\
D &:& \text{computational depth}
\end{array}}
$$

And **\(D\)** is probably the one our simulation intuition was actually pointing toward.

There is an existing mathematical notion remarkably close to what we independently described: Bennett's **logical depth**. Informally, it measures how much computation is required to generate an object from a near-minimal description, rather than merely asking how short that description is. Bennett introduced it specifically to distinguish things possessing a long nontrivial causal history from both trivial ordered objects and random noise. ([IBM Research][2])

Notice the lovely classification:

$$
\begin{array}{c|cc}
 & K & D\\
\hline
\text{crystal} & low & low\\
\text{random noise} & high & low\\
\text{evolved structured object} & ? & potentially\ high
\end{array}
$$

That's almost exactly the distinction we were reaching for.

And this isn't me saying “therefore use Bennett's definition.” I would treat this as **collision testing after our independent derivation**. It tells us our intuition landed in a nontrivial existing neighborhood.

---

### What I would do with these files

I wouldn't delete either one.

I'd rename them conceptually:

```text
dual_field_toy_depth.py
    → compression_reweighting.py

dual_field_toy_depth2.py
    → surprise_vs_persistence.py
```

because those are experiments they genuinely perform.

And then I'd make a new `depth3` whose question is much stricter:

$$
\boxed{
\text{Can two processes have matched ordinary statistics but radically different}
\\
\text{irreducible sequential generation cost?}
}
$$

The candidate quantity I'd now try is something like

$$
D_G(H|B)
=
\min_{\mathcal C}
\left[
\operatorname{depth}(\mathcal C)
\right],
$$

where \(\mathcal C\) must generate history \(H\) from boundary data \(B\), using only a specified set \(G\) of physically allowed **local gates/interactions**.

That fixes part of the “whose computer?” problem from our simulation hypothesis:

**the universe itself supplies the instruction set.**

Then random noise can be shallow, crystals can be shallow, while a compactly specified process requiring a long irreducible causal unfolding can be deep.

So my verdict is:

$$
\boxed{\text{the current conclusion is wrong, but the experiment was productive.}}
$$

`depth2` hasn't shown that computational depth is global.

It has shown that **surprise, short-range conditional memory, and temporal persistence are different things**.

And that pushes us toward a considerably sharper candidate for \(\mathcal I\):

$$
\boxed{\mathcal I\;\stackrel{?}{=}\;\text{intrinsic physical computational depth}}
$$

which is much closer to the terrible idea we were actually trying to test. 😄

[1]: https://arxiv.org/html/1405.5157v3?utm_source=chatgpt.com "Nonequilibrium Markov processes conditioned on large deviations"
[2]: https://research.ibm.com/publications/on-the-nature-and-origin-of-complexity-in-discrete-homogeneous-locally-interacting-systems?utm_source=chatgpt.com "On the nature and origin of complexity in discrete, homogeneous, locally-interacting systems for Foundations of Physics - IBM Research"


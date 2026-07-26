import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Softmax as linear attention: an evidence-first tutorial

    | Exact paper claim | Current evidence | Verdict |
    |---|---|---|
    | Proposition 3.1 concentration bound | At `L=1`, exact error `1` exceeds stated bound `0` | **FALSIFIED** |
    | Proposition 3.4 gradient bounds | Both exact gradient errors `1` exceed stated bounds `0` | **FALSIFIED** |
    | Lemma 2.1 Gaussian affine identity | Dimension-free Gaussian MGF proof | **VERIFIED** |
    | Theorem 4.3 risk transfer | Arbitrary-ε proof plus monotonicity | **VERIFIED** |
    | Theorem 5.1 Bayes-optimal training | Direct balanced-flow proof covers every positive-definite covariance and every published initialization | **VERIFIED** |

    These are the already-produced formal results from the cumulative
    20-test CPU run. This notebook is explanatory: no expensive experiment
    is required to see or understand them.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The central idea

    Infinite-prompt attention averages over a probability measure:

    \[
    T(z)=\frac{\mathbb E[VX\exp(a^\top X)]}
                {\mathbb E[\exp(a^\top X)]},
    \qquad a=K^\top Qz.
    \]

    If \(X\sim\mathcal N(m,\Gamma)\), its exponential normalizer is

    \[
    F(a)=\exp(a^\top m+\tfrac12a^\top\Gamma a).
    \]

    Differentiating \(F\) gives the tilted first moment. Cancelling the
    common normalizer proves, in every dimension and even for singular
    covariance,

    \[
    T(z)=Vm+V\Gamma K^\top Qz.
    \]
    """)
    return


@app.cell
def _(mo):
    score = mo.ui.slider(-3.0, 3.0, step=0.1, value=1.2, label="score a")
    mean = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.4, label="Gaussian mean m")
    variance = mo.ui.slider(0.0, 3.0, step=0.1, value=1.3, label="variance Γ")
    mo.hstack([score, mean, variance], justify="space-around")
    return mean, score, variance


@app.cell
def _(mean, mo, score, variance):
    affine_output = mean.value + variance.value * score.value
    mo.md(
        rf"""
        For the scalar Gaussian selected above, the exact tilted-attention
        output is

        \[
        m+\Gamma a={mean.value:.1f}+{variance.value:.1f}\times
        {score.value:.1f}=\mathbf{{{affine_output:.3f}}}.
        \]

        This slider evaluates the proved closed form. It is not used as formal
        reproduction evidence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why two propositions are falsified literally

    Both published concentration displays contain `ln(L)` and state no
    `L≥2` or sufficiently-large-`L` qualifier. At `L=1`, their right sides
    are exactly zero.

    Choose one-dimensional standard Gaussian prompts. With `K=0`, a
    one-token softmax output is just that token, so its squared population
    error is `E[X²]=1`. At `U=0,V=1`, the two gradient errors in Proposition
    3.4 are also exactly one. All nine of its moment assumptions reduce to
    products of the finite Gaussian moments `1,3,105`.

    One valid witness resolves a universal statement, regardless of its
    dimension. If the intended theorem had said `L≥2`, however, this
    boundary certificate would not address the repaired statement.
    """)
    return


@app.cell
def _(mo):
    epsilon = mo.ui.number(start=0.01, stop=2.0, step=0.01, value=0.2, label="ε")
    epsilon
    return (epsilon,)


@app.cell
def _(epsilon, mo):
    half = epsilon.value / 2
    mo.md(
        rf"""
        ## Theorem 4.3 in one budget

        For \(\epsilon={epsilon.value:.2f}\), allocate
        \(\epsilon/2={half:.2f}\) to the infinite-flow tail and
        \(\epsilon/2={half:.2f}\) to the finite/infinite comparison at a fixed
        time. Their exact total is \(\epsilon={epsilon.value:.2f}\).

        Gradient-flow risk then cannot increase:
        \(dR_L/dt=-\|\nabla R_L\|^2\leq0\). That final monotonicity step is
        essential; the negative control removes it and is rejected.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## How Theorem 5.1 is closed

    The advertised endpoint matrices predict \(w^\top x\) exactly for
    every invertible anisotropic covariance, so their squared risk is
    exactly zero. The new certificate also proves that the balanced
    population gradient flow reaches that endpoint.

    Writing its matrix and scalar blocks as \(A,b\), the exact risk is

    \[
    R(A,b)=\tfrac12\operatorname{tr}
      ((b\Sigma A-I)\Sigma(b\Sigma A-I)^\top).
    \]

    The flow preserves \(\|A\|_F^2-b^2=0\). Its only balanced stationary
    possibilities are the origin and \(bA\Sigma=I\). Positive diagonal
    entries from \(A(0)=\alpha\Theta\Theta^\top\), together with a trace
    inequality near the origin, exclude convergence to zero. Balancedness
    then fixes the unique zero-risk limit. This holds for every
    \(\alpha>0\), stronger than the paper's interval.

    For general covariance scale, query normalization and the conditional
    envelope
    \(\sigma_w^2=\max(1,\|\Sigma\|_{\rm op}(1+\|w\|^2))\)
    show that the finite/infinite concentration estimates still vanish;
    scale changes constants only.

    [Read the complete report](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/blob/master/reports/claim-by-claim/report.md)
    or inspect the executable evidence in
    [`space_candidate/evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/master/space_candidate/evidence).
    """)
    return


if __name__ == "__main__":
    app.run()

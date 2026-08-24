"""Portfolio tr(P_C . Sigma) consumer-relativity -- the finance twin of the
turboquant KV-keys finding.

The risk an investor feels is w' Sigma w = tr(w w' Sigma) = tr(P_C . Sigma),
with P_C = w w' the portfolio read operator and Sigma the return covariance --
the SAME functional the OT program runs on. A risk model that is optimal in
RECONSTRUCTION (a top-r PCA of Sigma capturing ~99% of market variance) can still
false-clear at the consumer, because the consumer reads a direction the model
dropped: tr(P_C . Sigma_r) << tr(P_C . Sigma).

The adversary needs no construction. Minimum-variance optimization *under the
truncated model*, w = (Sigma_r + eps I)^{-1} 1 (normalized), naturally loads onto
the model's small-eigenvalue / null directions -- the classic "min-variance loads
on estimation error." The model rates this book near-riskless; its realized
volatility (the witness -- Monte-Carlo returns ~ N(0, Sigma)) is far larger, so
its model-VaR breaches at a rate far above nominal. A consumer-aware VaR (full
Sigma) holds at nominal.

    python quant_portfolio.py    # prints the paradox + self-checks
"""
import numpy as np

RNG = np.random.default_rng(20260823)
N, K = 60, 6                    # assets, latent factors
Z99 = 2.3263                    # 99% one-sided normal quantile
NOMINAL = 0.01                  # a 99% VaR should breach ~1% of the time
N_MC = 400_000
EPS_FRAC = 1e-3                 # min-var regularization (fraction of mean eigenvalue)


def factor_cov():
    B = RNG.normal(0, 1.0, (N, K)) * np.array([2.5, 1.8, 1.3, 0.9, 0.6, 0.4])  # factor scale
    D = np.diag(RNG.uniform(0.2, 0.6, N) ** 2)                                  # idiosyncratic
    return B @ B.T + D


def truncate(Sigma, target=0.99):
    vals, vecs = np.linalg.eigh(Sigma)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    cum = np.cumsum(vals) / vals.sum()
    r = int(np.searchsorted(cum, target) + 1)
    Sigma_r = (vecs[:, :r] * vals[:r]) @ vecs[:, :r].T
    return Sigma_r, r, float(cum[r - 1])


def main():
    Sigma = factor_cov()
    Sigma_r, r, explained = truncate(Sigma, 0.99)
    eps = EPS_FRAC * np.trace(Sigma) / N

    # min-variance book UNDER THE MODEL -> loads onto the model's blind spot
    w = np.linalg.solve(Sigma_r + eps * np.eye(N), np.ones(N))
    w /= w.sum()

    model_risk = float(w @ Sigma_r @ w)      # tr(P_C . Sigma_r)
    true_risk = float(w @ Sigma @ w)         # tr(P_C . Sigma)
    model_var = Z99 * np.sqrt(model_risk)
    consumer_var = Z99 * np.sqrt(true_risk)

    # witness: realized P&L over Monte-Carlo returns ~ N(0, Sigma)
    L = np.linalg.cholesky(Sigma)
    pnl = (RNG.standard_normal((N_MC, N)) @ L.T) @ w
    breach_model = float(np.mean(pnl < -model_var))
    breach_consumer = float(np.mean(pnl < -consumer_var))

    print(f"risk model: top-{r} PCA of Sigma, explains {explained:.4%} of market variance")
    print(f"  tr(P_C . Sigma_r) [model]    = {model_risk:.4f}   (VaR99 {model_var:.3f})")
    print(f"  tr(P_C . Sigma)   [consumer] = {true_risk:.4f}   (VaR99 {consumer_var:.3f})")
    print(f"  under-report ratio true/model = {true_risk/model_risk:.1f}x")
    print(f"witness (realized returns, N={N_MC}):")
    print(f"  model-VaR breach rate    = {breach_model:.3%}   (nominal {NOMINAL:.0%}) "
          f"-> FALSE-CLEAR x{breach_model/NOMINAL:.0f}")
    print(f"  consumer-VaR breach rate = {breach_consumer:.3%}   (nominal {NOMINAL:.0%}) -> holds")

    assert explained >= 0.99, "the model must be reconstruction-good"
    assert true_risk / model_risk >= 3.0, "model must materially under-report the book"
    assert breach_model >= 0.05, "model VaR must false-clear (breach >> nominal)"
    assert breach_consumer <= 0.03, "consumer-aware VaR must hold near nominal"
    print("\nPASS: a 99%-variance risk model false-clears at the consumer; "
          "tr(P_C . Sigma) -- the risk the book reads -- is what holds.")


if __name__ == "__main__":
    main()

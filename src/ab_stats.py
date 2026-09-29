"""Small statistics helpers for the Cookie Cats A/B test analysis."""

import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest


def srm_check(counts, expected_ratios=None):
    """Chi-square goodness-of-fit test for sample ratio mismatch.

    counts: observed group sizes, e.g. [44700, 45489].
    expected_ratios: intended split (defaults to equal groups).
    Returns a dict with the chi-square statistic, p-value and expected counts.
    """
    counts = list(counts)
    total = sum(counts)
    if expected_ratios is None:
        expected_ratios = [1 / len(counts)] * len(counts)
    expected = [total * r for r in expected_ratios]
    chi2, p = stats.chisquare(counts, f_exp=expected)
    return {"chi2": chi2, "p_value": p, "expected": expected}


def compare_proportions(successes, totals, alpha=0.05):
    """Two-proportion z-test comparing treatment (index 1) with control (index 0).

    Returns the retention rates, absolute lift (treatment - control), its
    confidence interval, relative lift, z statistic and two-sided p-value.
    """
    s_c, s_t = successes
    n_c, n_t = totals
    p_c, p_t = s_c / n_c, s_t / n_t
    z, p_value = proportions_ztest([s_t, s_c], [n_t, n_c])
    ci_low, ci_high = confint_proportions_2indep(
        s_t, n_t, s_c, n_c, method="wald", compare="diff", alpha=alpha
    )
    return {
        "rate_control": p_c,
        "rate_treatment": p_t,
        "abs_lift": p_t - p_c,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "rel_lift": (p_t - p_c) / p_c,
        "rel_ci_low": ci_low / p_c,
        "rel_ci_high": ci_high / p_c,
        "z": z,
        "p_value": p_value,
    }


def bootstrap_diff(control, treatment, n_boot=10_000, seed=42, alpha=0.05):
    """Bootstrap the difference in means (treatment - control) of two 0/1 arrays.

    Each bootstrap sample redraws every player with replacement within their
    group. For a 0/1 metric the number of retained players in such a resample
    follows Binomial(n, observed rate), so drawing that count directly gives
    exactly the same distribution as resampling rows, just much faster.
    """
    rng = np.random.default_rng(seed)
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    n_c, n_t = len(control), len(treatment)
    boot_c = rng.binomial(n_c, control.mean(), n_boot) / n_c
    boot_t = rng.binomial(n_t, treatment.mean(), n_boot) / n_t
    diffs = boot_t - boot_c
    ci_low, ci_high = np.quantile(diffs, [alpha / 2, 1 - alpha / 2])
    return {"diffs": diffs, "ci_low": ci_low, "ci_high": ci_high}


def minimum_detectable_effect(baseline_rate, n_control, n_treatment, alpha=0.05, power=0.80):
    """Smallest true absolute difference in proportions detectable with the given power.

    Uses the normal approximation for a two-sided two-proportion test:
    MDE = (z_{1-alpha/2} + z_{power}) * sqrt(p(1-p) * (1/n_c + 1/n_t)).
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    se = np.sqrt(baseline_rate * (1 - baseline_rate) * (1 / n_control + 1 / n_treatment))
    return (z_alpha + z_power) * se


def power_for_effect(effect, baseline_rate, n_control, n_treatment, alpha=0.05):
    """Probability of a significant two-sided result if the true absolute difference is `effect`."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    se = np.sqrt(baseline_rate * (1 - baseline_rate) * (1 / n_control + 1 / n_treatment))
    shift = np.abs(effect) / se
    return stats.norm.cdf(shift - z_alpha) + stats.norm.cdf(-shift - z_alpha)

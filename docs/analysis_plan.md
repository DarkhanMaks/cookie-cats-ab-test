# Analysis Plan: Cookie Cats Gate Experiment

*Written and committed before any statistical test was run. Every later decision refers back to this file.*

## Background
In Cookie Cats, players reach a "gate" where they must wait or pay to continue.
Each player was randomly assigned to one of two groups:
- the first gate at level 30 (`gate_30`, the current version = **control**)
- the first gate at level 40 (`gate_40`, the **treatment**)

The data covers 90,189 players ([Kaggle](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats)).

**Business question:** should the first gate move from level 30 to level 40?

## Hypotheses
- **H0:** Retention is the same in both groups (p_gate40 = p_gate30).
- **H1:** Retention differs (p_gate40 ≠ p_gate30). The test is two-sided because moving the gate could plausibly help or hurt.

## Metrics
| Role | Metric | Definition |
|---|---|---|
| Primary | `retention_7` | Player played on day 7 after install |
| Secondary | `retention_1` | Player played on day 1 after install |
| Descriptive only | `sum_gamerounds` | Rounds played in the first 14 days. **Not tested**, because the gate itself affects it (a post-treatment variable) |

Why `retention_7` is primary: the gate sits at level 30–40, which most players reach after day 1, so a long-term effect is where the change should show. Long-term retention is also what drives revenue.

## Statistical approach
- **Significance level:** α = 0.05, two-sided.
- **Multiple testing:** Holm correction across the 2 retention metrics, which keeps the family-wise error rate ≤ 5%.
- **Main test:** two-proportion z-test, with a 95% confidence interval for the difference (gate_40 − gate_30).
- **Effect size:** absolute lift (percentage points) and relative lift (%).
- **Robustness check:** bootstrap of the difference in retention (10,000 resamples, fixed random seed). It should agree with the z-test.
- **Power:** after the main test, compute the minimum detectable effect (MDE) at 80% power for this sample size, to judge how informative the result is.

## Sample ratio mismatch (SRM) check (done first)
- A chi-square goodness-of-fit test compares the group sizes with the intended 50/50 split.
- Threshold: **p < 0.01** means SRM is detected. This is stricter than 0.05 because an SRM check runs on every experiment, and a false alarm would wrongly throw out a valid test.
- **If SRM is detected:** don't interpret the effects as clean causal estimates. Investigate the possible causes that the data allows (duplicate users, differences in player mix between groups, where in the user ID range the imbalance sits) and document what we find. Report any effect estimates as **exploratory**, with the SRM caveat stated next to them.

## Decision rule (primary metric, after Holm correction)
- gate_40 has **significantly higher** retention_7 → recommend moving the gate to 40.
- gate_40 has **significantly lower** retention_7 → keep the gate at 30.
- **Not significant** → keep the gate at 30, since there's no evidence to change. Report the confidence interval and the MDE, and don't claim "no effect".
- retention_1 is supporting evidence only and can't justify a change on its own.
- If SRM is detected, the recommendation is also conditional on fixing and re-running the experiment.

## Data handling
- All 90,189 players stay in the main analysis. That includes the 3,994 players with 0 rounds, because they were randomised too.
- One extreme outlier (49,854 rounds in 14 days, likely a logging error or bot) is kept. Retention is binary, so it counts as one player.
  **Sensitivity check:** rerun the primary test without this player.
- No adjustment for `sum_gamerounds` in the main analysis, because the treatment affects it (see the post-treatment analysis).

## Known limitations (stated in advance)
- Not every player reaches level 30, so many players in both groups never saw a gate. This dilutes any effect.
- There's no install date, country or platform information, so we can't check the balance of pre-treatment characteristics.
- This is one historical experiment, and the results may not generalise to other games or time periods.

# Readout: Should the first gate move from level 30 to level 40?

**For:** Cookie Cats game management
**Recommendation: Keep the gate at level 30.** Before this is treated as final, have the data team check the experiment's assignment and logging pipeline (see Caveats).

## What we tested
90,189 new players were randomly split into two versions of the game. The only difference was where the first gate appears: level 30 (current) or level 40. We compared how many players were still playing 1 day and 7 days after installing. The analysis plan was written and committed before any results were looked at.

## What we found

| | Gate at 30 | Gate at 40 | Difference (95% range) |
|---|---|---|---|
| **Playing on day 7** (main metric) | 19.0% | 18.2% | **−0.8 points** (−1.3 to −0.3) |
| Playing on day 1 | 44.8% | 44.2% | −0.6 points (−1.2 to +0.1), not conclusive |

- **Moving the gate to level 40 lowers 7-day retention.** About 8 fewer players out of every 1,000 are still playing after a week, a 4.3% relative drop. The whole plausible range is below zero, and the result holds after correcting for testing two metrics.
- **Day-1 retention:** the difference is too small to call. That's expected, since most players haven't reached level 30 by day 1.
- The result holds with a second statistical method (bootstrap), with the one extreme outlier removed, and in the same direction when we look only at players who reached the gate.

## Why it matters
Day-7 retention is a leading indicator of long-term players and revenue. Moving the gate later looks like a small, low-risk change, but it would cost retention.

## Caveats
1. **The two groups aren't quite the size they should be.** gate_40 has 789 more players than a 50/50 split explains (p = 0.009). All the extra players are low-engagement players who never reached a gate. We couldn't find the cause in this data. It could be chance, or it could be a tracking issue. Checks that avoid this imbalance point the same way, but the pipeline should be verified.
2. **Small effects could be missed.** The experiment reliably detects day-7 changes of about 0.7 points or more. The effect we found is just above that.
3. **We don't "adjust" for how much people played.** The gate changes how much people play, so that adjustment would give a misleading answer.
4. This is one experiment on one game at one point in time.

## Next steps
- Keep the gate at level 30.
- Ask the data team to audit the assignment and logging for low-engagement players.
- If gate placement stays a priority, a follow-up test of an *earlier* gate could check whether a forced break helps players come back. That's a hypothesis, not something this experiment showed.

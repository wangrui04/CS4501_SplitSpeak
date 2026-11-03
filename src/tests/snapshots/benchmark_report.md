# Benchmark Report

- Model: `claude-sonnet-5-5`
- Provider: `claude`
- Prompt version: `test-1`
- Commit: `abc1234`
- Run at: 2026-11-03T12:00:00+00:00

Run 1 is the **official** run. ⚠ marks a scenario whose result differs across runs.

| Scenario | Run 1 (official) | Run 2 | Run 3 | Behavior (Run 1) |
| --- | --- | --- | --- | --- |
| B1 Basic | ✅ 2 prompts | ✅ 2 prompts | ✅ 2 prompts | ✅ expected asked, asked |
| B2 Moderate | ✅ 2 prompts | ✅ 2 prompts | ✅ 2 prompts | ✅ expected asked, asked |
| B3 Intermediate ⚠ | ❌ 2 prompts, Kayla's share off by $0.01 | ✅ 2 prompts | ✅ 2 prompts | ✅ expected asked, asked |
| B4 Advanced | ✅ 2 prompts | ✅ 2 prompts | ✅ 2 prompts | ✅ expected asked, asked |
| B5 Most complex ⚠ | ✅ 2 prompts | ✅ 2 prompts | ❌ 5 prompts, prompt limit: no final preview within 5 prompts | ✅ expected asked, asked |

## Pass rates

| Run | Passed | Result |
| --- | --- | --- |
| Run 1 (official) | 4/5 (80%) | FAIL |
| Run 2 | 5/5 (100%) | PASS |
| Run 3 | 4/5 (80%) | FAIL |
| Overall | 13/15 (87%) | — |

## Threshold

**FAIL** against the 90% target: Run 1 passed 4/5 (80%).

With 5 scenarios, a single automated run passes 90% only at 5/5 (4/5 is 80%). This report is supporting evidence. The official result is the 15-attempt human session in `docs/alpha-results.md` (3 testers × 5 scenarios, ≥ 14/15 to pass).

## Failures by category

| Category | Failures |
| --- | ---: |
| tax/tip | 1 |
| prompt limit | 1 |

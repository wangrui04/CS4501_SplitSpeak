# Alpha Submission: Checklist and Activities Draft

Due on Canvas **before class on Nov 5**: the Activities Document (PDF), the Presentation Slides (PDF), and the repo link (issue #37).

This file is a working draft. Copy each section into the Activities Document, fill in the blanks, and export to PDF.

---

## 1. Checklist

- [ ] The alpha session is done and recorded in [alpha-results.md](alpha-results.md) (#33).
- [ ] The automated benchmark report is attached as supporting evidence (#32).
- [ ] The Activities Document covers Activities 1–3 (sections 2–4 below), exported to PDF.
- [ ] The slides cover the product, methodology, results, and limitations (section 5), exported to PDF.
- [ ] The README has run instructions and links, and the repo is accessible to the instructors.
- [ ] Every issue is closed or explicitly deferred with a reason (section 6).
- [ ] Every PR links to an issue.
- [ ] A teammate walks this checklist and fresh-clones the repo to confirm the quick start works.
- [ ] Both PDFs and the repo link are submitted on Canvas.

---

## 2. Activity 1: Validation analysis

Copy the numbers and decision from [alpha-results.md](alpha-results.md) §4–5.

- **Hypothesis:** the AI expense assistant produces an accurate split, meaning every share, amount paid, and settlement transfer matches the key, within 5 user prompts in at least 90% of attempts.
- **Method:** 3 internal testers × 5 benchmark scenarios (B1–B5) = 15 attempts. Success requires at least 14 of 15. Prompts are pasted verbatim from [benchmarks.md](benchmarks.md).
- **Result:** _N_ / 15 (_N_%), broken down per scenario.
- **Decision:** _Validated_ / _Invalidated: pivot_, with root cause, fix plan, and retest plan if it failed.
- **Supporting evidence:** automated benchmark Run 1 (official) / Run 2 / Run 3 report.
- **Limitations:** see [alpha-results.md](alpha-results.md) §8.

---

## 3. Activity 2: Stories → issues coverage

| User story | Issues | Status |
| --- | --- | --- |
| US-01 Equal splitting | [#19](https://github.com/wangrui04/CS4501_Splitwise/issues/19), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-02 Selected members | [#20](https://github.com/wangrui04/CS4501_Splitwise/issues/20), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-03 Itemized splitting | [#22](https://github.com/wangrui04/CS4501_Splitwise/issues/22) | _fill in_ |
| US-04 Quantities and tax/tip | [#21](https://github.com/wangrui04/CS4501_Splitwise/issues/21), [#23](https://github.com/wangrui04/CS4501_Splitwise/issues/23) | _fill in_ |
| US-05 Missing / ambiguous info | [#24](https://github.com/wangrui04/CS4501_Splitwise/issues/24), [#30](https://github.com/wangrui04/CS4501_Splitwise/issues/30) | _fill in_ |
| US-06 Messy language and typos | [#25](https://github.com/wangrui04/CS4501_Splitwise/issues/25) | _fill in_ |
| US-07 Manual entry | [#26](https://github.com/wangrui04/CS4501_Splitwise/issues/26), [#27](https://github.com/wangrui04/CS4501_Splitwise/issues/27), [#30](https://github.com/wangrui04/CS4501_Splitwise/issues/30) | _fill in_ |
| US-08 Name-based sign-in | [#9](https://github.com/wangrui04/CS4501_Splitwise/issues/9), [#16](https://github.com/wangrui04/CS4501_Splitwise/issues/16), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-09 Balances and history | [#28](https://github.com/wangrui04/CS4501_Splitwise/issues/28), [#29](https://github.com/wangrui04/CS4501_Splitwise/issues/29) | _fill in_ |
| Benchmarks B1–B5 | [#28](https://github.com/wangrui04/CS4501_Splitwise/issues/28), [#31](https://github.com/wangrui04/CS4501_Splitwise/issues/31), [#32](https://github.com/wangrui04/CS4501_Splitwise/issues/32), [#33](https://github.com/wangrui04/CS4501_Splitwise/issues/33) | _fill in_ |
| Security (all stories) | [#34](https://github.com/wangrui04/CS4501_Splitwise/issues/34) | _fill in_ |
| End-to-end coverage | [#36](https://github.com/wangrui04/CS4501_Splitwise/issues/36) | _fill in_ |

---

## 4. Activity 3: TDD evidence

### Test-first work on `feature/alpha-25-37`

For each issue, tests were written first and run red before the implementation. Each commit then contains the tests together with the code that makes them pass. The exception is #36: the Playwright specs were committed on their own, **before** the features they cover.

| Commit | Issue | Red run before implementation |
| --- | --- | --- |
| `fa7fc81` | Upstream benchmark model | `test_trip_allocation.py` failed at import (`WeightsMismatchError` did not exist) |
| `e82120c` | #28 | `test_settlement.py` chat-preview test failed with `KeyError: 'paid'` |
| `18c3494` | #26 | manual-entry tests written before `backend/manual.py` |
| `b14b5a5` | #34 | security tests written before `backend/security.py` |
| `d0827a0` | #35 | the 2 contradictory "Kayla and I" tests failed; the 10 resolution tests already passed |
| `ed67f52` | #27, #30 | 5 escape-hatch tests failed before the modal changes |
| `94b66e2` | #36 | E2E specs committed before #27, #29, and #30 were implemented |

**Failing CI runs:** _link the first GitHub Actions run for `94b66e2` once the branch is pushed. The E2E job should fail there, because the features land in later commits._

### How AI-generated tests were reviewed and corrected

Examples from this sprint:

1. **Mocked tests hid a broken live path.** The Claude client tests mocked the SDK and checked for a forced `tool_choice`, so they passed while every real request to Sonnet 5.5 would fail (the model rejects forced tool use and `temperature`). The tests were rewritten to assert that those parameters are *not* sent, and the client moved to structured outputs (`24f6281`).
2. **A property test found a real bug.** The Hypothesis test for settlement produced an expense with an empty payments list, and `payments_of()` wrongly treated it as missing. The code was fixed, not the test.
3. **A wrong expectation in a generated test.** A comparator test expected both a share and a settlement mismatch, but its hand-built preview kept the original transfers, so only the share differed. The expectation was corrected, and an assertion on the human-readable reason was added.
4. **A test that encoded the wrong behavior.** The old manual-entry test asserted a payload built with `parseFloat` × 100, and that nothing was saved through the API. It was replaced with tests for the real endpoint and string-based cents conversion.
5. **An answer-key check against itself.** The benchmark keys are typed by hand from `Benchmarks.docx` rather than computed, so `test_answer_key_sanity` can catch typos: shares must equal amounts paid, and the settlement function must reproduce the key's transfers.

---

## 5. Slides outline

1. **Problem:** splitting complicated shared bills is tedious and error-prone.
2. **Product:** Splitwise core plus a conversational assistant that asks before guessing and shows an itemized preview you must confirm.
3. **Architecture:** the LLM only extracts structured JSON; deterministic, unit-tested code does all arithmetic; validation and confirmation gate every save.
4. **Hypothesis and method:** ≥ 90% accurate within 5 prompts; 3 testers × 5 benchmark scenarios.
5. **Results:** per-scenario table, total _N_/15, and the decision.
6. **Supporting evidence:** automated Run 1/2/3 report and test counts.
7. **Limitations:** 3 internal testers, scripted scenarios, LLM variability, and the same team wrote the benchmark and the product.
8. **Next steps:** fixes from failures, external testers, settle up, corrections UI.

---

## 6. Issue status

| Issue | Status | Reason if deferred |
| --- | --- | --- |
| #2, #3 | _open_ | _documentation and professor confirmation; owned by the team_ |
| #4–#24 | _close if done, or defer with a reason_ | |
| #25–#32, #34–#36 | Implemented on `feature/alpha-25-37` | |
| #33 | Pending: needs the human session | |
| #37 | Pending: needs PDFs and Canvas submission | |
| #38 Corrections after a preview | _decide_ | Backend handles corrections (B5); no dedicated UI |
| #39 Itemized manual entry | Deferred | Optional; equal-split manual entry covers US-07 |
| #40 Settle up placeholder | Deferred | Optional; settlement is shown, but recording payments is out of alpha scope |

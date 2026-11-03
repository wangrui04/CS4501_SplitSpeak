# Benchmark Scenarios (B1–B5)

This file is the source of truth for the alpha benchmark. It copies the prompts from the team's `Benchmarks.docx`. The scenario files in [`src/benchmark/scenarios/official/`](../src/benchmark/scenarios/official/) must match these prompts exactly. `src/tests/test_benchmark_runner.py` checks this.

**Do not retype or "fix" the prompts.** The typos and missing punctuation are part of the test. Testers copy and paste them.

---

## Rules

- Group: **Apartment 4B** (Sarah, Kayla, Rui). Sign in as **Sarah**.
- Start a fresh conversation for each scenario.
- Send each turn according to its mode:
  - `always`: send it after the previous response, even if the bot already showed a preview (B5's correction).
  - `if_asked`: send it only if the bot's last response was a question.
- **Pass** = every person's cost share, every person's amount paid, and every settlement transfer match the key to the cent, **and** the attempt uses 5 prompts or fewer.
- Behavior checks (B1 asks nothing; B2–B5 ask at least one question before the final preview) are recorded but do not change pass/fail.

Settlement uses net positions: `net = amount paid − cost share`. People with a negative net pay people with a positive net.

---

## B1 Basic

Turn 1 (`always`):

```text
sarah rui and kayla got dinner and it was 96 total w tax and tip. i paid the whole thing im sarah. split evenly pls
```

| Person | Cost share | Paid |
| --- | ---: | ---: |
| Sarah | $32.00 | $96.00 |
| Rui | $32.00 | $0.00 |
| Kayla | $32.00 | $0.00 |

Settlement: Kayla pays Sarah $32.00; Rui pays Sarah $32.00.

Expected prompts: 1. Behavior: should not ask a question.

---

## B2 Moderate

Turn 1 (`always`):

```text
dinner was me rui and kayla. im sarah. ruis meal was 18 mine was 24 and kaylas was 30. everyone pays for their own food
```

Turn 2 (`if_asked`):

```text
i paid. tax was $6 and tip was 14.40. split both proportionally based on what we ordered
```

| Person | Cost share | Paid |
| --- | ---: | ---: |
| Sarah | $30.80 | $92.40 |
| Rui | $23.10 | $0.00 |
| Kayla | $38.50 | $0.00 |

Settlement: Kayla pays Sarah $38.50; Rui pays Sarah $23.10 (Sarah receives $61.60).

Expected prompts: 2. Behavior: should ask at least one question first.

---

## B3 Intermediate

Turn 1 (`always`):

```text
rui and i split nachos and rui and kayla shared a pizza. everyone but kayla got a marg. i paid can u split it
```

Turn 2 (`if_asked`):

```text
nachos 18 pizza 36 and margs 12 each. yes equal for the shared food and one marg each. tax 9 tip 18 split those proportionally
```

| Person | Cost share | Paid |
| --- | ---: | ---: |
| Sarah | $28.27 | $105.00 |
| Rui | $52.50 | $0.00 |
| Kayla | $24.23 | $0.00 |

Settlement: Rui pays Sarah $52.50; Kayla pays Sarah $24.23 (Sarah receives $76.73).

Tax and tip are pooled into one $27.00 proportional allocation. Rounding them separately gives Sarah $28.28 and Kayla $24.22, which fails the key.

Expected prompts: 2. Behavior: should ask at least one question first.

---

## B4 Advanced

Turn 1 (`always`):

```text
trip was me rui and kayla. i paid 840 for the house, rui paid 120 groceries for everyone and kayla paid 90 for transportation just for me and her. me and rui stayed 3 nights kayla only stayed 1. split it fairly
```

Turn 2 (`if_asked`):

```text
yes to all of that. groceries equal even tho kayla stayed less. those are the final totals
```

| Person | Cost share | Paid |
| --- | ---: | ---: |
| Sarah | $445.00 | $840.00 |
| Rui | $400.00 | $120.00 |
| Kayla | $205.00 | $90.00 |

Settlement: Rui pays Sarah $280.00; Kayla pays Sarah $115.00.

House $840 split by nights (3 / 3 / 1), groceries $120 split equally, transportation $90 split between Sarah and Kayla. A pairwise implementation would say Kayla owes Rui $40, which fails the key.

Expected prompts: 2. Behavior: should ask at least one question first.

---

## B5 Most complex

Turn 1 (`always`):

```text
im sarah. trip w rui and kayla. i paid 600 lodging. me and rui stayed 3 nights kayla stayed 2. split lodging per person per night. rui paid dinner 120 split equal between all 3. kayla paid 60 taxi everyone except rui split equal. all amounts final no extra tax or fees
```

Turn 2 (`always`, sent even if the bot already showed a preview):

```text
wait kayla didnt eat dinner actually. rui said shed cover twice as much dinner as me. also i got a 100 refund on the lodging
```

Turn 3 (`if_asked`):

```text
yes same proportions and the refund went back to me
```

| Person | Cost share | Paid |
| --- | ---: | ---: |
| Sarah | $257.50 | $500.00 ($600 − $100 refund) |
| Rui | $267.50 | $120.00 |
| Kayla | $155.00 | $60.00 |

Settlement: Rui pays Sarah $147.50; Kayla pays Sarah $95.00.

Lodging $500 after the refund, split by nights (3 / 3 / 2). Dinner $120 split between Sarah and Rui at 1 : 2. Taxi $60 split between Sarah and Kayla.

Expected prompts: 3. Behavior: should ask at least one question first.

> **Open wording decision:** issue #31 notes that "shed" in turn 2 can be misread, and suggests "hed". The prompt above keeps the original wording. If the team changes it, update this file and `src/benchmark/scenarios/official/b5.json` together, and bump `PROMPT_VERSION` in `src/backend/config.py` only if the system prompt also changes.

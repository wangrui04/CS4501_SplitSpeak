
# Alpha Hypothesis and Testing Plan

## Core Hypothesis

Our AI expense assistant can generate an accurate expense
split within 5 user prompts in at least 90% of test attempts,
across varying levels of complexity.

## Alpha Testing Scope

- Testers: 3 development team members
- Scenarios: 5 benchmark scenarios, B1–B5 (see [benchmarks.md](benchmarks.md))
- Attempts: Each team member tests all 5 scenarios
- Total test attempts: 15
- Target accuracy: >= 90%
- Minimum passing attempts: 14 out of 15

> Revised from the original 6 scenarios / 18 attempts after the team adopted the benchmark document. The original six user-story scenarios are kept below and run as informational benchmark cases.

## Test Categories

### Simple Splits
1. Equal expense splitting
2. Splitting among selected participants

### Complicated Multi-Way Splits
3. Multiple items with different participants
4. Unequal quantities and tax/tip allocation

### Worst-Case Scenarios
5. Missing information, ambiguity, and typos
6. Conversational corrections

## Success Criteria

A test attempt passes if:
- Every person's cost share matches the answer key to the cent.
- Every person's amount paid matches the answer key.
- Every settlement transfer ("who pays whom") matches the answer key.
- The correct split is produced within 5 user prompts.

A prompt is defined as one user message sent to the LLM,
including clarification responses and corrections.

Results are recorded in [alpha-results.md](alpha-results.md).

## Evaluation Method

1. Prepare the expected answer for each scenario.
2. Each team member independently tests all 5 scenarios, pasting the prompts verbatim.
3. Record the AI's generated split.
4. Compare the results against the expected answer.
5. Record the number of prompts used.
6. Mark each attempt as Pass or Fail.
7. Calculate overall accuracy.

Accuracy = (Passed Attempts / Total Attempts) * 100

## Limitations

This is internal Alpha testing conducted by the development
team rather than independent users.

The results evaluate initial functional reliability but
do not establish accuracy across the broader target population.

Further external user validation will be needed.

# Splitwise AI — Conversational Expense Assistant

**CS 4501: Software Engineering Final Project**

## Project Overview

Splitwise AI is a shared-expense tracking application inspired by Splitwise, with an AI-powered conversational assistant.

The application aims to help users record shared expenses, track group balances, and split complex bills through natural-language instructions instead of manually calculating each person's share.

For example:

> "I paid $42. Kayla and I shared $12 nachos. Rui had a $15 burger, and Kayla had a $15 pasta."

The assistant identifies the payer, items, prices, and participants to produce a structured expense breakdown.

If information is missing or unclear, the assistant asks follow-up questions rather than making assumptions.

**All monetary calculations are performed using deterministic Python code, not the LLM.** Expense allocations must pass validation and be confirmed by the user before they are saved.

---

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, JavaScript, Vite |
| Backend | Python, FastAPI |
| Database | SQLite |
| AI Integration | Anthropic Claude API |
| Data Validation | Pydantic |
| Unit and Integration Testing | pytest |
| Property-Based Testing | Hypothesis |
| Version Control | Git and GitHub |
| Continuous Integration | GitHub Actions |

The intended architecture uses a React frontend communicating with a Python FastAPI backend through REST endpoints.

---

## Development Status

The project is currently in **Alpha Development**.

### Implemented and Tested

- React frontend: name-picker sign-in, group page with summary bar, month-grouped expense list, and balances panel
- AI assistant tab with prompt counter, itemized preview (shares, amounts paid, who pays whom), and confirm
- Manual-entry form backed by the same allocation engine and validator as the AI path
- Switch-to-manual escape hatch when the AI cannot resolve an expense
- FastAPI backend with SQLite, signed name-based sessions, and protected endpoints
- Integer-cents allocation: equal, itemized, quantities, weighted splits (nights, "twice as much"), per-item payers, refunds, and pooled tax/tip
- Net-position settlement ("simplified debts") for group balances and previews
- Claude structured-output client (`output_config.format`), with user text delimited as data
- Rate limiting, input sanitizing, CORS restriction, security headers, and secret redaction in logs
- Benchmark runner and report for scenarios B1–B5 (`python -m benchmark`)
- Playwright end-to-end smoke tests (run headless in CI)

### In Progress / Planned

- Alpha test session with 3 testers × 5 benchmark scenarios ([docs/alpha-results.md](docs/alpha-results.md))
- Live-LLM benchmark runs (Run 1/2/3) and report
- Settle up and conversational corrections UI (optional issues #38–#40)

**Note:** Passing automated tests verifies the tested implementation. It does not yet establish the accuracy of the complete application with real users or live AI responses.

---

## Developer Setup

For installation instructions, environment configuration, local development, troubleshooting, and testing commands, see:

**[SETUP.md](SETUP.md)**

The guide covers:

- Installing Python, Node.js, and npm
- Cloning the repository
- Setting up the Python virtual environment
- Installing dependencies
- Configuring environment variables
- Running the full application locally
- Running automated tests

---

## Running the Application Locally

The application consists of a FastAPI backend and a React frontend. Run each in a separate terminal:

### 1. Start the Backend API (Terminal 1)

From the project root:

```bash
PYTHONPATH=src .venv/bin/python -m uvicorn backend.main:get_app --factory --port 8000 --reload
```

- The API server runs at `http://127.0.0.1:8000`.
- The SQLite database is automatically created and seeded with sample groups (`Apartment 4B` and `Weekend trip`).
- If `ANTHROPIC_API_KEY` is provided in `.env`, the assistant connects to Claude. Otherwise, a built-in demo assistant handles sample splitting scenarios out of the box.

### 2. Start the React Frontend (Terminal 2)

In a second terminal:

```bash
cd src/frontend
npm run dev
```

*(Or from the repository root: `npm --prefix src/frontend run dev`)*.

- The Vite dev server starts at `http://localhost:5173`.
- API calls to `/api/*` are automatically proxied to `http://127.0.0.1:8000`.

### 3. Open in Your Browser

Navigate to **[http://localhost:5173](http://localhost:5173)**:

1. **Sign in:** Pick a user (e.g. **Sarah**, **Kayla**, or **Rui**) and click **Continue as...**.
2. **Dashboard:** View group balances, active group details, and friend lists.
3. **Add an Expense:** Click **+ Add an expense** and either click quick examples (*Try restaurant split*, *Try groceries*) or describe your expense in natural language.
4. **Confirm:** Review the itemized breakdown and confirm the expense to update balances live.

---

## Project Structure

The current development structure is:

```text
CS4501_Splitwise/
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── pull_request_template.md
│
├── docs/
│   ├── AlphaTesting.md
│   ├── UserStories.md
│   ├── alpha-validation-decision.md
│   ├── alpha-results.md
│   ├── alpha-submission.md
│   ├── api.md
│   └── benchmarks.md
│
├── src/
│   ├── benchmark_local.db
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── allocation.py
│   │   ├── validator.py
│   │   ├── database.py
│   │   ├── repository.py
│   │   ├── config.py        # model, prompt, limits
│   │   ├── llm.py
│   │   ├── pipeline.py
│   │   ├── settlement.py    # net settlement
│   │   ├── manual.py        # manual-entry builder
│   │   ├── security.py      # rate limit, sanitizing, headers
│   │   └── fixtures/        # test-only LLM fixtures
│   │
│   ├── benchmark/           # python -m benchmark
│   │   ├── scenarios/       # official, legacy, informational
│   │   └── results/
│   │
│   ├── frontend/
│   │   ├── package.json
│   │   ├── playwright.config.js
│   │   ├── e2e/
│   │   └── src/
│   │
│   ├── demo/
│   │   └── splitwise_ai_demo.html
│   │
│   └── tests/
│       ├── test_setup.py
│       ├── test_expense.py
│       ├── test_validator.py
│       ├── test_backend.py
│       └── test_llm.py
│
├── ideas/
├── AGENTS.md
├── README-startupSelected.md
├── README.md
├── SETUP.md
├── requirements.txt
├── pytest.ini
├── .env.example
└── .gitignore
```

The original HTML prototype is preserved in `src/demo/` as a reference for frontend development.

The React interface lives in `src/frontend/`.

---

## Core Features

### 1. Conversational Expense Entry

Users can describe shared expenses in natural language.

The AI assistant is designed to extract:

- Payer
- Purchased items and quantities
- Individual item prices
- Participants
- Excluded group members
- Tax, tip, and additional charges
- Instructions for splitting expenses

The extracted information is converted into structured data for further validation and calculation.

### 2. Expense Splitting

The Python allocation engine calculates each person's share.

Supported calculation scenarios include:

- Equal splitting
- Splitting among selected participants
- Itemized expenses with different participants
- Different item quantities
- Participant exclusions
- Equal or proportional allocation of additional charges

All calculations use integer cents to avoid floating-point rounding errors.

The sum of individual shares must equal the full expense total.

### 3. Clarification Questions

The assistant is designed to ask questions when information is missing, contradictory, or ambiguous.

Examples include:

- "Who paid for this expense?"
- "How much were the nachos?"
- "Did you mean Rui?"
- "Should the tip be split equally or proportionally?"

The conversation pipeline retains previous messages so users do not need to restate their entire expense.

### 4. Expense Validation

The backend validates expenses before saving.

Validation includes checking that:

- The payer belongs to the selected group.
- Participants are valid group members.
- Monetary amounts are valid.
- Individual shares are nonnegative integer amounts in cents.
- No participants are duplicated incorrectly.
- Individual shares add up to the expense total.
- Required information is present.

Invalid expenses are rejected rather than permanently stored.

### 5. Expense Preview and Confirmation

The intended user workflow is:

1. The user enters an expense manually or through the AI assistant.
2. The application calculates the allocation.
3. The backend validates the result.
4. The frontend displays an itemized breakdown.
5. The user reviews and confirms the breakdown.
6. The confirmed expense is saved.

The frontend implementation of this workflow is part of ongoing Alpha development.

### 6. Groups and Expense History

SQLite stores information about groups, members, expenses, individual shares, and conversations.

The Alpha prototype includes two sample groups.

**Apartment 4B**
- Sarah
- Kayla
- Rui

**Weekend Trip**
- Sarah
- Kayla
- Rui
- Aly
- Ben

These predefined groups allow the development team to test expense allocation and group management consistently.

### 7. Name-Based Demo Sessions

For the Alpha prototype, users can select their name from a predefined group-member roster.

The backend creates a signed session and protects group-related API endpoints.

This approach is intended for an internal demonstration and is not a replacement for production authentication.

---

## Alpha Development Hypothesis

Our core hypothesis is:

**The AI expense assistant can generate an accurate expense split within 5 user prompts in at least 90% of test attempts across varying levels of complexity.**

### Alpha Testing Plan

| Metric | Target |
|---|---|
| Testers | 3 development team members |
| Scenarios | 5 benchmark scenarios (B1 Basic … B5 Most complex) |
| Total attempts | 15 (3 testers × 5 scenarios) |
| Required successful attempts | 14 |
| Accuracy target | At least 90% |
| Prompt limit | 5 user prompts |

An attempt passes only when every person's cost share, every person's amount paid, and every settlement transfer match the answer key to the cent, within five user prompts.

### Benchmark Scenarios

The prompts and answer keys are in [docs/benchmarks.md](docs/benchmarks.md). Testers copy and paste the prompts, because the typos are part of the test.

1. **B1 Basic:** equal dinner split
2. **B2 Moderate:** everyone pays for their own meal, proportional tax and tip
3. **B3 Intermediate:** shared items, exclusions, quantities, proportional tax and tip
4. **B4 Advanced:** trip with three payers and a per-night house split
5. **B5 Most complex:** trip with per-night lodging, an unprompted correction, and a refund

The original six user-story scenarios (US-01…US-06) are kept as informational benchmark cases.

The Alpha testing plan uses internal team members to evaluate initial functionality.

External user validation may be performed in a later development stage, subject to course requirements and professor guidance.

See [AlphaTesting.md](docs/AlphaTesting.md) and [UserStories.md](docs/UserStories.md) for more details.

---

## Test-Driven Development

The project follows a **Red–Green–Refactor** development cycle.

### Red — Write Failing Tests

Tests are written based on the acceptance criteria of each GitHub issue.

They are run before implementation to verify the required behavior is not yet satisfied.

### Green — Implement the Feature

The minimum necessary functionality is implemented until the tests pass.

### Refactor — Improve the Implementation

The code is improved for readability, structure, and maintainability while keeping tests passing.

### Running Tests

From the repository root (use `py` on Windows):

```bash
# Backend unit and integration tests (no paid API calls)
python3 -m pytest src/tests/ -v --tb=short

# Frontend unit tests
npm --prefix src/frontend test

# End-to-end smoke tests (first run: npx playwright install chromium)
npm --prefix src/frontend run test:e2e
```

The E2E tests start their own backend with `LLM_PROVIDER=fake`, which returns scripted responses from `src/backend/fixtures/llm_fixtures.json`. That setting is **test-only** and never the default.

### Running the Benchmark

```bash
# Live run against Claude (needs ANTHROPIC_API_KEY; refuses to run in CI)
PYTHONPATH=src python3 -m benchmark run --runs 3 --model claude-sonnet-5-5

# Offline smoke run with the scripted fixtures (no API calls)
PYTHONPATH=src python3 -m benchmark run --provider fake --runs 1

# Markdown report for the latest results file
PYTHONPATH=src python3 -m benchmark report
```

Results are written to `src/benchmark/results/<timestamp>.json`. Add `--include-informational` to also run the US-01…US-06, messy-phrasing, and first-person cases. Those are excluded from pass rates.

### Test Organization

| Test File | Coverage |
|---|---|
| `test_setup.py` | Project structure, dependencies, configuration, and documentation |
| `test_expense.py` | Expense models, allocation, rounding, and edge cases |
| `test_trip_allocation.py` | Weighted splits, per-item payers, refunds, pooled tax/tip |
| `test_settlement.py` | Net settlement (benchmark keys as vectors) and group balances API |
| `test_validator.py` | Validation of expense data and allocations |
| `test_backend.py` | Database, persistence, groups, sessions, and API endpoints |
| `test_manual_entry.py` | Manual-entry endpoint |
| `test_security.py` | Rate limiting, prompt-injection hardening, CORS, headers, redaction |
| `test_first_person.py` | "I" / "me" resolution for every signed-in user |
| `test_us06_messy.py` | Messy language and typo handling |
| `test_llm.py` | Mock LLM, Claude integration, retries, and conversation processing |
| `test_benchmark_runner.py` | Benchmark comparator, runner flow, answer-key sanity, verbatim prompts |
| `test_benchmark_report.py` | Benchmark report rendering (snapshot) |

### Latest Local Test Results

As of November 2, 2026: **301 backend tests** and **91 frontend tests** passed locally. The Playwright specs run in CI.

These results come from automated tests with a mocked LLM. Live Claude accuracy is measured separately by the benchmark and the alpha test session.

---

## AI Integration Architecture

The AI assistant is responsible for interpreting natural-language expense descriptions.

It is not responsible for performing the final financial calculations.

The intended processing pipeline is:

```text
User enters expense description
             |
             v
    Anthropic Claude API
             |
             v
 Structured expense information
             |
             v
    Pydantic validation
             |
             v
  Python allocation engine
             |
             v
   Allocation validation
             |
             v
      Expense preview
             |
             v
      User confirmation
             |
             v
        SQLite database
```

The automated tests use a fake LLM implementation to validate the pipeline without requiring live API calls.

The actual performance of Claude on the six Alpha scenarios must be evaluated separately.

---

## Development Workflow

The team uses GitHub issues to organize feature development and testing requirements.

Recommended workflow:

1. Select an assigned GitHub issue.
2. Create a feature branch.
3. Write tests based on the acceptance criteria.
4. Confirm the tests initially fail.
5. Implement the required functionality.
6. Run the relevant tests.
7. Refactor as necessary.
8. Open a pull request.
9. Request teammate review before merging.

Before submitting a pull request, developers should verify that:

- Relevant tests pass.
- Changes satisfy the linked GitHub issue.
- No sensitive credentials are included.
- AI-generated code has been reviewed.
- Documentation is updated when necessary.

---

## Security and Environment Variables

The project uses environment variables for development configuration.

Configuration variables are documented in `.env.example`:

```env
ANTHROPIC_API_KEY=
LLM_MODEL=            # defaults to claude-sonnet-5-5
SESSION_SECRET=
WEB_ORIGINS=http://localhost:5173
```

`LLM_PROVIDER` can be set to `demo` (built-in demo assistant, the default without an API key), `claude`, or `fake` (test-only scripted fixtures).

Actual values belong in a local `.env` file.

**Never commit real API keys, passwords, or session secrets to GitHub.**

Automated LLM tests use mock responses and do not require a live Anthropic API key.

For setup and environment configuration, refer to [SETUP.md](SETUP.md).

---

## Future Development

Planned work includes:

- Running the alpha test session and recording results
- Settle up and conversational-correction UI
- External user testing in a later stage
- Voice input, after the text workflow is reliable

---

## Project Documentation

- [Developer Setup](SETUP.md)
- [Alpha Testing Plan](docs/AlphaTesting.md)
- [User Stories](docs/UserStories.md)
- [Alpha Validation Decision](docs/alpha-validation-decision.md)
- [Benchmark Scenarios B1–B5](docs/benchmarks.md)
- [Alpha Results](docs/alpha-results.md)
- [Alpha Submission Checklist and Activities Draft](docs/alpha-submission.md)
- [API Reference](docs/api.md)

Additional planning and development tasks are tracked through GitHub issues.

---

## Course Information

**Course:** CS 4501 — Software Engineering  
**Project:** Splitwise AI — Conversational Expense Assistant  
**Development Stage:** Alpha Development
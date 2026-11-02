"""Run every scenario N times and write a results file."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from backend.config import DEFAULT_LLM_MODEL, PROMPT_VERSION
from benchmark.runner import run_scenario
from benchmark.schema import RESULTS_DIR, ResultsFile, Run, load_scenarios


class BenchmarkRefused(RuntimeError):
    pass


def check_allowed(provider: str, env) -> None:
    if provider != "claude":
        return
    if env.get("CI"):
        raise BenchmarkRefused("Refusing to call the paid LLM API in CI. Use --provider fake.")
    if not env.get("ANTHROPIC_API_KEY"):
        raise BenchmarkRefused("ANTHROPIC_API_KEY is not set.")


def make_llm(provider: str, model: str, env):
    if provider == "fake":
        from backend.llm import FixtureLlmClient

        return FixtureLlmClient()

    from backend.llm import ClaudeLlmClient

    return ClaudeLlmClient(api_key=env["ANTHROPIC_API_KEY"], model=model)


def commit_sha() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def run_benchmark(
    runs: int = 3,
    model: str = DEFAULT_LLM_MODEL,
    provider: str = "claude",
    include_informational: bool = False,
    env=os.environ,
    progress=print,
) -> ResultsFile:
    check_allowed(provider, env)

    folders = ["official"]
    if include_informational:
        folders += ["legacy", "informational"]
    scenarios = load_scenarios(*folders)

    all_runs = []
    for number in range(1, runs + 1):
        llm = make_llm(provider, model, env)
        results = []
        for scenario in scenarios:
            result = run_scenario(scenario, llm)
            progress(
                f"run {number} {scenario.id}: "
                f"{'PASS' if result.passed else 'FAIL'} "
                f"({result.promptCount} prompts)"
                + (f" - {result.failureReason}" if result.failureReason else "")
            )
            results.append(result)
        all_runs.append(Run(run=number, official=number == 1, results=results))

    return ResultsFile(
        model=model if provider == "claude" else f"fake ({model} not called)",
        promptVersion=PROMPT_VERSION,
        commitSha=commit_sha(),
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        provider=provider,
        runs=all_runs,
    )


def write_results(results: ResultsFile, directory: Path = RESULTS_DIR) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stamp = results.timestamp.replace(":", "").replace("+0000", "Z")
    path = directory / f"{stamp}.json"
    path.write_text(results.model_dump_json(by_alias=True, indent=2) + "\n")
    return path


def latest_results(directory: Path = RESULTS_DIR) -> Path:
    files = sorted(directory.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No results in {directory}. Run the benchmark first.")
    return files[-1]

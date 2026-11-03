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


API_KEYS = {
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
}


def check_allowed(provider: str, env) -> None:
    if provider not in API_KEYS:
        return
    if env.get("CI"):
        raise BenchmarkRefused("Refusing to call a live LLM API in CI. Use --provider fake.")
    if not env.get(API_KEYS[provider]):
        raise BenchmarkRefused(f"{API_KEYS[provider]} is not set.")


def make_llm(provider: str, model: str, env):
    if provider == "fake":
        from backend.llm import FixtureLlmClient

        return FixtureLlmClient()

    if provider == "groq":
        from backend.llm import GroqLlmClient

        return GroqLlmClient(api_key=env["GROQ_API_KEY"], model=model)

    if provider == "gemini":
        from backend.llm import GeminiLlmClient

        return GeminiLlmClient(api_key=env["GEMINI_API_KEY"], model=model)

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
        model=model if provider != "fake" else f"fake ({model} not called)",
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

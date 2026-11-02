"""Benchmark CLI.

    PYTHONPATH=src python -m benchmark run --runs 3 --model claude-sonnet-5-5
    PYTHONPATH=src python -m benchmark run --provider fake
    PYTHONPATH=src python -m benchmark report [results.json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from backend.config import DEFAULT_LLM_MODEL
from benchmark.benchmark import (
    BenchmarkRefused,
    latest_results,
    run_benchmark,
    write_results,
)
from benchmark.report import render
from benchmark.schema import ResultsFile


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m benchmark")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="run the benchmark scenarios")
    run.add_argument("--runs", type=int, default=3)
    run.add_argument("--model", default=DEFAULT_LLM_MODEL)
    run.add_argument(
        "--provider", choices=["claude", "fake"], default="claude",
        help="fake uses the scripted test fixtures and calls no API",
    )
    run.add_argument("--include-informational", action="store_true")

    report = commands.add_parser("report", help="render a markdown report")
    report.add_argument("results", nargs="?", type=Path)

    args = parser.parse_args(argv)

    if args.command == "run":
        load_dotenv()
        try:
            results = run_benchmark(
                runs=args.runs,
                model=args.model,
                provider=args.provider,
                include_informational=args.include_informational,
            )
        except BenchmarkRefused as exc:
            print(f"benchmark: {exc}", file=sys.stderr)
            return 2
        path = write_results(results)
        print(f"wrote {path}")
        return 0

    path = args.results or latest_results()
    markdown = render(ResultsFile.model_validate_json(path.read_text()))
    path.with_suffix(".md").write_text(markdown)
    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())

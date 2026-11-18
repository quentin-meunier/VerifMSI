#!/usr/bin/env python3
# Copyright (C) 2023-2026, Sorbonne Universite, LIP6
# This file is part of the VerifMSI project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only

"""
Global test runner for VerifMSI (Python).

Discovers and runs unit tests under tests/ concurrently or sequentially,
and verifies outputs (OK / KO, error codes, leaks).
"""

import argparse
import concurrent.futures
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent

DEFAULT_SUITES = [
    "simplify",
    "extended_simplify",
    "large_int",
    "arith",
    "concrev",
    "ni",
    "tps/OK",
    "tps/KO",
    "mask_occ",
]

EXTRA_SUITES = [
    "hw",
    "propagate_const",
    "propagate_extract",
    "simp_rules",
    "graph",
]

ALL_SUITES = DEFAULT_SUITES + EXTRA_SUITES

# Regular expressions to match standalone OK / KO tokens in test output
OK_REGEX = re.compile(r"(?:^|\s|\[)OK(?:\]|\s|:|$)", re.MULTILINE)
KO_REGEX = re.compile(r"(?:^|\s|\[)KO(?:\]|\s|:|$)", re.MULTILINE)
LEAK_ZERO_REGEX = re.compile(r"Total Nb\. of potential leakages found:\s*0\b")
LEAK_NONZERO_REGEX = re.compile(r"Total Nb\. of potential leakages found:\s*[1-9]\d*\b")


@dataclass
class TestResult:
    suite: str
    name: str
    status: str  # "PASS", "FAIL", "NO_ASSERT", "TIMEOUT"
    duration_s: float
    returncode: int
    stdout: str
    stderr: str
    reason: str = ""


def execute_single_test(
    suite: str, test_path: Path, timeout: float, env: Dict[str, str]
) -> TestResult:
    t0 = time.perf_counter()
    try:
        res = subprocess.run(
            [sys.executable, str(test_path)],
            cwd=str(test_path.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        dt = time.perf_counter() - t0
        return TestResult(
            suite=suite,
            name=test_path.name,
            status="TIMEOUT",
            duration_s=dt,
            returncode=-1,
            stdout=exc.stdout or "" if isinstance(exc.stdout, str) else "",
            stderr=exc.stderr or "" if isinstance(exc.stderr, str) else "",
            reason=f"Timed out after {timeout}s",
        )

    dt = time.perf_counter() - t0
    out = res.stdout
    err = res.stderr

    if res.returncode != 0:
        return TestResult(
            suite=suite,
            name=test_path.name,
            status="FAIL",
            duration_s=dt,
            returncode=res.returncode,
            stdout=out,
            stderr=err,
            reason=f"Non-zero exit code ({res.returncode})",
        )

    has_assert_in_src = "assert" in test_path.read_text(encoding="utf-8", errors="ignore")
    has_ko = bool(KO_REGEX.search(out))
    if not has_assert_in_src and bool(LEAK_NONZERO_REGEX.search(out)):
        has_ko = True

    has_ok = bool(OK_REGEX.search(out)) or bool(LEAK_ZERO_REGEX.search(out)) or (has_assert_in_src and not has_ko)

    if has_ko:
        return TestResult(
            suite=suite,
            name=test_path.name,
            status="FAIL",
            duration_s=dt,
            returncode=res.returncode,
            stdout=out,
            stderr=err,
            reason="Output contains 'KO' or unexpected leakage",
        )

    if not has_ok:
        return TestResult(
            suite=suite,
            name=test_path.name,
            status="NO_ASSERT",
            duration_s=dt,
            returncode=res.returncode,
            stdout=out,
            stderr=err,
            reason="Exited with 0 but printed no 'OK' check result",
        )

    return TestResult(
        suite=suite,
        name=test_path.name,
        status="PASS",
        duration_s=dt,
        returncode=0,
        stdout=out,
        stderr=err,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run VerifMSI unit tests.")
    parser.add_argument(
        "--suite",
        dest="suites",
        action="append",
        choices=ALL_SUITES,
        help="Select specific suite(s) to run.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all suites including extra/legacy ones.",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=os.cpu_count() or 4,
        help="Number of parallel worker jobs (default: CPU count).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-test timeout in seconds (default: 30.0).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print detailed test execution information.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat NO_ASSERT (0 exit code but no assertion) as failure.",
    )
    args = parser.parse_args()

    suites_to_run = args.suites or (ALL_SUITES if args.all else DEFAULT_SUITES)
    env = os.environ.copy()
    current_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{ROOT_DIR.parent}:{ROOT_DIR}:{current_pp}"

    print(f"==> Running VerifMSI unit tests with {args.jobs} jobs...")
    all_results: List[TestResult] = []
    start_time = time.perf_counter()

    for suite in suites_to_run:
        suite_dir = ROOT_DIR / "tests" / suite
        if not suite_dir.is_dir():
            continue

        test_files = sorted(
            [f for f in suite_dir.glob("*.py") if f.name != "__init__.py"]
        )
        if not test_files:
            continue

        suite_results: List[TestResult] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [
                pool.submit(execute_single_test, suite, f, args.timeout, env)
                for f in test_files
            ]
            for fut in concurrent.futures.as_completed(futures):
                suite_results.append(fut.result())

        suite_results.sort(key=lambda r: r.name)
        all_results.extend(suite_results)

        n_pass = sum(1 for r in suite_results if r.status == "PASS")
        n_fail = sum(1 for r in suite_results if r.status in ("FAIL", "TIMEOUT"))
        n_warn = sum(1 for r in suite_results if r.status == "NO_ASSERT")
        status_tag = "OK" if n_fail == 0 else "FAIL"
        warn_str = f", {n_warn} no-assert" if n_warn > 0 else ""
        print(
            f"  [{status_tag:4s}] Suite {suite:20s}: "
            f"{n_pass:3d}/{len(suite_results):3d} passed{warn_str}"
        )

        if args.verbose:
            for r in suite_results:
                print(f"         - {r.name:28s} [{r.status}] ({r.duration_s*1000:.1f} ms)")

    total_time = time.perf_counter() - start_time
    passed = [r for r in all_results if r.status == "PASS"]
    failed = [r for r in all_results if r.status in ("FAIL", "TIMEOUT")]
    no_assert = [r for r in all_results if r.status == "NO_ASSERT"]

    print("\n" + "=" * 70)
    print(
        f"Summary: {len(passed)} passed, {len(failed)} failed, "
        f"{len(no_assert)} without assertion (total: {len(all_results)} in {total_time:.2f}s)"
    )
    print("=" * 70)

    if failed:
        print("\nFailed tests:")
        for r in failed:
            print(f"  [FAIL] {r.suite}/{r.name}: {r.reason}")
            if r.stdout.strip():
                for line in r.stdout.strip().splitlines()[-5:]:
                    print(f"         stdout: {line}")
            if r.stderr.strip():
                for line in r.stderr.strip().splitlines()[-5:]:
                    print(f"         stderr: {line}")

    if failed or (args.strict and no_assert):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

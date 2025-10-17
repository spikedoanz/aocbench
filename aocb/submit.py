import json
import os
import subprocess
import time
from itertools import product
from typing import Any, Dict, Iterable, List, Optional

from aocd import submit
from aocd.models import Puzzle
from aocb.defaults import SOLUTIONS_PATH, INPUTS_PATH, CACHE_PATH


SOLUTIONS_FILE = CACHE_PATH / "solutions.json"


def save_answers(years: List[int], days: List[int]) -> None:
    """Run all solutions and save answers to disk."""
    solutions_path = SOLUTIONS_PATH
    inputs_path = INPUTS_PATH

    # Collect available solutions and inputs
    available_solutions = set()
    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        solution_file = solutions_path / str(year) / "python" / f"day_{day_str}.py"
        input_file = inputs_path / f"{year}_{day_str}.txt"

        if solution_file.exists() and input_file.exists():
            available_solutions.add((year, day))

    print(f"Found {len(available_solutions)} solutions with inputs")

    results = []
    for (year, day) in sorted(available_solutions):
        day_str = "0" + str(day) if day < 10 else str(day)
        filepath = solutions_path / str(year) / "python" / f"day_{day_str}.py"

        print(f"Running: {filepath}")
        try:
            result = subprocess.run(
                ["python", str(filepath)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"  Error running {filepath}: {result.stderr}")
                continue

            lines = result.stdout.strip().split('\n')

            if len(lines) < 1:
                print("  No output from script")
                continue

            part1 = lines[0].strip()
            part2 = lines[1].strip() if len(lines) >= 2 else None

            print(f"  Part 1: {part1}")
            if part2:
                print(f"  Part 2: {part2}")

            results.append({
                "year": year,
                "day": day,
                "part1": part1,
                "part2": part2
            })

        except subprocess.TimeoutExpired:
            print(f"  Timeout running {filepath}")
        except Exception as e:
            print(f"  Unexpected error: {e}")

    # Save to disk
    CACHE_PATH.mkdir(parents=True, exist_ok=True)
    with open(SOLUTIONS_FILE, 'w') as f:
        json.dump({"solutions": results}, f, indent=2)

    print(f"\nSaved {len(results)} solutions to {SOLUTIONS_FILE}")


def load_answers() -> List[Dict[str, Any]]:
    """Load answers from disk."""
    if not SOLUTIONS_FILE.exists():
        return []

    with open(SOLUTIONS_FILE, 'r') as f:
        data = json.load(f)

    return data.get("solutions", [])


def get_answer(year: int, day: int) -> Optional[Dict[str, Any]]:
    """Get a specific answer from saved solutions."""
    solutions = load_answers()

    for sol in solutions:
        if sol["year"] == year and sol["day"] == day:
            return sol

    return None


def submit_all(
    years: Optional[Iterable[int]] = None,
    days: Optional[Iterable[int]] = None,
    dry_run: bool = False,
    delay: float = 2.0,
) -> None:
    """Submit saved solutions to Advent of Code.

    Args:
        years: Iterable of years to submit. If omitted, submit every cached year.
        days: Iterable of days to submit. If omitted, submit every cached day.
        dry_run: When True, print the submissions without sending them.
        delay: Delay in seconds between submissions to respect rate limits.
    """
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please get an AOC token https://github.com/wimglenn/advent-of-code-wim/issues/1"

    solutions = load_answers()

    if not solutions:
        print("No solutions found. Run save_answers() first.")
        return

    year_filter = set(years) if years is not None else None
    day_filter = set(days) if days is not None else None

    filtered = [
        sol
        for sol in solutions
        if (year_filter is None or sol["year"] in year_filter)
        and (day_filter is None or sol["day"] in day_filter)
    ]

    if not filtered:
        print("No matching solutions found for the specified filters.")
        return

    print(f"Submitting {len(filtered)} solutions to AOC")

    for sol in filtered:
        year = sol["year"]
        day = sol["day"]
        part1 = sol.get("part1")
        part2 = sol.get("part2")

        puzzle = Puzzle(year=year, day=day)

        print(f"\nYear {year} Day {day}:")

        # Submit part A
        if part1 and not puzzle.answered_a:
            if dry_run:
                print(f"  Dry run: would submit part A = {part1}")
            else:
                try:
                    ret = submit(part1, part="a", day=day, year=year, reopen=False)
                    print(ret)
                    print(f"  Submitted part A: {part1}")
                except Exception as e:
                    print(f"  Error submitting part A: {e}")

            time.sleep(delay)  # rate limiting
        elif part1:
            print(f"  Part A already solved")

        # Submit part B
        if part2 and not puzzle.answered_b:
            if dry_run:
                print(f"  Dry run: would submit part B = {part2}")
            else:
                try:
                    ret = submit(part2, part="b", day=day, year=year, reopen=False)
                    print(ret)
                    print(f"  Submitted part B: {part2}")
                except Exception as e:
                    print(f"  Error submitting part B: {e}")

            time.sleep(delay)  # rate limiting
        elif part2:
            print(f"  Part B already solved")


def run_and_submit(
    years: Iterable[int],
    days: Iterable[int],
    *,
    refresh: bool = True,
    dry_run: bool = False,
    delay: float = 2.0,
) -> None:
    """Run cached solution scripts and submit their answers.

    This helper wraps ``save_answers`` followed by ``submit_all`` so that a single
    call will refresh cached outputs and (optionally) submit them.

    Args:
        years: Iterable of years to process.
        days: Iterable of days to process for each year.
        refresh: When True, solution scripts are re-executed before submitting.
        dry_run: When True, skip actual submissions (useful for verification).
        delay: Delay in seconds between submissions to respect rate limits.
    """
    if refresh:
        save_answers(list(years), list(days))

    submit_all(years=years, days=days, dry_run=dry_run, delay=delay)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run cached Advent of Code solutions and submit the answers."
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        required=True,
        help="Years to process (e.g. --years 2016 2017).",
    )
    parser.add_argument(
        "--days",
        type=int,
        nargs="+",
        default=list(range(1, 26)),
        help="Specific days to process (default: all 1-25).",
    )
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Use cached answers without rerunning solution scripts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the submissions without sending them to Advent of Code.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay in seconds between submissions (default: 2.0).",
    )

    args = parser.parse_args()
    run_and_submit(
        years=args.years,
        days=args.days,
        refresh=not args.no_refresh,
        dry_run=args.dry_run,
        delay=args.delay,
    )

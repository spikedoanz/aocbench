import json
import os
import subprocess
import time
from itertools import product
from typing import List, Dict, Optional, Any

from aocd import submit
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


def load_answers() -> List[Dict[str, any]]:
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


def submit_all() -> None:
    """Submit all saved solutions to Advent of Code."""
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please get an AOC token https://github.com/wimglenn/advent-of-code-wim/issues/1"

    solutions = load_answers()

    if not solutions:
        print("No solutions found. Run save_answers() first.")
        return

    print(f"Submitting {len(solutions)} solutions to AOC")

    for sol in solutions:
        year = sol["year"]
        day = sol["day"]
        part1 = sol.get("part1")
        part2 = sol.get("part2")

        print(f"\nYear {year} Day {day}:")

        # Submit part A
        if part1:
            try:
                submit(part1, part="a", day=day, year=year)
                print(f"  Submitted part A: {part1}")
            except Exception as e:
                print(f"  Error submitting part A: {e}")

            time.sleep(2)  # rate limiting

        # Submit part B
        if part2:
            try:
                submit(part2, part="b", day=day, year=year)
                print(f"  Submitted part B: {part2}")
            except Exception as e:
                print(f"  Error submitting part B: {e}")

            time.sleep(2)  # rate limiting


if __name__ == "__main__":
    days = [i for i in range(1, 26)]
    years = [i for i in range(2015, 2016)]

    # Run all solutions and save answers
    save_answers(years, days)

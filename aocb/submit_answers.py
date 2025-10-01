import os
import subprocess
import time
from pathlib import Path
from itertools import product

from aocd import submit

if __name__ == "__main__":
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please get an AOC token https://github.com/wimglenn/advent-of-code-wim/issues/1"

    days  = [i for i in range(1,26)]
    years = [i for i in range(2015, 2025)]

    solutions_path = Path("./solutions")
    inputs_path = Path("./inputs")

    # Collect available solutions and inputs
    available_solutions = set()
    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        solution_file = solutions_path / str(year) / "python" / f"day_{day_str}.py"
        input_file = inputs_path / f"{year}_{day_str}.txt"

        if solution_file.exists() and input_file.exists():
            available_solutions.add((year, day))

    print(f"Found {len(available_solutions)} solutions with inputs")

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

            if len(lines) < 2:
                print(f"  Expected 2 lines of output, got {len(lines)}")
                continue

            part_a = lines[0].strip()
            part_b = lines[1].strip()

            print(f"  Part A: {part_a}")
            print(f"  Part B: {part_b}")

            # Submit part A
            try:
                submit(part_a, part="a", day=day, year=year)
                print(f"  Submitted part A")
            except Exception as e:
                print(f"  Error submitting part A: {e}")

            time.sleep(2)  # rate limiting

            # Submit part B
            try:
                submit(part_b, part="b", day=day, year=year)
                print(f"  Submitted part B")
            except Exception as e:
                print(f"  Error submitting part B: {e}")

            time.sleep(2)  # rate limiting

        except subprocess.TimeoutExpired:
            print(f"  Timeout running {filepath}")
        except Exception as e:
            print(f"  Unexpected error: {e}")

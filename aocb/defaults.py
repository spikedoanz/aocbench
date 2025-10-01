from typing import Tuple
from pathlib import Path

AVAILABLE_YEARS = list(range(2015, 2017))
cache_path      = Path("~/.cache/aocb/")
problems_path   = Path("./problems/txt")
inputs_path     = Path("./inputs/") 
solutions_path  = Path("./solutions")


SYSTEM_PROMPT = """
You're in an text editing environment on a computer.
You're a programmer proficient at the Lean4 programming language.
"""

USER_PROMPT = """
You find before yourself a programming puzzle:

{part1_text}
{part2_text}

===========================================================

Please solve the problem by writing pure lean code, you should 
structure your submission as follows:

```lean4
import Input

def part1 (input : String) -> String := ...

def part2 (input : String) -> String :=

def main : IO Unit := do
  IO.println part1 Input.string
  IO.println part2 Input.string
```

make sure to only include the exact string of the solution.

Good luck, have fun!
"""

def get_solution_path(
    year: int,
    day: int,
    solutions_path: Path = solutions_path, 
) -> Path:
    assert year in AVAILABLE_YEARS
    assert day in range(1,26)
    day_str = "day_0" + str(day) if day < 10 else "day_" + str(day)
    ret = solutions_path / str(year) / "python" / (day_str + ".py")
    return ret

def get_problem_path(
    year: int,
    day: int,
    problems_path: Path = problems_path, 
) -> Tuple[Path, Path]:
    assert year in AVAILABLE_YEARS
    assert day in range(1,26)
    day_str = "0" + str(day) if day < 10 else str(day)
    part1_fn = str(year) + "_" + day_str + "_part1.txt"
    part2_fn = str(year) + "_" + day_str + "_part2.txt"
    return (problems_path / part1_fn,
            problems_path / part2_fn,)

def get_inputs_path(
    year: int,
    day: int,
    inputs_path: Path = inputs_path, 
) -> Path:
    assert year in AVAILABLE_YEARS
    assert day in range(1,26)
    day_str = "0" + str(day) if day < 10 else str(day)
    input_fn = str(year) + "_" + day_str + ".txt"
    return inputs_path / input_fn

def path_to_str(
    path: Path
) -> str:
    assert path.is_file()
    with open(path, "r") as f:
        return f.read()


def get_prompt(
    year:int,
    day:int,
    template= USER_PROMPT,
) -> str:
    p1_str, p2_str = map(path_to_str, get_problem_path(year,day))
    if day == 25: p2_str = "" # day 25 part 2 is flavor text            
    return template.format(
        part1_text = p1_str, part2_text = p2_str
    )

print(get_prompt(2015,14))

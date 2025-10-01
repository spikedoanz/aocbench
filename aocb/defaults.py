from typing import Tuple
from pathlib import Path

AVAILABLE_YEARS = list(range(2015, 2017))
cache_path      = Path("~/.cache/aocb/")
problems_path   = Path("./problems/txt")
inputs_path     = Path("./inputs/") 
solutions_path  = Path("./solutions")

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

p1, p2 = get_problem_path(2015, 25)
print(p1)
assert p1.is_file()
assert p2.is_file()
inp = get_inputs_path(2015,10)
print(inp)
assert inp.is_file()

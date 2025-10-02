import subprocess
from subprocess import CompletedProcess
from typing import Tuple, Optional
from pathlib import Path

AVAILABLE_YEARS = list(range(2015, 2017))
cache_path      = Path("~/.cache/aocb/").expanduser()
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

def get_input_path(
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

"""
1. build project structure
§ tree
.
└── {submission_name} Sonnet45_2025_14
    ├── lake-manifest.json
    ├── lakefile.toml
    ├── lean-toolchain
    ├── Main.lean
    ├── README.md
    └── {submission_name} 
        └── Input.lean

1.1
"""

def create_task(
    project_root_dir = cache_path / "submissions",
    project_name = "Y2025D14ExampleTask",
    input_str = path_to_str(get_input_path(2015,14,inputs_path)), 
):
    project_root_dir.mkdir(parents=True, exist_ok=True)
    project_exe  = project_name.lower()

    submission_str = f"""import {project_name}.Input

def part1 (s: String) : String := s
def part2 (s: String) : String := s

def main : IO Unit := do
  IO.println (part1 {project_name}.Input.input)
  IO.println (part2 {project_name}.Input.input)
    """

    project_files = [
        # ---------------------------------------
        ("lake-manifest.json", f"""{{
 "version": "1.1.0",
 "packagesDir": ".lake/packages",
 "packages": [],
 "name": "{project_name}",
 "lakeDir": ".lake"
}}"""),
        #----------------------------------------
        ("lakefile.toml", f"""name = "{project_name}"
version = "0.1.0"
defaultTargets = ["{project_exe}"]

[[lean_lib]]
name = "{project_name}"

[[lean_exe]]
name = "{project_exe}"
root = "Main"
"""),
        #---------------------------------------- 
        # this is put inside {project_name}/Input.lean
        (f"{project_name}/Input.lean", f"""namespace {project_name}.Input
def input := "{input_str}"
end {project_name}.Input
"""),
        # Main.lean is the model input ----------
        ("Main.lean", submission_str),
    ]

    for filepath, content in project_files:
        path = project_root_dir / project_name / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)




def run_task(
    project_root_dir = cache_path / "submissions",
    project_name = "Y2025D14ExampleTask",
) -> Tuple[CompletedProcess, Optional[CompletedProcess]]:
    assert project_root_dir.exists()
    assert (project_root_dir/project_name).exists()
    compile_result = subprocess.run(
        ["lake", "build"],
        cwd = (project_root_dir/project_name),
        capture_output= True,
        text = True,
    )
    if compile_result.returncode != 0:
        return compile_result, None
    run_result = subprocess.run(
        ["lake", "exec", project_name.lower()],
        cwd = (project_root_dir/project_name),
        capture_output= True,
        text = True,
    )
    return compile_result, run_result


create_task()
c, r = run_task()
print(c)
print(r)

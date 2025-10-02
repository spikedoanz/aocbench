import subprocess
from typing import Tuple
from pathlib import Path
from jinja2 import Template

from .defaults import (
    AVAILABLE_YEARS,
    CACHE_PATH,
    PROBLEMS_TXT_PATH,
    INPUTS_PATH,
    SOLUTIONS_PATH
)

cache_path = CACHE_PATH
problems_path = PROBLEMS_TXT_PATH
inputs_path = INPUTS_PATH
solutions_path = SOLUTIONS_PATH

SYSTEM_PROMPT = """
You're in an text editing environment on a computer.
You're a programmer proficient at the Lean4 programming language.
"""

USER_PROMPT_TEMPLATE = Template("""
You find before yourself a programming puzzle:

{{ part1_text }}
{{ part2_text }}

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
""")

# Template for lake-manifest.json
LAKE_MANIFEST_TEMPLATE = Template("""{
 "version": "1.1.0",
 "packagesDir": ".lake/packages",
 "packages": [],
 "name": "{{ project_name }}",
 "lakeDir": ".lake"
}""")

# Template for lakefile.toml
LAKEFILE_TEMPLATE = Template("""name = "{{ project_name }}"
version = "0.1.0"
defaultTargets = ["{{ project_exe }}"]

[[lean_lib]]
name = "{{ project_name }}"

[[lean_exe]]
name = "{{ project_exe }}"
root = "Main"
""")

# Template for Input.lean
INPUT_LEAN_TEMPLATE = Template("""namespace {{ project_name }}.Input
def input := "{{ input_str }}"
end {{ project_name }}.Input
""")

# Template for Main.lean
MAIN_LEAN_TEMPLATE = Template("""import {{ project_name }}.Input

def part1 (s: String) : String := s
def part2 (s: String) : String := s

def main : IO Unit := do
  IO.println (part1 {{ project_name }}.Input.input)
  IO.println (part2 {{ project_name }}.Input.input)
""")


def validate_year_day(year: int, day: int) -> None:
    """Validate year and day parameters."""
    if year not in AVAILABLE_YEARS:
        raise ValueError(f"Year {year} not in available years: {AVAILABLE_YEARS}")
    if day not in range(1, 26):
        raise ValueError(f"Day {day} must be between 1 and 25")


def get_solution_path(
    year: int,
    day: int,
    solutions_path: Path = solutions_path,
) -> Path:
    validate_year_day(year, day)
    day_str = f"day_{day:02d}"
    return solutions_path / str(year) / "python" / f"{day_str}.py"


def get_problem_path(
    year: int,
    day: int,
    problems_path: Path = problems_path,
) -> Tuple[Path, Path]:
    validate_year_day(year, day)
    day_str = f"{day:02d}"
    part1_fn = f"{year}_{day_str}_part1.txt"
    part2_fn = f"{year}_{day_str}_part2.txt"
    return (problems_path / part1_fn, problems_path / part2_fn)


def get_input_path(
    year: int,
    day: int,
    inputs_path: Path = inputs_path,
) -> Path:
    validate_year_day(year, day)
    day_str = f"{day:02d}"
    input_fn = f"{year}_{day_str}.txt"
    return inputs_path / input_fn


def path_to_str(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text()


def get_prompt(year: int, day: int) -> str:
    part1_path, part2_path = get_problem_path(year, day)
    part1_text = path_to_str(part1_path)
    part2_text = path_to_str(part2_path) if day != 25 else ""  # day 25 part 2 is flavor text
    
    return USER_PROMPT_TEMPLATE.render(
        part1_text=part1_text,
        part2_text=part2_text
    )


def create_task(
    project_root_dir: Path = cache_path / "submissions",
    project_name: str = "Y2025D14ExampleTask",
    input_str: str = path_to_str(get_input_path(2015, 14, inputs_path)),
) -> None:
    """Create a Lean4 project structure with templated files."""
    project_root_dir.mkdir(parents=True, exist_ok=True)
    project_exe = project_name.lower()
    
    # Define all project files with their templates
    project_files = [
        ("lake-manifest.json", LAKE_MANIFEST_TEMPLATE.render(project_name=project_name)),
        ("lakefile.toml", LAKEFILE_TEMPLATE.render(
            project_name=project_name,
            project_exe=project_exe
        )),
        (f"{project_name}/Input.lean", INPUT_LEAN_TEMPLATE.render(
            project_name=project_name,
            input_str=input_str
        )),
        ("Main.lean", MAIN_LEAN_TEMPLATE.render(project_name=project_name)),
    ]
    
    # Write all files
    for filepath, content in project_files:
        path = project_root_dir / project_name / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def run_task(
    project_root_dir: Path = cache_path / "submissions",
    project_name: str = "Y2025D14ExampleTask",
):
    """Build and run a Lean4 project."""
    project_path = project_root_dir / project_name
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project not found: {project_path}")
    
    # Compile the project
    compile_result = subprocess.run(
        ["lake", "build"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    
    # Only run if compilation succeeded
    run_result = None
    if compile_result.returncode == 0:
        run_result = subprocess.run(
            ["lake", "exec", project_name.lower()],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
    
    return compile_result, run_result


if __name__ == "__main__":
    create_task()
    compile_result, run_result = run_task()
    print("Compile result:", compile_result)
    print("Run result:", run_result)

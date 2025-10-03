import os
import re
import subprocess
import uuid
from subprocess import CompletedProcess
from itertools import product
from typing import Tuple, List, Dict
from pathlib import Path
from jinja2 import Template

from aocb.defaults import (
    AVAILABLE_YEARS,
    CACHE_PATH,
    PROBLEMS_TXT_PATH,
    INPUTS_PATH,
    SOLUTIONS_PATH,
    DEFAULT_PROJECT_NAME,
    DEFAULT_LAKE_TIMEOUT
)

from aocb.submit import get_answer
from aocb.docs import DOCS

SYSTEM_PROMPT = f"""
You're in an text editing environment on a computer.
You're a programmer proficient at the Lean4 programming language.

You look inside your pocket, and find a giant instruction manual,
it reads:
{DOCS}
"""

USER_PROMPT_TEMPLATE = Template("""
You find before yourself a programming puzzle:

{{ part1_text }}
{{ part2_text }}

===========================================================

Please solve the problem by writing pure lean code, you should
structure your submission as follows:

```lean4
import {{ project_name }}.Input

def part1 (input : String) -> String := ...

def part2 (input : String) -> String :=

def main : IO Unit := do
  IO.println part1 {{ project_name }}.Input.input
  IO.println part2 {{ project_name }}.Input.input
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
# batteries are required for hashmap
LAKEFILE_TEMPLATE = Template("""name = "{{ project_name }}"
version = "0.1.0"
defaultTargets = ["{{ project_exe }}"]

[[require]]
name = "batteries"
scope = "leanprover-community"
rev = "main"

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

def part1 (s: String) : String := "hello"
def part2 (s: String) : String := "advent of code bench"

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
) -> Path:
    solutions_path = SOLUTIONS_PATH
    validate_year_day(year, day)
    day_str = f"day_{day:02d}"
    return solutions_path / str(year) / "python" / f"{day_str}.py"


def get_problem_path(
    year: int,
    day: int,
) -> Tuple[Path, Path]:
    problems_path = PROBLEMS_TXT_PATH
    validate_year_day(year, day)
    day_str = f"{day:02d}"
    part1_fn = f"{year}_{day_str}_part1.txt"
    part2_fn = f"{year}_{day_str}_part2.txt"
    return (problems_path / part1_fn, problems_path / part2_fn)


def get_input_path(
    year: int,
    day: int,
) -> Path:
    inputs_path = INPUTS_PATH
    validate_year_day(year, day)
    day_str = f"{day:02d}"
    input_fn = f"{year}_{day_str}.txt"
    return inputs_path / input_fn


def path_to_str(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text()


def get_prompt(year: int, day: int) -> str:
    project_name = DEFAULT_PROJECT_NAME
    part1_path, part2_path = get_problem_path(year, day)
    part1_text = path_to_str(part1_path)
    part2_text = path_to_str(part2_path) if day != 25 else ""  # day 25 part 2 is flavor text

    return USER_PROMPT_TEMPLATE.render(
        part1_text=part1_text,
        part2_text=part2_text,
        project_name=project_name
    )


def create_task(
    spec: Dict,
    submission: str = MAIN_LEAN_TEMPLATE.render(project_name=DEFAULT_PROJECT_NAME),
) -> str:
    """Create a Lean4 project structure with templated files.

    Args:
        spec: Task specification dict containing task_identifier, year, and day
        submission: Lean4 code to use as Main.lean

    Returns:
        The task_identifier used for the created task.
    """
    task_identifier = spec["task_identifier"]
    year = spec["year"]
    day = spec["day"]

    project_root_dir = CACHE_PATH / "submissions"
    project_name = DEFAULT_PROJECT_NAME
    input_str = path_to_str(get_input_path(year, day))
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
        ("Main.lean", submission),
    ]

    # Write all files
    for filepath, content in project_files:
        path = project_root_dir / task_identifier / project_name / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    return task_identifier


def run_task(
    task_identifier: str,
):
    """Build and run a Lean4 project."""
    project_root_dir = CACHE_PATH / "submissions"
    project_name = DEFAULT_PROJECT_NAME
    project_path = project_root_dir / task_identifier / project_name
    
    if int(os.environ.get("VERBOSE", 0)) > 0: 
        print(f"Running task at {project_path}")
    if not project_path.exists():
        raise FileNotFoundError(f"Project not found: {project_path}")
    
    # Compile the project

    _update_result = subprocess.run(
        ["lake", "update"],
        cwd=project_path,
        capture_output=True,
        text=True,
        timeout=DEFAULT_LAKE_TIMEOUT,
    ) # required for batteries

    compile_result = subprocess.run(
        ["lake", "build"],
        cwd=project_path,
        capture_output=True,
        text=True,
        timeout=DEFAULT_LAKE_TIMEOUT,
    )
    
    # Only run if compilation succeeded
    run_result = None
    if compile_result.returncode == 0:
        run_result = subprocess.run(
            ["lake", "exec", project_name.lower()],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=DEFAULT_LAKE_TIMEOUT,
        )
    
    if int(os.environ.get("VERBOSE", 0)) > 0: 
        print(f"Ran task at {project_path}")
    return compile_result, run_result


def create_spec(year: int, day: int) -> Dict:
    """Create a task specification with unique identifier.

    Returns a dict containing all information needed to create a task environment.
    """
    task_identifier = f"{year}_{day:02d}_{uuid.uuid4()}"
    return {
        "task_identifier": task_identifier,
        "year": year,
        "day": day,
        "prompt": get_prompt(year, day)
    }

def load_tasks(
    years: List[int] = [2015],
    days: List[int] = list(range(1, 26)),
) -> List[Dict]:
    targets = product(years, days)
    return [create_spec(year, day) for year, day in targets]

def extract_lean4_block(text: str) -> str|None:
    """Extract content from ```lean4 ``` code block."""
    pattern = r'```lean4\s*\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def compile_reward(compile_result: CompletedProcess) -> float:
    if compile_result.returncode != 0:
        return 0.0
    else:
        return 1.0 

def correctness_reward(
    year: int,
    day: int,
    run_result: CompletedProcess | None,
    p1_weight: float = 0.5,  # assigned to part 1
    format_reward: float = 0.3
) -> float:
    if run_result is None:
        return 0.0
    answer = get_answer(year, day)
    assert answer, f"No cached answer for {year}, {day}"  # TODO: invoke save answer
    p1, p2 = answer['part1'], answer['part2']
    
    # Parse the output
    output = run_result.stdout.strip() if run_result.stdout else ""
    lines = output.split('\n')
    
    # Calculate format reward
    format_score = format_reward if len(lines) == 2 else 0.0
    
    # Determine if p2 exists (adjust weights accordingly)
    p2_exists = p2 is not None and p2 != ""
    
    if p2_exists:
        # Both parts exist, use the provided weights
        p2_weight = 1.0 - p1_weight - format_reward
    else:
        # Only part 1 exists, assign all non-format reward to p1
        p1_weight = 1.0 - format_reward
        p2_weight = 0.0
    
    # Calculate correctness scores
    p1_score = 0.0
    p2_score = 0.0
    
    if len(lines) >= 1:
        p1_score = p1_weight if lines[0] == p1 else 0.0
    
    if p2_exists and len(lines) >= 2:
        p2_score = p2_weight if lines[1] == p2 else 0.0
    
    # Total reward
    total_reward = format_score + p1_score + p2_score
    return total_reward


if __name__ == "__main__":
    spec = create_spec(2015, 14)
    task_id = create_task(spec)
    print(f"Created task: {task_id}")
    compile_result, run_result = run_task(task_id)
    print("Compile result:", compile_result)
    print("Run result:", run_result)
    print(compile_reward(compile_result))
    print(correctness_reward(2015, 14, run_result))
    print(spec["task_identifier"])

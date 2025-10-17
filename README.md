# Advent of Code Bench

A Lean4 benchmarking environment for Advent of Code problems.

## Setup

### 1. Get an Advent of Code Session Token

Follow the instructions at [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) to obtain your session token.

Set it as an environment variable:
```bash
export AOC_SESSION=your_session_token_here
```

### 2. Install

```bash
uv pip install git+https://github.com/spikedoanz/advent-of-code-bench.git
```

Or use directly with uvx (no installation needed):
```bash
uvx --from git+https://github.com/spikedoanz/advent-of-code-bench.git aocbench --help
```

## CLI Usage

### DIY Mode (For Human Solving)

Download Lean4 project stubs for solving AOC problems:

```bash
# Download a specific year
aocbench diy download -p . --year 2015

# Download all available years
aocbench diy download -p . --all

# Using uvx (no installation)
uvx --from git+https://github.com/spikedoanz/advent-of-code-bench.git aocbench diy download -p . --year 2015
```

This creates a directory structure:
```
./
├── 2015/
│   ├── day_01/
│   │   ├── README.md          # Problem text
│   │   ├── Main.lean          # Your solution goes here
│   │   ├── AocBench/Input.lean # Puzzle input
│   │   ├── lakefile.toml
│   │   └── lake-manifest.json
│   ├── day_02/
│   └── ...
```

### Submit Your Solution

From inside a day directory (e.g., `2015/day_01/`):

```bash
# Build and submit
aocbench diy submit -p .

# Using uvx
uvx --from git+https://github.com/spikedoanz/advent-of-code-bench.git aocbench diy submit -p .
```

This will:
1. Run `lake build` to compile your solution
2. Execute the program to get outputs
3. Submit to Advent of Code (part 1, then part 2)
4. Re-download problem text after part 1 submission to unlock part 2

### Automated Submission of Python Solutions

If you already have working Python solutions in `solutions/<year>/python/day_##.py`, you can submit multiple days in one go. First ensure your Advent of Code session token is exported:

```bash
export AOC_SESSION=your_session_token_here
```

Then run:

```bash
python -m aocb.submit --years 2016 2017
```

This command will re-run every Python solution for the requested years, cache the answers in `~/.cache/aocb/solutions.json`, and submit them using the official Advent of Code API. Useful flags:

- `--days 1 2 3` to submit only selected days.
- `--no-refresh` to reuse the cached answers without rerunning scripts.
- `--dry-run` to print the submissions without sending them (helpful for verification).

Programmatic use is also available inside Python:

```python
from aocb.submit import run_and_submit

run_and_submit(years=[2016, 2017], days=range(1, 26), dry_run=True)
```

Always double-check that each script prints the correct single-line answers expected by Advent of Code before performing a live submission.

## Acknowledgements

- https://github.com/narimiran/advent_of_code_2015
- https://github.com/narimiran/advent_of_code_2016

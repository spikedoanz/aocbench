# 2024 Advent of Code Solutions

This directory contains all 25 days of Advent of Code 2024 solutions ported to the standardized format used across this repository.

## Format

All solutions follow the standardized format:

1. **Input Reading**: Uses `INPUT_DIR` environment variable to locate input files
2. **File Naming**: Reads from `2024_XX.txt` where XX is the day (01-25)
3. **Output**: Prints two values (Part 1 and Part 2 results) using `print()` statements
4. **Structure**: Compatible with the run and submission modules in the parent directory

## Running Solutions

### Prerequisites

1. Set up the environment:
   ```bash
   cd /Users/spike/R/environments/aoc_bench
   uv sync
   ```

2. Download input files (requires AOC_SESSION token):
   ```bash
   export AOC_SESSION="your_session_token_here"
   python -m aocb.download
   ```

   Or manually place input files in `~/.cache/aocb/inputs/2024_XX.txt`

### Execute a Solution

```bash
cd /Users/spike/R/environments/aoc_bench
uv run python solutions/2024/python/day_01.py
```

### Custom Input Directory

Set the `AOC_INPUT_DIR` environment variable:

```bash
export AOC_INPUT_DIR=/path/to/your/inputs
uv run python solutions/2024/python/day_01.py
```

## Testing

Two test scripts are available in the parent `solutions/` directory:

### Format Validation
```bash
uv run python solutions/test_2024_format.py
```

Verifies:
- Correct INPUT_DIR usage
- Proper file path format (2024_XX.txt)
- Print statements for output
- Valid Python syntax

### Import Test
```bash
uv run python solutions/test_2024_import.py
```

Verifies all solutions can be imported without syntax errors.

## Dependencies

The solutions use the following external libraries:
- **networkx**: Days 5, 10, 12, 16, 18, 20, 21, 23, 24
- **numpy**: Days 14, 22
- **z3-solver**: Days 13, 24

Standard library modules used:
- `collections`, `itertools`, `functools`, `re`, `operator`, `math`

All dependencies are managed via `uv` and defined in the project's `pyproject.toml`.

## Special Cases

- **Day 17**: Uses a hardcoded program array instead of reading from an input file (as in the original solution)
- **Day 25**: Only has Part 1 (as expected for the final day of AoC)

## File Structure

```
2024/
├── python/
│   ├── day_01.py
│   ├── day_02.py
│   ├── ...
│   └── day_25.py
└── README.md
```

## Linting

Note: Some solutions have style warnings (e.g., using `l` as a variable name). These are preserved from the original solutions to maintain code consistency. Run linting with:

```bash
uvx ruff check solutions/2024/python/
```

## Original Source

These solutions were ported from `extras/adventofcode/2024/` with minimal modifications to match the repository's standardized format.

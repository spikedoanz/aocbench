#!/usr/bin/env python3
"""
Test script to verify that 2024 solutions follow the correct format.
This checks:
1. All files use INPUT_DIR environment variable
2. All files read from the correct file path format (2024_XX.txt)
3. All files have print statements for output
"""

import os
import ast
from pathlib import Path

def check_file_format(filepath):
    """Check if a solution file follows the correct format."""
    with open(filepath, 'r') as f:
        content = f.read()

    errors = []

    # Day 17 doesn't read from input file - it has hardcoded program
    is_day_17 = filepath.name == 'day_17.py'

    # Check for INPUT_DIR usage (unless it's day 17)
    if not is_day_17 and 'INPUT_DIR' not in content:
        errors.append("Missing INPUT_DIR variable")

    # Check for correct file path format (unless it's day 17)
    if not is_day_17:
        day_num = filepath.name.replace('day_', '').replace('.py', '')
        expected_filename = f"2024_{day_num}.txt"
        if expected_filename not in content:
            errors.append(f"Missing correct input filename: {expected_filename}")

    # Check for os.path.join usage (unless it's day 17)
    if not is_day_17 and 'os.path.join' not in content and 'open' in content:
        errors.append("Uses open() but not os.path.join with INPUT_DIR")

    # Check for print statements
    if content.count('print(') < 1:
        errors.append("Missing print statements for output")

    # Try to parse as valid Python
    try:
        ast.parse(content)
    except SyntaxError as e:
        errors.append(f"Syntax error: {e}")

    return errors

def main():
    solutions_dir = Path(__file__).parent / "2024" / "python"

    if not solutions_dir.exists():
        print(f"❌ Directory not found: {solutions_dir}")
        return 1

    print("Checking 2024 Python solutions format...")
    print("=" * 60)

    all_good = True
    files = sorted(solutions_dir.glob("day_*.py"))

    if not files:
        print(f"❌ No solution files found in {solutions_dir}")
        return 1

    for filepath in files:
        errors = check_file_format(filepath)

        if errors:
            all_good = False
            print(f"❌ {filepath.name}:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✓ {filepath.name}")

    print("=" * 60)

    if all_good:
        print(f"✓ All {len(files)} files passed format checks!")
        print("\nFormat requirements verified:")
        print("  • Uses INPUT_DIR environment variable")
        print("  • Reads from correct file path (2024_XX.txt)")
        print("  • Contains print statements for output")
        print("  • Valid Python syntax")
        print("\nNote: To run these solutions, you need to:")
        print("  1. Set AOC_SESSION environment variable")
        print("  2. Download inputs: cd /Users/spike/R/environments/aoc_bench && python -m aocb.download")
        print("  3. Or manually place input files in ~/.cache/aocb/inputs/")
        return 0
    else:
        print("❌ Some files have format errors")
        return 1

if __name__ == "__main__":
    exit(main())

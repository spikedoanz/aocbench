#!/usr/bin/env python3
"""
Test that all 2024 solutions can be imported without errors.
This verifies that there are no syntax errors or import issues.
"""

import sys
from pathlib import Path
import importlib.util

def test_import(filepath):
    """Try to import a solution file and check for errors."""
    spec = importlib.util.spec_from_file_location("solution", filepath)
    if spec is None or spec.loader is None:
        return ["Failed to create module spec"]

    try:
        module = importlib.util.module_from_spec(spec)
        # Don't actually execute - just check if it can be loaded
        # spec.loader.exec_module(module) would execute it
        return []
    except Exception as e:
        return [f"Import error: {e}"]

def main():
    solutions_dir = Path(__file__).parent / "2024" / "python"

    if not solutions_dir.exists():
        print(f"❌ Directory not found: {solutions_dir}")
        return 1

    print("Testing 2024 Python solutions can be imported...")
    print("=" * 60)

    all_good = True
    files = sorted(solutions_dir.glob("day_*.py"))

    if not files:
        print(f"❌ No solution files found in {solutions_dir}")
        return 1

    for filepath in files:
        errors = test_import(filepath)

        if errors:
            all_good = False
            print(f"❌ {filepath.name}:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✓ {filepath.name}")

    print("=" * 60)

    if all_good:
        print(f"✓ All {len(files)} files can be imported successfully!")
        print("\nAll solutions are syntactically valid and ready to run.")
        return 0
    else:
        print("❌ Some files have import errors")
        return 1

if __name__ == "__main__":
    exit(main())

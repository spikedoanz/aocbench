#!/usr/bin/env python3
"""AOC Bench initialization script."""

import sys
from aocb.cli import aocbench

if __name__ == "__main__":
    # Run the aocbench CLI with "init" as the command and pass through all arguments
    sys.argv.insert(1, "init")
    aocbench()

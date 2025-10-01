import os
import time
from pathlib import Path
from itertools import product

from aocd import get_data

if __name__ == "__main__":
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please get an AOC token https://github.com/wimglenn/advent-of-code-wim/issues/1"

    days  = [i for i in range(1,26)]
    years = [i for i in range(2015, 2025)]

    root_path = Path("./inputs")

    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        filepath = root_path / (str(year) + "_" + day_str + ".txt")
        if filepath.exists() and filepath.is_file() and filepath.stat().st_size > 0:
            print(f"File already downloaded, skipping {filepath}")
        else:
            with open(filepath, "w") as f:
                f.write(get_data(aoc_session, day, year))
                time.sleep(1) # rate limiting
                print(f"Downloaded to {filepath}")

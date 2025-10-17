import os
import time
from itertools import product
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from aocd import get_data
from .defaults import AVAILABLE_YEARS, PROBLEMS_HTML_PATH, INPUTS_PATH

def get_problem_html(session, year, day):
    """Fetch raw HTML for a specific problem using urllib."""
    url = f"https://adventofcode.com/{year}/day/{day}"
    req = Request(url)
    req.add_header("Cookie", f"session={session}")
    with urlopen(req) as response:
        return response.read().decode('utf-8')

def download_problems():
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please set AOC_SESSION environment variable"
    
    days = [i for i in range(1, 26)]
    years = AVAILABLE_YEARS
    root_path = PROBLEMS_HTML_PATH
    root_path.mkdir(parents = True, exist_ok=True)
    
    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        filepath = root_path / (str(year) + "_" + day_str + ".html")
        
        if filepath.exists() and filepath.is_file() and filepath.stat().st_size > 0:
            print(f"File already downloaded, skipping {filepath}")
        else:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    html_content = get_problem_html(aoc_session, year, day)
                    f.write(html_content)
                    time.sleep(1)  # rate limiting
                    print(f"Downloaded to {filepath}")
            except HTTPError as e:
                print(f"Error downloading {year} day {day}: {e}")
                # Problem might not be released yet, continue to next

def download_inputs():
    aoc_session = os.environ.get("AOC_SESSION")
    assert aoc_session, "Please get an AOC token https://github.com/wimglenn/advent-of-code-wim/issues/1"

    days  = [i for i in range(1,26)]
    years = [i for i in range(2015, 2025)]

    root_path = INPUTS_PATH
    root_path.mkdir(parents=True, exist_ok=True)

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


if __name__ == "__main__":
    download_problems()
    download_inputs()

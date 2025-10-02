from pathlib import Path

# Common paths used across the project
INPUTS_PATH = Path("./inputs")
SOLUTIONS_PATH = Path("./solutions")
PROBLEMS_HTML_PATH = Path("./problems/html")
PROBLEMS_TXT_PATH = Path("./problems/txt")
CACHE_PATH = Path("~/.cache/aocb/").expanduser()

# Common constants
AVAILABLE_YEARS = list(range(2015, 2017))

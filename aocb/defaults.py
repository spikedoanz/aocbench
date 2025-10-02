from pathlib import Path


DEFAULT_PROJECT_NAME = "AocBench"

# Cache directory (base for all downloaded data)
CACHE_PATH = Path("~/.cache/aocb/").expanduser()

# Common paths used across the project
INPUTS_PATH = CACHE_PATH / "inputs"
PROBLEMS_HTML_PATH = CACHE_PATH / "problems/html"
PROBLEMS_TXT_PATH = CACHE_PATH / "problems/txt"

# Solutions remain in project directory
SOLUTIONS_PATH = Path("./solutions")

# Common constants
AVAILABLE_YEARS = list(range(2015, 2017))

# Timeout for lake commands (in seconds)
DEFAULT_LAKE_TIMEOUT = 60

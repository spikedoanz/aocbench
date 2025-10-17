import os
import re
import time
from itertools import product
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from aocd import get_data
from .defaults import AVAILABLE_YEARS, PROBLEMS_HTML_PATH, PROBLEMS_TXT_PATH, PROMPTS_PATH, INPUTS_PATH
from .task import get_prompt

def html_to_text(html_content):
    """Convert AOC HTML problem page to plain text."""
    # Remove script and style elements
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)

    # Extract article content (main problem text)
    article_match = re.search(r'<article[^>]*class="[^"]*day-desc[^"]*"[^>]*>(.*?)</article>', html_content, re.DOTALL)
    if article_match:
        content = article_match.group(1)
    else:
        # Fallback: look for any article tag
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL)
        content = article_match.group(1) if article_match else html_content

    # Convert <p> tags to text with double newlines
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)

    # Convert <li> tags to bullet points
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1', content, flags=re.DOTALL)

    # Convert <br> and <br/> to newlines
    content = re.sub(r'<br[^>]*>', '\n', content)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Decode HTML entities
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    content = content.replace('&quot;', '"')
    content = content.replace('&apos;', "'")
    content = content.replace('&#39;', "'")

    # Clean up whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    return content

def extract_problem_parts(html_content):
    """Extract part 1 and part 2 from HTML content."""
    # Split on common part 2 indicators
    part2_indicators = [
        r'--- Part Two ---',
        r'--- Part 2 ---',
        r'=== Part Two ===',
        r'=== Part 2 ==='
    ]

    for indicator in part2_indicators:
        if indicator in html_content:
            parts = html_content.split(indicator, 1)
            part1 = html_to_text(parts[0].strip())
            part2 = html_to_text(indicator + parts[1].strip())
            return part1, part2

    # If no part 2 found, return whole as part 1
    return html_to_text(html_content), ""

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
    html_path = PROBLEMS_HTML_PATH
    txt_path = PROBLEMS_TXT_PATH
    html_path.mkdir(parents=True, exist_ok=True)
    txt_path.mkdir(parents=True, exist_ok=True)

    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        html_filepath = html_path / (str(year) + "_" + day_str + ".html")
        part1_txt_filepath = txt_path / f"{year}_{day_str}_part1.txt"
        part2_txt_filepath = txt_path / f"{year}_{day_str}_part2.txt"

        # Download HTML if it doesn't exist
        html_content = None
        if html_filepath.exists() and html_filepath.is_file() and html_filepath.stat().st_size > 0:
            print(f"HTML file already exists, skipping download for {html_filepath}")
        else:
            try:
                html_content = get_problem_html(aoc_session, year, day)
                with open(html_filepath, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Downloaded HTML to {html_filepath}")
                time.sleep(1)  # rate limiting
            except HTTPError as e:
                print(f"Error downloading {year} day {day}: {e}")
                # Problem might not be released yet, continue to next
                continue

        # Extract text from HTML if .txt files don't exist
        if (not part1_txt_filepath.exists() or part1_txt_filepath.stat().st_size == 0 or
            not part2_txt_filepath.exists() or part2_txt_filepath.stat().st_size == 0):
            try:
                if html_content is None:
                    # Load existing HTML content
                    with open(html_filepath, "r", encoding="utf-8") as f:
                        html_content = f.read()

                # Extract text from HTML
                part1_text, part2_text = extract_problem_parts(html_content)

                # Write part 1
                with open(part1_txt_filepath, "w", encoding="utf-8") as f:
                    f.write(part1_text)
                print(f"Extracted part 1 text to {part1_txt_filepath}")

                # Write part 2 if it exists
                if part2_text:
                    with open(part2_txt_filepath, "w", encoding="utf-8") as f:
                        f.write(part2_text)
                    print(f"Extracted part 2 text to {part2_txt_filepath}")

            except Exception as e:
                print(f"Error extracting text for {year} day {day}: {e}")
                continue

def generate_prompts():
    """Generate and save prompt .txt files for all available problems."""
    days = [i for i in range(1, 26)]
    years = AVAILABLE_YEARS
    prompts_path = PROMPTS_PATH
    prompts_path.mkdir(parents=True, exist_ok=True)

    for (year, day) in list(product(years, days)):
        day_str = "0" + str(day) if day < 10 else str(day)
        prompt_filepath = prompts_path / f"{year}_{day_str}.txt"

        # Skip if prompt file already exists and has content
        if prompt_filepath.exists() and prompt_filepath.stat().st_size > 0:
            print(f"Prompt file already exists, skipping {prompt_filepath}")
            continue

        try:
            prompt_text = get_prompt(year, day)
            with open(prompt_filepath, "w", encoding="utf-8") as f:
                f.write(prompt_text)
            print(f"Generated prompt to {prompt_filepath}")
        except FileNotFoundError:
            print(f"Skipping {year} day {day}: problem text not found")
        except Exception as e:
            print(f"Error generating prompt for {year} day {day}: {e}")

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

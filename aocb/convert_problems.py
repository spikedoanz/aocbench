import re
from pathlib import Path

config = {
    'html_dir': './problems/html',
    'txt_dir': './problems/txt',
    'censor_patterns': [
        (r'Your puzzle answer was.*?\.', '[ANSWER REDACTED]'),
        (r'<code>\d{10,}</code>', '<code>[REDACTED]</code>'),
    ]
}

def extract_articles(html):
    articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    return articles

def html_to_text(html):
    text = re.sub(r'<pre><code>(.*?)</code></pre>', r'\n```\n\1\n```\n', html, flags=re.DOTALL)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def apply_censorship(text, patterns):
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text

def parse_file(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    articles = extract_articles(html)
    if not articles:
        return None, None
    
    part1 = html_to_text(articles[0]) if articles else None
    part2 = html_to_text(articles[1]) if len(articles) > 1 else None
    
    if part1 and "--- Part Two ---" in part1:
        part1, part2 = None, part1
    
    if config['censor_patterns']:
        if part1:
            part1 = apply_censorship(part1, config['censor_patterns'])
        if part2:
            part2 = apply_censorship(part2, config['censor_patterns'])
    
    return part1, part2

def convert_all():
    html_path = Path(config['html_dir'])
    txt_path = Path(config['txt_dir'])
    txt_path.mkdir(parents=True, exist_ok=True)
    
    for html_file in sorted(html_path.glob('*.html')):
        part1, part2 = parse_file(html_file)
        base = html_file.stem  # e.g., "2015_24"
        
        if part1:
            with open(txt_path / f'{base}_part1.txt', 'w', encoding='utf-8') as f:
                f.write(part1)
            print(f"Created: {base}_part1.txt")
        
        if part2:
            with open(txt_path / f'{base}_part2.txt', 'w', encoding='utf-8') as f:
                f.write(part2)
            print(f"Created: {base}_part2.txt")

if __name__ == "__main__":
    convert_all()

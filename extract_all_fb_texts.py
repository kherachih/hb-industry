import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('fb_selenium.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

raw_texts = re.findall(r'"text":\s*"((?:\\.|[^"\\])*)"', html)

posts = []
for t in raw_texts:
    try:
        decoded = json.loads(f'"{t}"')
    except Exception:
        continue
    
    if any(k in decoded for k in ['HB INDUSTRY GROUP', 'paillasse', 'laboratoire', 'savoir-faire', '0775', 'hbig']):
        if len(decoded) > 50 and decoded not in posts:
            posts.append(decoded)

print(f"Found {len(posts)} distinctive post texts!")
for i, p in enumerate(posts):
    print(f"\n================ PUBLICATION {i+1} ================")
    print(p)

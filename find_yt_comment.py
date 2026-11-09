import urllib.request
import re

url = 'https://www.youtube.com/shorts/UcWTeZepXJc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Search for the pinned comment or tool name in the HTML
pinned = re.findall(r'"commentText":\s*\{\s*"runs":\s*(\[.*?\])\}', html)
if pinned:
    print("Found commentText:", pinned[0])

# Look for mentions of the specific builder
for name in ['dora', 'spline', 'vulk', 'framer', 'orbital', 'relume', 'midjourney', 'three.js']:
    m = re.findall(rf'\b{name}\b', html, re.IGNORECASE)
    if m:
        print(f"Mentioned {name}: {len(m)} times")

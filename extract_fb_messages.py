import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('temp_raw/fb_about.html', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Look for "message":{"text":"
results = []
pos = 0
key = '"message":{"text":"'
while True:
    idx = text.find(key, pos)
    if idx == -1:
        break
    start = idx + len(key)
    # find ending quote not preceded by odd number of backslashes
    p = start
    while p < len(text):
        if text[p] == '"':
            # check backslashes before it
            bs_count = 0
            b = p - 1
            while b >= start and text[b] == '\\':
                bs_count += 1
                b -= 1
            if bs_count % 2 == 0:
                break
        p += 1
    msg_str = text[start:p]
    try:
        decoded = json.loads('"' + msg_str + '"')
    except Exception:
        try:
            decoded = msg_str.encode('utf-8').decode('unicode-escape')
        except Exception:
            decoded = msg_str
    
    results.append(decoded)
    pos = p + 1

print(f"Total raw messages: {len(results)}")
unique_posts = []
seen = set()
for r in results:
    cleaned = r.strip()
    if len(cleaned) > 25 and cleaned not in seen:
        seen.add(cleaned)
        unique_posts.append(cleaned)

print(f"Unique posts: {len(unique_posts)}")
for i, p in enumerate(unique_posts):
    print(f"\n==================== POST {i+1} ====================")
    print(p)

with open('facebook_posts_extracted_all.json', 'w', encoding='utf-8') as f:
    json.dump(unique_posts, f, indent=2, ensure_ascii=False)

import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('fb_selenium.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# In Facebook's HTML, text is stored in "text":"..." inside JSON
pattern = r'"text":\s*"([^"]{25,1200})"'
matches = re.findall(pattern, html)
print(f"Total potential text matches: {len(matches)}")

seen = set()
posts = []

keywords = [
    'laboratoire', 'projet', 'excellence', 'qualité', 'mobilier',
    'paillasse', 'sorbonne', 'armoire', 'client', 'conception',
    'batna', 'contact', 'hbig', '0775', '0550', 'rayonnage',
    'sécurité', 'fabrication', 'devis', 'espace', 'hbig.dz'
]

for m in matches:
    # unescape unicode sequences like \u00e9 -> é
    try:
        decoded = m.encode('utf-8').decode('unicode_escape')
    except Exception:
        decoded = m
    
    decoded_clean = decoded.replace('\\n', '\n').strip()
    if len(decoded_clean) < 30:
        continue
    if decoded_clean in seen:
        continue
    
    # Check if relevant
    if any(k in decoded_clean.lower() for k in keywords):
        seen.add(decoded_clean)
        posts.append(decoded_clean)

print(f"Extracted {len(posts)} relevant posts/messages from Facebook!")
for i, p in enumerate(posts):
    print(f"\n--- [PUBLICATION {i+1}] ---")
    print(p)

with open('fb_extracted_posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

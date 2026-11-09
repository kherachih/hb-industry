import sys
import json
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# 1. Parse About Page
print("--- PARSING ABOUT PAGE ---")
with open('fb_about.html', 'r', encoding='utf-8', errors='ignore') as f:
    about_soup = BeautifulSoup(f.read(), 'html.parser')

about_texts = []
for span in about_soup.find_all(['span', 'div', 'p']):
    t = span.get_text(strip=True)
    if t and len(t) > 3 and len(t) < 400:
        if any(w in t.lower() for w in ['batna', 'gaous', 'lehnancha', 'email', 'téléphone', 'phone', 'contact', '0775', '0550', 'matériel', 'fabricant', 'mobilier', 'laboratoire', 'création', 'abonnés', 'followers', 'suivi', 'site web', 'hbig', 'eurl']):
            if t not in about_texts:
                about_texts.append(t)

for t in about_texts[:30]:
    print(">", t)

# 2. Parse Photos
print("\n--- PARSING PHOTOS ---")
with open('fb_photos.html', 'r', encoding='utf-8', errors='ignore') as f:
    photos_html = f.read()

# Extract all image links from photos page
img_urls = set()
for m in re.finditer(r'https://scontent[^\s"\'\\]+?fbcdn\.net[^\s"\'\\]+', photos_html):
    url = m.group(0).replace('&amp;', '&').replace('\\/', '/')
    # Exclude emojis or tiny icons
    if 'emoji.php' not in url and 'rsrc.php' not in url:
        img_urls.add(url)

print(f"Found {len(img_urls)} photo URLs from Facebook Photos page!")

with open('fb_photo_urls.json', 'w', encoding='utf-8') as f:
    json.dump(list(img_urls), f, indent=2)

print("Saved fb_photo_urls.json")

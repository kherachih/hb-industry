import sys
import json
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('fb_selenium.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("=== META TAGS ===")
for meta in soup.find_all('meta'):
    p = meta.get('property') or meta.get('name')
    c = meta.get('content')
    if p and c:
        print(f"{p} = {c}")

print("\n=== IMAGES (fbcdn / scontent) ===")
images = []
for img in soup.find_all('img'):
    src = img.get('src')
    alt = img.get('alt', '')
    if src and ('fbcdn.net' in src or 'scontent' in src):
        images.append({'src': src, 'alt': alt})

print(f"Total matching images found: {len(images)}")
for i, img in enumerate(images[:20]):
    print(f"[{i+1}] ALT: {img['alt']} | URL: {img['src'][:100]}...")

# Also find background-image styles or image URLs anywhere in HTML
all_fbcdn = set(re.findall(r'https://[^\s"\'\\]+?fbcdn\.net[^\s"\'\\]+', html))
all_scontent = set(re.findall(r'https://[^\s"\'\\]+?scontent[^\s"\'\\]+', html))
combined = all_fbcdn.union(all_scontent)
print(f"\nRegex total image URLs found: {len(combined)}")

# Clean up URLs (replace &amp; with &)
clean_urls = set()
for u in combined:
    u_clean = u.replace('&amp;', '&').replace('\\/', '/')
    # Filter out small icons or tracking pixels if needed, or keep all
    clean_urls.add(u_clean)

print(f"Clean URLs: {len(clean_urls)}")

# Check for JSON payloads in script tags (Facebook stores page data in Relay/GraphQL script tags)
script_data = []
for script in soup.find_all('script'):
    content = script.string or ''
    if 'requireGraphQL' in content or 'scheduled_posts' in content or 'Hb industry group' in content or 'hbig.dz' in content:
        script_data.append(content[:200])

print(f"\nScripts mentioning brand: {len(script_data)}")

with open('fb_extracted_images.json', 'w', encoding='utf-8') as f:
    json.dump(list(clean_urls), f, indent=2)

print("Saved fb_extracted_images.json")

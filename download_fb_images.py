import json
import re
import os
import urllib.request
from PIL import Image

all_urls = set()

# Load from fb_extracted_images.json
if os.path.exists('fb_extracted_images.json'):
    with open('fb_extracted_images.json', 'r') as f:
        all_urls.update(json.load(f))

# Load from fb_photo_urls.json
if os.path.exists('fb_photo_urls.json'):
    with open('fb_photo_urls.json', 'r') as f:
        all_urls.update(json.load(f))

# Regex on fb_photos.html and fb_about.html
for fname in ['fb_photos.html', 'fb_about.html', 'fb_selenium.html']:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for m in re.finditer(r'https://scontent[^\s"\'\\]+?fbcdn\.net[^\s"\'\\]+', content):
                u = m.group(0).replace('&amp;', '&').replace('\\/', '/')
                all_urls.add(u)

print(f"Total candidate scontent URLs collected: {len(all_urls)}")

# Filter out icons, emojis, tracking pixels, and tiny thumbnails
filtered_urls = set()
for u in all_urls:
    if any(bad in u for bad in ['rsrc.php', 'emoji.php', 'cp3', '16x16', '24x24', '32x32']):
        continue
    # Keep only image urls
    if any(pat in u for pat in ['/v/t39.', '/v/t1.', '/p', 'scontent']):
        filtered_urls.add(u)

print(f"Filtered candidate photo URLs: {len(filtered_urls)}")

os.makedirs('assets/facebook_photos', exist_ok=True)

downloaded = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

count = 0
for idx, u in enumerate(filtered_urls):
    filename = f"fb_img_{idx+1:03d}.jpg"
    filepath = os.path.join('assets/facebook_photos', filename)
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 5000:  # Skip tiny files
                with open(filepath, 'wb') as out_f:
                    out_f.write(data)
                try:
                    im = Image.open(filepath)
                    w, h = im.size
                    if w >= 150 and h >= 150:
                        downloaded.append({
                            'filename': filename,
                            'path': filepath,
                            'width': w,
                            'height': h,
                            'format': im.format,
                            'size_bytes': len(data),
                            'url': u
                        })
                        count += 1
                        print(f"[{count}] Saved {filename} ({w}x{h}, {len(data)//1024} KB)")
                    else:
                        os.remove(filepath)
                except Exception:
                    if os.path.exists(filepath):
                        os.remove(filepath)
    except Exception as e:
        # Ignore failed individual requests
        pass

print(f"\nSuccessfully downloaded and validated {len(downloaded)} high-quality Facebook photos!")

with open('downloaded_fb_photos.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, indent=2)

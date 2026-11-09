import sys
import time
import json
import re
import os
import urllib.request
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

annonces = [
    ("44297578", "paillasse_scolaire_eleve"),
    ("38711646", "paillasse_scolaire_table_scientifique"),
    ("45694867", "paillasse_laboratoire_bureautique"),
    ("41275177", "paillasse_laboratoire_centrale_murale"),
    ("38700804", "armoire_securite_coupe_feu"),
    ("38711544", "armoire_ventilee_produits_chimiques")
]

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)

os.makedirs('assets/products', exist_ok=True)
all_products_details = []

for aid, slug in annonces:
    url = f"https://www.ouedkniss.com/store/24762/hb-industry-group/annonce/{aid}"
    print(f"\nVisiting: {slug} ({aid})...")
    try:
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract title
        title_el = soup.find('h1')
        title = title_el.get_text(strip=True) if title_el else slug
        
        # Extract description and specs
        desc_el = soup.find('div', class_=lambda c: c and 'description' in c.lower()) or soup.find('div', attrs={'itemprop': 'description'})
        desc_text = desc_el.get_text('\n', strip=True) if desc_el else ''
        
        # Also grab all text inside paragraphs / article
        all_paragraphs = [p.get_text(strip=True) for p in soup.find_all(['p', 'li']) if len(p.get_text(strip=True)) > 20]
        
        # Extract all image hashes from page
        img_hashes = set(re.findall(r'/medias/announcements/images/0gMPZX/([a-zA-Z0-9_-]+\.jpg)', driver.page_source))
        print(f"  Found title: {title}")
        print(f"  Found {len(img_hashes)} photo hashes: {list(img_hashes)}")
        
        downloaded_imgs = []
        for h_idx, img_name in enumerate(img_hashes):
            high_res_url = f"https://cdn7.ouedkniss.com/1600/medias/announcements/images/0gMPZX/{img_name}"
            # fallback to 800 if 1600 fails
            save_filename = f"{slug}_{h_idx+1}.jpg"
            save_path = os.path.join('assets/products', save_filename)
            
            try:
                req = urllib.request.Request(high_res_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    with open(save_path, 'wb') as f:
                        f.write(resp.read())
            except Exception:
                fallback_url = f"https://cdn7.ouedkniss.com/800/medias/announcements/images/0gMPZX/{img_name}"
                req = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    with open(save_path, 'wb') as f:
                        f.write(resp.read())
            
            if os.path.exists(save_path):
                im = Image.open(save_path)
                downloaded_imgs.append({
                    'filename': save_filename,
                    'path': save_path,
                    'resolution': f"{im.size[0]}x{im.size[1]}",
                    'size_kb': os.path.getsize(save_path) // 1024
                })
                print(f"  Downloaded: {save_filename} ({im.size[0]}x{im.size[1]})")

        all_products_details.append({
            'id': aid,
            'slug': slug,
            'title': title,
            'description': desc_text,
            'paragraphs': all_paragraphs,
            'images': downloaded_imgs
        })
    except Exception as e:
        print(f"  Error scraping {aid}: {e}")

driver.quit()

with open('catalog_full_details.json', 'w', encoding='utf-8') as f:
    json.dump(all_products_details, f, indent=2, ensure_ascii=False)

print("\nSaved catalog_full_details.json successfully!")

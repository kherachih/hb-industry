import sys
import json
import re
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

annonces = [
    ("44297578", "paillasse-scolaire-pour-eleve"),
    ("38711646", "paillasse-scolaire-table-scientifique"),
    ("45694867", "paillasse-de-laboratoire-et-bureautique"),
    ("41275177", "paillasse-de-laboratoires"),
    ("38700804", "armoire-de-securite-coupe-feu"),
    ("38711544", "armoire-ventile-armoire-de-stockage-produit-chemique-inflamable")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

products_data = []

for aid, slug in annonces:
    url = f"https://www.ouedkniss.com/store/24762/hb-industry-group/annonce/{aid}"
    print(f"Fetching {aid} - {slug}...")
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Extract meta tags
            og_title = soup.find('meta', property='og:title')
            og_desc = soup.find('meta', property='og:description')
            og_img = soup.find('meta', property='og:image')
            
            title = og_title['content'] if og_title else slug
            desc = og_desc['content'] if og_desc else ''
            img = og_img['content'] if og_img else ''
            
            # Find all images on the page related to this item
            page_imgs = set()
            if img:
                page_imgs.add(img)
            for m in re.finditer(r'https://cdn\d?\.ouedkniss\.com/[^\s"\'\\]+?\.(?:jpg|jpeg|png|webp)', r.text):
                img_url = m.group(0)
                if 'favicon' not in img_url and 'logo' not in img_url and 'icon' not in img_url:
                    # Prefer high-res version if url contains /400/ or /800/
                    high_res = img_url.replace('/400/', '/original/').replace('/800/', '/original/')
                    page_imgs.add(high_res)
                    page_imgs.add(img_url)

            # Look for JSON payload in Nuxt script
            nuxt_data = None
            for s in soup.find_all('script'):
                if s.string and ('description' in s.string or 'specification' in s.string):
                    # extract description texts
                    m_desc = re.search(r'"description":\s*"([^"]+)"', s.string)
                    if m_desc:
                        desc = m_desc.group(1).encode('utf-8').decode('unicode_escape', errors='ignore')
            
            p_info = {
                'id': aid,
                'slug': slug,
                'url': url,
                'title': title,
                'description': desc,
                'main_image': img,
                'images': list(page_imgs)
            }
            products_data.append(p_info)
            print(f"  -> Title: {title}")
            print(f"  -> Desc: {desc[:100]}...")
            print(f"  -> Images found: {len(page_imgs)}")
        else:
            print(f"  -> Status code: {r.status_code}")
    except Exception as e:
        print(f"  -> Error: {e}")

with open('ouedkniss_products.json', 'w', encoding='utf-8') as f:
    json.dump(products_data, f, indent=2, ensure_ascii=False)

print(f"\nDone! Extracted {len(products_data)} products to ouedkniss_products.json")

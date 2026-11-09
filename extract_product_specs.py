import sys
import time
import json
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

detailed_products = []

for aid, slug in annonces:
    url = f"https://www.ouedkniss.com/store/24762/hb-industry-group/annonce/{aid}"
    print(f"Reading specs for {slug} ({aid})...")
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        title_el = soup.find('h1')
        title = title_el.get_text(strip=True) if title_el else slug
        
        # Grab all texts inside main content
        texts = []
        for tag in soup.find_all(['p', 'span', 'li', 'div', 'td']):
            t = tag.get_text(' ', strip=True)
            if len(t) > 20 and not any(bad in t.lower() for bad in ['javascript', 'ouedkniss', 'cookie', 'connecter', 'google', 'signaler', 'partager']):
                if t not in texts:
                    texts.append(t)

        detailed_products.append({
            'id': aid,
            'slug': slug,
            'title': title,
            'url': url,
            'content_snippets': texts[:15]
        })
    except Exception as e:
        print(f"Error on {slug}: {e}")

driver.quit()

with open('products_specifications.json', 'w', encoding='utf-8') as f:
    json.dump(detailed_products, f, indent=2, ensure_ascii=False)

print("Saved products_specifications.json!")

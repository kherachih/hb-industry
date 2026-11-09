import os
import sys
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--force-device-scale-factor=1')
# set exact canvas size: 1080x1350
options.add_argument('--window-size=1080,1350')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)

files = [
    ('fiches_produits_commerciales/social_ad_01_douche_cinematic.html', 'fiches_produits_commerciales/SOCIAL_AD_01_DOUCHE_CINEMATIC.png'),
    ('fiches_produits_commerciales/social_ad_02_paillasse_cinematic.html', 'fiches_produits_commerciales/SOCIAL_AD_02_PAILLASSE_CINEMATIC.png')
]

for html_file, out_png in files:
    abs_path = os.path.abspath(html_file).replace('\\', '/')
    url = f"file:///{abs_path}"
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(2.5)  # Wait for Google Fonts (Syne, Plus Jakarta Sans, JetBrains Mono)
    
    try:
        canvas = driver.find_element("css selector", ".ad-canvas")
        canvas.screenshot(out_png)
        print(f"Saved element screenshot: {out_png}")
    except Exception as e:
        print(f"Canvas capture fallback: {e}")
        driver.save_screenshot(out_png)
    
    if os.path.exists(out_png):
        im = Image.open(out_png)
        print(f"Image {out_png} resolution: {im.size}, format: {im.format}")

driver.quit()
print("\nSocial ads rendered successfully!")

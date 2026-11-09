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
# set exact canvas size: 1200x1200
options.add_argument('--window-size=1200,1200')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)

files = [
    ('fiches_produits_commerciales/fiche_01_douches_securite.html', 'fiches_produits_commerciales/EXEMPLE_01_DOUCHES_SECURITE_HBIG.png'),
    ('fiches_produits_commerciales/fiche_02_paillasse_centrale.html', 'fiches_produits_commerciales/EXEMPLE_02_PAILLASSE_CENTRALE_HBIG.png')
]

for html_file, out_png in files:
    abs_path = os.path.abspath(html_file).replace('\\', '/')
    url = f"file:///{abs_path}"
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(2)  # Wait for web fonts (Plus Jakarta Sans, Syne) and images
    
    # Locate .flyer-canvas and take element screenshot for exact 1200x1200 crop
    try:
        canvas = driver.find_element("css selector", ".flyer-canvas")
        canvas.screenshot(out_png)
        print(f"Saved element screenshot: {out_png}")
    except Exception as e:
        print(f"Canvas element capture error: {e}, capturing window...")
        driver.save_screenshot(out_png)
    
    # Verify image dimensions
    if os.path.exists(out_png):
        im = Image.open(out_png)
        print(f"Image {out_png} resolution: {im.size}, format: {im.format}")

driver.quit()
print("\nAll flyers rendered successfully!")

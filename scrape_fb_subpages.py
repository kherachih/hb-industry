import os
import sys
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)

def get_page_info():
    results = {}
    
    # 1. Fetch About page
    print("Fetching About page...")
    try:
        driver.get('https://www.facebook.com/hbig.dz/about')
        time.sleep(4)
        about_html = driver.page_source
        with open('fb_about.html', 'w', encoding='utf-8') as f:
            f.write(about_html)
        print("About page saved. Size:", len(about_html))
    except Exception as e:
        print("Error fetching about:", e)

    # 2. Fetch Photos page
    print("Fetching Photos page...")
    try:
        driver.get('https://www.facebook.com/hbig.dz/photos')
        time.sleep(4)
        
        # Scroll multiple times to trigger lazy loading of photos
        for scroll_i in range(8):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            print(f"Scrolled {scroll_i + 1}/8...")
            
        photos_html = driver.page_source
        with open('fb_photos.html', 'w', encoding='utf-8') as f:
            f.write(photos_html)
        print("Photos page saved. Size:", len(photos_html))
    except Exception as e:
        print("Error fetching photos:", e)

    driver.quit()

if __name__ == '__main__':
    get_page_info()

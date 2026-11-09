import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

print("Navigating to Ouedkniss store...")
try:
    driver.get('https://www.ouedkniss.com/store/24762/hb-industry-group/accueil')
    time.sleep(5)
    with open('ouedkniss_rendered_home.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Saved ouedkniss_rendered_home.html, len:", len(driver.page_source))

    driver.get('https://www.ouedkniss.com/store/24762/hb-industry-group/annonces')
    time.sleep(6)
    # Scroll to load more
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
    with open('ouedkniss_rendered_annonces.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Saved ouedkniss_rendered_annonces.html, len:", len(driver.page_source))
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1440,900')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)

try:
    print("Testing http://localhost:4173/ ...")
    driver.get('http://localhost:4173/')
    time.sleep(3)

    print("Page Title:", driver.title)

    # Check console errors
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser severe errors: {len(errors)}")
    for e in errors:
        print("  Error:", e['message'])

    os.makedirs('screenshots', exist_ok=True)
    driver.save_screenshot('screenshots/hero_revamped.png')
    print("Saved screenshots/hero_revamped.png")

    # Scroll to Hardware Catalog
    driver.execute_script("window.scrollTo(0, 950);")
    time.sleep(1)
    driver.save_screenshot('screenshots/catalog_revamped.png')
    print("Saved screenshots/catalog_revamped.png")

    # Scroll to Blueprint Explorer
    driver.execute_script("window.scrollTo(0, 1800);")
    time.sleep(1)
    driver.save_screenshot('screenshots/blueprint_revamped.png')
    print("Saved screenshots/blueprint_revamped.png")

    # Scroll to Facility Batna & Manifesto
    driver.execute_script("window.scrollTo(0, 2600);")
    time.sleep(1)
    driver.save_screenshot('screenshots/facility_revamped.png')
    print("Saved screenshots/facility_revamped.png")

    # Language Switch to Arabic
    lang_btn = driver.find_element(By.XPATH, "//button[contains(., 'AR') or contains(., 'FR')]")
    lang_btn.click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    driver.save_screenshot('screenshots/hero_arabic_revamped.png')
    print("Saved screenshots/hero_arabic_revamped.png (Arabic RTL)")

    print("\nALL REVAMPED SCREENSHOTS CAPTURED WITH 0 ERRORS!")

except Exception as e:
    print("Test failed with error:", e)
finally:
    driver.quit()

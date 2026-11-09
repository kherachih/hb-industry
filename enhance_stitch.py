import re
from bs4 import BeautifulSoup

with open('stitch_screen.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 1. Update Logo in header
# Find the first logo container or img
logo_img = soup.find('img', alt=re.compile(r'logo|badge|lead', re.I))
if logo_img:
    logo_img['src'] = '/assets/logo/ouedkniss_logo.jpg'
    logo_img['class'] = logo_img.get('class', []) + ['rounded-sm', 'border', 'border-primary/40']

# 2. Update Hero Visual with real central lab bench
hero_img = soup.find('img', alt=re.compile(r'hero|installation|bench|paillasse', re.I))
# Look for any main image in section 1
hero_sec = soup.find('section', id='hero') or soup.find_all('section')[0]
for img in hero_sec.find_all('img'):
    img['src'] = '/assets/products/paillasse_laboratoire_centrale_murale_01.jpg'
    img['alt'] = 'Paillasse Centrale de Laboratoire HB Industry Group'

# 3. Update Product Images in catalogue section
cat_sec = soup.find('section', id='catalogue') or (soup.find_all('section')[2] if len(soup.find_all('section')) > 2 else None)
if cat_sec:
    product_images = [
        ('/assets/products/paillasse_laboratoire_centrale_murale_01.jpg', 'Série TITAN-LAB 2400'),
        ('/assets/products/armoire_securite_coupe_feu_01.jpg', 'Série PYRO-GUARD 90'),
        ('/assets/products/armoire_ventilee_produits_chimiques_01.jpg', 'Série VORTEX-CHEM 1500'),
        ('/assets/products/paillasse_scolaire_table_scientifique_01.jpg', 'Série ACADÉMIE-PRO')
    ]
    cards = cat_sec.find_all('article') or cat_sec.find_all('div', class_=re.compile(r'bg-surface-container|industrial-card|border', re.I))
    # inject into cards
    card_idx = 0
    for card in cards:
        img = card.find('img')
        if img and card_idx < len(product_images):
            img['src'] = product_images[card_idx][0]
            img['alt'] = product_images[card_idx][1]
            img['class'] = img.get('class', []) + ['object-cover', 'w-full', 'h-full']
            card_idx += 1

# 4. Update Factory / Usine Batna section images
factory_sec = soup.find('section', id='usine-batna') or (soup.find_all('section')[3] if len(soup.find_all('section')) > 3 else None)
if factory_sec:
    f_imgs = factory_sec.find_all('img')
    if f_imgs:
        f_imgs[0]['src'] = '/assets/facebook_photos/fb_img_002.jpg'
        f_imgs[0]['alt'] = 'Atelier de soudure et thermolaquage Batna'
    if len(f_imgs) > 1:
        f_imgs[1]['src'] = '/assets/facebook_photos/fb_img_022.jpg'

# 5. Update Deployments / Real Projects images
dep_sec = soup.find('section', id='deploiements') or (soup.find_all('section')[4] if len(soup.find_all('section')) > 4 else None)
if dep_sec:
    dep_imgs = dep_sec.find_all('img')
    real_photos = [
        '/assets/facebook_photos/fb_img_015.jpg',
        '/assets/facebook_photos/fb_img_040.jpg',
        '/assets/facebook_photos/fb_img_032.jpg',
        '/assets/facebook_photos/fb_img_028.jpg'
    ]
    for i, img in enumerate(dep_imgs):
        if i < len(real_photos):
            img['src'] = real_photos[i]

# Save enhanced version
enhanced_html = str(soup)

# Write to both website/dist and root
with open('website/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(enhanced_html)

with open('stitch_enhanced.html', 'w', encoding='utf-8') as f:
    f.write(enhanced_html)

print("Saved enhanced Stitch design to website/dist/index.html and stitch_enhanced.html!")

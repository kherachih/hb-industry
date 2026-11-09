import os
import sys
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('fiches_produits_commerciales', exist_ok=True)

html_code = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>HB Industry Group - Affiche Commerciale Master</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Syne:wght@700;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1200px;
    height: 1200px;
    overflow: hidden;
    background: #0b1523;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1e293b;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .poster-canvas {
    position: relative;
    width: 1200px;
    height: 1200px;
    background: #ffffff;
    overflow: hidden;
  }

  /* Full background photo featuring Paillasses + HBIG Boxes + Showers */
  .bg-scene {
    position: absolute;
    top: 0;
    right: 0;
    width: 1200px;
    height: 1110px;
    object-fit: cover;
    object-position: right 65% center;
    z-index: 1;
  }

  /* Elegant translucent glass fade on the left, letting paillasses show through */
  .glass-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 60%;
    height: 1110px;
    background: linear-gradient(90deg, 
      rgba(255, 255, 255, 0.94) 0%, 
      rgba(255, 255, 255, 0.88) 50%, 
      rgba(255, 255, 255, 0.65) 75%, 
      rgba(255, 255, 255, 0.0) 100%);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 2;
  }

  /* Header Box */
  .header-box {
    position: absolute;
    top: 45px;
    left: 55px;
    z-index: 10;
  }
  .brand-header-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 22px;
  }
  .brand-logo-img {
    height: 58px;
    width: auto;
    object-fit: contain;
  }
  .brand-names {
    display: flex;
    flex-direction: column;
  }
  .brand-corp {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #0a6aa5;
    letter-spacing: 0.5px;
    line-height: 1.1;
  }
  .brand-motto {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* Hook & Main Titles */
  .hook-lead {
    font-size: 32px;
    font-weight: 900;
    line-height: 1.15;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }
  .hook-lead span {
    color: #e05638;
  }
  .product-main-name {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #0a6aa5;
    letter-spacing: -0.3px;
    margin-bottom: 28px;
  }

  /* Feature Bullets with Icons */
  .features-grid {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 480px;
  }
  .feature-pill-row {
    display: flex;
    align-items: center;
    gap: 15px;
    background: rgba(255, 255, 255, 0.70);
    padding: 6px 14px 6px 8px;
    border-radius: 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid rgba(255,255,255,0.8);
  }
  .feat-icon-circle {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f97316 0%, #e05638 100%);
    box-shadow: 0 4px 10px rgba(224, 86, 56, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .feat-icon-circle svg {
    width: 20px;
    height: 20px;
    fill: #ffffff;
  }
  .feat-caption {
    font-size: 14.5px;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.3;
  }

  /* Badges: Top Right Color Ribbons */
  .swatches-panel {
    position: absolute;
    top: 45px;
    right: 55px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 7px;
  }
  .swatches-title {
    font-size: 13px;
    font-style: italic;
    font-weight: 800;
    color: #0a6aa5;
    background: rgba(255, 255, 255, 0.95);
    padding: 6px 16px;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 4px;
  }
  .swatch-ribbon {
    width: 140px;
    padding: 7px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    letter-spacing: 1px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.18);
    clip-path: polygon(0% 0%, 100% 0%, 93% 50%, 100% 100%, 0% 100%, 5% 50%);
  }
  .rib-green { background: linear-gradient(90deg, #15803d, #22c55e); }
  .rib-yellow { background: linear-gradient(90deg, #ca8a04, #eab308); color: #0f172a; }
  .rib-red { background: linear-gradient(90deg, #b91c1c, #ef4444); }
  .rib-inox { background: linear-gradient(90deg, #64748b, #94a3b8); }

  /* Inset Focus (Inox & Emballage) */
  .focus-cards-row {
    position: absolute;
    bottom: 122px;
    left: 55px;
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .inox-card {
    display: flex;
    align-items: center;
    background: #0f172a;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.15);
  }
  .inox-thumb {
    width: 82px;
    height: 68px;
    object-fit: cover;
  }
  .inox-details {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 18px 10px 14px;
  }
  .inox-check-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #22c55e;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .inox-check-circle svg {
    width: 16px;
    height: 16px;
    fill: #ffffff;
  }
  .inox-text {
    font-size: 12px;
    font-weight: 700;
    color: #e2e8f0;
  }
  .inox-text span {
    font-size: 16px;
    font-weight: 900;
    color: #38bdf8;
    display: block;
  }

  .factory-stock-badge {
    background: rgba(10, 106, 165, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 12px 18px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .factory-stock-sub {
    font-size: 10.5px;
    font-weight: 700;
    color: #bae6fd;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .factory-stock-main {
    font-family: 'Syne', sans-serif;
    font-size: 14.5px;
    font-weight: 800;
    letter-spacing: 0.3px;
  }

  /* Sectors Bar (Bottom Right) */
  .sectors-panel {
    position: absolute;
    bottom: 122px;
    right: 55px;
    z-index: 10;
    display: flex;
    gap: 20px;
    align-items: center;
    background: rgba(255, 255, 255, 0.94);
    padding: 9px 22px;
    border-radius: 35px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  }
  .sector-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .sector-node-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #f1f5f9;
    border: 1.5px solid #0a6aa5;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .sector-node-circle svg {
    width: 16px;
    height: 16px;
    fill: #0a6aa5;
  }
  .sector-node-caption {
    font-size: 9.5px;
    font-weight: 800;
    color: #334155;
    text-transform: uppercase;
  }

  /* Bottom Contact Bar */
  .footer-strip {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 1200px;
    height: 94px;
    background: #091a2c;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 55px;
  }
  .footer-contacts-wrap {
    display: flex;
    align-items: center;
    gap: 36px;
  }
  .footer-contact-item {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .footer-contact-bubble {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #e05638;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .footer-contact-bubble svg {
    width: 20px;
    height: 20px;
    fill: #ffffff;
  }
  .footer-contact-num {
    font-size: 17.5px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.5px;
  }

  /* Orange Angled Brand Block */
  .footer-orange-slice {
    height: 94px;
    background: linear-gradient(135deg, #f97316 0%, #e05638 100%);
    clip-path: polygon(14% 0%, 100% 0%, 100% 100%, 0% 100%);
    padding: 0 45px 0 65px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
  }
  .footer-slice-title {
    font-family: 'Syne', sans-serif;
    font-size: 21px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.5px;
  }
  .footer-slice-motto {
    font-size: 11.5px;
    font-weight: 700;
    color: #fef08a;
    letter-spacing: 0.5px;
  }
</style>
</head>
<body>
<div class="poster-canvas">
  <!-- 3D Scene: Showers (Foreground) + HBIG Boxes (Midground) + Paillasses Lab (Background) -->
  <img class="bg-scene" src="../assets/generated_products/hbig_catalog_v2_with_paillasses_and_boxes.jpg" alt="Atelier HBIG - Paillasses et Douches de Sécurité">

  <!-- Translucent Glass Fade on Left -->
  <div class="glass-backdrop"></div>

  <!-- Header -->
  <div class="header-box">
    <div class="brand-header-row">
      <img class="brand-logo-img" src="../assets/logo/hbig_logo_clean.png" alt="HBIG Logo">
      <div class="brand-names">
        <div class="brand-corp">HB INDUSTRY GROUP</div>
        <div class="brand-motto">Mobilier & Équipements Spécialisés Pour Laboratoires</div>
      </div>
    </div>
    <div class="hook-lead">Votre sécurité <span>notre priorité</span></div>
    <div class="product-main-name">Douches de sécurité et lave-yeux</div>

    <!-- 5 Feature Points with Pills -->
    <div class="features-grid">
      <div class="feature-pill-row">
        <div class="feat-icon-circle">
          <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
        </div>
        <div class="feat-caption">Répond aux normes de sécurité EN 15154</div>
      </div>
      <div class="feature-pill-row">
        <div class="feat-icon-circle">
          <svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
        </div>
        <div class="feat-caption">Construction robuste et durable</div>
      </div>
      <div class="feature-pill-row">
        <div class="feat-icon-circle">
          <svg viewBox="0 0 24 24"><path d="M12 2c-5.33 4.55-8 8.48-8 11.8 0 4.98 3.8 8.2 8 8.2s8-3.22 8-8.2c0-3.32-2.67-7.25-8-11.8zm0 18c-3.35 0-6-2.57-6-6.2 0-2.34 1.95-5.44 6-9.14 4.05 3.7 6 6.79 6 9.14 0 3.63-2.65 6.2-6 6.2z"/></svg>
        </div>
        <div class="feat-caption">Activation rapide et facile</div>
      </div>
      <div class="feature-pill-row">
        <div class="feat-icon-circle">
          <svg viewBox="0 0 24 24"><path d="M4 10v7h3v-7H4zm6 0v7h3v-7h-3zM2 22h19v-3H2v3zm14-12v7h3v-7h-3zm-5-7L2 6v2h19V3l-10-5z"/></svg>
        </div>
        <div class="feat-caption">Idéal pour laboratoires, industries & sites sensibles</div>
      </div>
      <div class="feature-pill-row">
        <div class="feat-icon-circle">
          <svg viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>
        </div>
        <div class="feat-caption">Installation simple et fiable</div>
      </div>
    </div>
  </div>

  <!-- Swatches Stack -->
  <div class="swatches-panel">
    <div class="swatches-title">Disponible en plusieurs couleurs</div>
    <div class="swatch-ribbon rib-green">VERT</div>
    <div class="swatch-ribbon rib-yellow">JAUNE</div>
    <div class="swatch-ribbon rib-red">ROUGE</div>
    <div class="swatch-ribbon rib-inox">INOX</div>
  </div>

  <!-- Inset & Stock Badges -->
  <div class="focus-cards-row">
    <div class="inox-card">
      <img class="inox-thumb" src="../assets/generated_products/inset_inox_sample.jpg" alt="Inox Macro">
      <div class="inox-details">
        <div class="inox-check-circle">
          <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </div>
        <div class="inox-text">
          Également disponible en
          <span>INOX 316L</span>
        </div>
      </div>
    </div>

    <!-- Packaging & Stock Badge -->
    <div class="factory-stock-badge">
      <div class="factory-stock-sub">Conditionnement d'Origine</div>
      <div class="factory-stock-main">📦 Cartons Certifiés HBIG en Stock</div>
    </div>
  </div>

  <!-- Sectors Panel -->
  <div class="sectors-panel">
    <div class="sector-node">
      <div class="sector-node-circle"><svg viewBox="0 0 24 24"><path d="M19 19H5V8h14m-3-5v2H8V3H6v2H5c-1.11 0-2 .89-2 2v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3h-2z"/></svg></div>
      <div class="sector-node-caption">Laboratoires</div>
    </div>
    <div class="sector-node">
      <div class="sector-node-circle"><svg viewBox="0 0 24 24"><path d="M12 3L2 12h3v8h14v-8h3L12 3zm1 15h-2v-4h2v4zm0-6h-2v-2h2v2z"/></svg></div>
      <div class="sector-node-caption">Industrie</div>
    </div>
    <div class="sector-node">
      <div class="sector-node-circle"><svg viewBox="0 0 24 24"><path d="M6 3h12v2H6V3zm11 6V7H7v2c0 2.76 2.24 5 5 5s5-2.24 5-5zm-5 7c-3.87 0-7 3.13-7 7h14c0-3.87-3.13-7-7-7z"/></svg></div>
      <div class="sector-node-caption">Pharmacie</div>
    </div>
    <div class="sector-node">
      <div class="sector-node-circle"><svg viewBox="0 0 24 24"><path d="M19.8 18.4L14 10.7V5h1V3H9v2h1v5.7L4.2 18.4c-.6.8-.7 1.8-.3 2.7.4.9 1.2 1.4 2.2 1.4h11.8c1 0 1.8-.5 2.2-1.4.4-.9.3-1.9-.3-2.7z"/></svg></div>
      <div class="sector-node-caption">Chimie</div>
    </div>
  </div>

  <!-- Bottom Strip -->
  <div class="footer-strip">
    <div class="footer-contacts-wrap">
      <div class="footer-contact-item">
        <div class="footer-contact-bubble">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
        </div>
        <div class="footer-contact-num">0775 55 87 28 / 0550 02 58 47</div>
      </div>
      <div class="footer-contact-item">
        <div class="footer-contact-bubble">
          <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        </div>
        <div class="footer-contact-num">hbig.dz@gmail.com</div>
      </div>
    </div>

    <!-- Right Orange Block -->
    <div class="footer-orange-slice">
      <div class="footer-slice-title">HB INDUSTRY GROUP</div>
      <div class="footer-slice-motto">Qualité · Sécurité · Performance</div>
    </div>
  </div>
</div>
</body>
</html>
"""

html_out = 'fiches_produits_commerciales/AFFICHE_MASTER_HBIG_AVEC_PAILLASSES_ET_PACKAGING.html'
with open(html_out, 'w', encoding='utf-8') as f:
    f.write(html_code)

print(f"Created {html_out}")

# Render with Selenium
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--force-device-scale-factor=1')
options.add_argument('--window-size=1200,1200')
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options)
abs_path = os.path.abspath(html_out).replace('\\', '/')
driver.get(f"file:///{abs_path}")
time.sleep(2)

png_out = 'fiches_produits_commerciales/AFFICHE_MASTER_HBIG_AVEC_PAILLASSES_ET_PACKAGING.png'
canvas = driver.find_element("css selector", ".poster-canvas")
canvas.screenshot(png_out)
driver.quit()

print(f"Saved: {png_out}")
im = Image.open(png_out)
print(f"Rendered image size: {im.size}")

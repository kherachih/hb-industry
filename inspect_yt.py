import urllib.request
import re
import json

url = 'https://www.youtube.com/shorts/UcWTeZepXJc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    title_m = re.search(r'<title>(.*?)</title>', html)
    print("Page Title:", title_m.group(1) if title_m else "None")
    
    # Try finding meta tags
    og_title = re.search(r'<meta property="og:title" content="(.*?)"', html)
    og_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
    og_image = re.search(r'<meta property="og:image" content="(.*?)"', html)
    
    print("OG Title:", og_title.group(1) if og_title else "None")
    print("OG Desc:", og_desc.group(1) if og_desc else "None")
    print("OG Image:", og_image.group(1) if og_image else "None")
    
    # Search for keywords or channel name
    keywords = re.findall(r'"keywords":\s*(\[.*?\])', html)
    if keywords:
        print("Keywords:", keywords[0][:200])

except Exception as e:
    print("Error:", e)

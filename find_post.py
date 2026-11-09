import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fb_selenium.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

idx = html.find("L'excellence")
if idx != -1:
    print("Found 'L'excellence' at position", idx)
    print("Context around it:")
    print(html[max(0, idx-200):idx+800])
else:
    print("Not found with exact string, searching case-insensitive...")
    import re
    m = re.search(r'excellence', html, re.IGNORECASE)
    if m:
        pos = m.start()
        print("Found at pos", pos)
        print(html[max(0, pos-200):pos+800])

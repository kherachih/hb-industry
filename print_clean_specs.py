import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('products_specifications.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    print(f"\n==========================================")
    print(f"PRODUIT: {p['title']}")
    print(f"URL: {p['url']}")
    print(f"==========================================")
    for s in p['content_snippets']:
        if len(s) > 15:
            print(f"- {s}")

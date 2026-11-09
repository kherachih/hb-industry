import urllib.request
import re

url = 'https://www.youtube.com/shorts/UcWTeZepXJc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Search for tool name in description
m = re.search(r'\"description\":\s*\{\"runs\":\s*(\[.*?\])\}', html)
if m:
    print("Full description runs:")
    print(m.group(1))
else:
    # Look for generic description
    m2 = re.search(r'\"shortDescription\":\s*\"(.*?)\"', html)
    if m2:
        print("Short description:", m2.group(1))

# Search for channel name
channel = re.search(r'\"ownerChannelName\":\s*\"(.*?)\"', html)
print("Channel:", channel.group(1) if channel else "Unknown")

import urllib.request
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

dest_dir = r'D:\Hb industry\terminal_clone\frames_raw'
os.makedirs(dest_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download_frame(idx):
    url = f'https://terminal-industries.com/static/frames/home/desktop/webp/hero_anim_desktop_60_{idx}.webp'
    file_path = os.path.join(dest_dir, f'hero_anim_desktop_60_{idx}.webp')
    if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
        return idx, True
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(file_path, 'wb') as f:
                f.write(data)
        return idx, True
    except Exception as e:
        return idx, False

start = time.time()
print('Starting parallel download of 410 frames...')
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(download_frame, i) for i in range(410)]
    completed = 0
    errors = 0
    for f in as_completed(futures):
        idx, success = f.result()
        if success:
            completed += 1
        else:
            errors += 1
        if (completed + errors) % 50 == 0 or (completed + errors) == 410:
            print(f'Progress: {completed + errors}/410 (Success: {completed}, Errors: {errors})')

duration = time.time() - start
print(f'Finished in {duration:.2f} seconds! Total downloaded: {completed}')

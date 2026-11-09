import os
from PIL import Image
import numpy as np

raw_dir = r'D:\Hb industry\terminal_clone\frames_raw'

# Let's inspect frames to get the exact trailer bounds across the whole sequence
# We can find trailer rear-top, front-top, rear-bottom, front-bottom

for idx in [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]:
    path = os.path.join(raw_dir, f'hero_anim_desktop_60_{idx}.webp')
    im = Image.open(path)
    arr = np.array(im)
    
    # Save a thumbnail with index
    brain_dir = r'C:\Users\pc-click\.gemini\antigravity\brain\16b48961-c305-4d16-bd2c-ca9bcf4112c0'
    im.resize((480, 270)).save(os.path.join(brain_dir, f'track_ref_{idx:03d}.jpg'), quality=80)
    print(f'Saved track_ref_{idx:03d}.jpg')

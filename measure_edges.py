import os
from PIL import Image
import numpy as np

raw_dir = r'D:\Hb industry\terminal_clone\frames_raw'

# Let's inspect the trailer position in frames 0 to 80
# In frame 0:
# trailer top edge: y ~ 349
# trailer bottom edge: y ~ 550
# trailer rear (left edge): let's find it
# trailer front (right edge): let's find it

def get_trailer_edges(arr):
    # Search horizontal edge at y=450
    row = arr[450, :, :]
    # Trailer panel has specific color characteristics:
    # Sky/background outside is bright sunset sky or dark ground
    # At y=450, left of trailer is sky (bright orange: R>180, G>130) or background
    # Inside trailer panel: R in [30, 90], G in [15, 60], B in [15, 50]
    is_panel = (row[:, 0] >= 25) & (row[:, 0] <= 100) & (row[:, 1] >= 15) & (row[:, 1] <= 65)
    indices = np.where(is_panel)[0]
    if len(indices) > 50:
        # filter out outliers
        left = indices[0]
        right = indices[-1]
        return left, right
    return None, None

for idx in range(0, 80, 5):
    path = os.path.join(raw_dir, f'hero_anim_desktop_60_{idx}.webp')
    im = Image.open(path)
    arr = np.array(im)
    left, right = get_trailer_edges(arr)
    print(f'Frame {idx:03d}: left={left}, right={right}, width={right-left if left else None}')

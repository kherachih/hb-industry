import os
import time
from concurrent.futures import ThreadPoolExecutor
import imageio
from PIL import Image

def main():
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(base_dir, 'user_new_video.mp4')
    desktop_dir = os.path.join(base_dir, 'static', 'frames', 'home', 'desktop', 'webp')
    mobile_dir = os.path.join(base_dir, 'static', 'frames', 'home', 'mobile', 'webp')
    
    os.makedirs(desktop_dir, exist_ok=True)
    os.makedirs(mobile_dir, exist_ok=True)
    
    print("Reading video frames...")
    reader = imageio.get_reader(video_path)
    video_frames = [f for f in reader]
    total_src = len(video_frames)
    print(f"Loaded {total_src} frames from video in {time.time() - start_time:.2f}s")
    
    # Pre-convert to PIL Images
    print("Converting to PIL Images...")
    pil_frames = [Image.fromarray(f) for f in video_frames]
    
    # Desktop 410 frames (0 to 409)
    # Mobile 410 frames (0 to 409)
    total_target = 410
    
    def process_desktop_frame(i):
        src_idx = int(round(i * (total_src - 1) / (total_target - 1)))
        src_idx = max(0, min(total_src - 1, src_idx))
        im = pil_frames[src_idx]
        out_path = os.path.join(desktop_dir, f'hero_anim_desktop_60_{i}.webp')
        im.save(out_path, 'WEBP', quality=88, method=4)
        return i
        
    def process_mobile_frame(i):
        src_idx = int(round(i * (total_src - 1) / (total_target - 1)))
        src_idx = max(0, min(total_src - 1, src_idx))
        im = pil_frames[src_idx]
        resized = im.resize((960, 540), Image.Resampling.LANCZOS)
        out_path = os.path.join(mobile_dir, f'hero_anim_mobile_60_{i}.webp')
        resized.save(out_path, 'WEBP', quality=82, method=4)
        return i

    print("Generating desktop WebP frames...")
    t1 = time.time()
    with ThreadPoolExecutor(max_workers=12) as executor:
        list(executor.map(process_desktop_frame, range(total_target)))
    print(f"Desktop frames completed in {time.time() - t1:.2f}s")

    print("Generating mobile WebP frames...")
    t2 = time.time()
    with ThreadPoolExecutor(max_workers=12) as executor:
        list(executor.map(process_mobile_frame, range(total_target)))
    print(f"Mobile frames completed in {time.time() - t2:.2f}s")

    print(f"All done in {time.time() - start_time:.2f}s!")

if __name__ == '__main__':
    main()

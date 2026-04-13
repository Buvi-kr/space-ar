import os
import rembg
from PIL import Image

def process_file(in_path, out_path_bg, out_path_webp):
    print(f"Processing {in_path}...")
    try:
        with open(in_path, 'rb') as i:
            with open(out_path_bg, 'wb') as o:
                output = rembg.remove(i.read())
                o.write(output)
        Image.open(out_path_bg).save(out_path_webp, 'WEBP', quality=95)
        print(f"Saved {out_path_webp}")
    except Exception as e:
        print(f"Error on {in_path}: {e}")

for i in [1, 2, 3]:
    process_file(f'assets/ship{i}_artifact.png', f'assets/ship{i}_bg.png', f'assets/ship{i}_bg.png') # saving directly to _bg.png since we want PNG for the background or webp.
    # Ah wait, I will just save the transparent one to _bg.png, and the HTML is already updated to load ship${shipId}_bg.png

process_file('assets/cute_sun.png', 'assets/cute_sun_bg.png', 'assets/cute_sun.webp')

try:
    print("Resizing background...")
    Image.open('assets/new_bg.png').resize((1920, 1080)).save('assets/new_bg.webp', 'WEBP', quality=85)
except Exception as e:
    print(f"Error bg: {e}")

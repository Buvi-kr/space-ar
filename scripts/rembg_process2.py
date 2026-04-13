import os
import rembg
from PIL import Image

def process_file(in_path, out_path_bg):
    print(f"Processing {in_path}...")
    try:
        with open(in_path, 'rb') as i:
            with open(out_path_bg, 'wb') as o:
                output = rembg.remove(i.read())
                o.write(output)
        print(f"Saved {out_path_bg}")
    except Exception as e:
        print(f"Error on {in_path}: {e}")

process_file(r"C:\Users\Buvi\.gemini\antigravity\brain\f159dbc8-8eb0-4b52-a553-ca8d1b13c72f\media__1775720220563.jpg", 'assets/ship1_bg.png')
process_file(r"C:\Users\Buvi\.gemini\antigravity\brain\f159dbc8-8eb0-4b52-a553-ca8d1b13c72f\media__1775720220512.jpg", 'assets/ship2_bg.png')
process_file(r"C:\Users\Buvi\.gemini\antigravity\brain\f159dbc8-8eb0-4b52-a553-ca8d1b13c72f\media__1775720220466.jpg", 'assets/ship3_bg.png')

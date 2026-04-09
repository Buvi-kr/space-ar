from PIL import Image
import os

src_path = r"C:\Users\Buvi\.gemini\antigravity\brain\f159dbc8-8eb0-4b52-a553-ca8d1b13c72f\majestic_sun_1775715480120.png"
if os.path.exists(src_path):
    sun = Image.open(src_path).convert("RGB")
    sun = sun.resize((400, 400), Image.Resampling.LANCZOS)

    frames = []
    # Create 36 frames for animation
    for i in range(0, 360, 10):
        frames.append(sun.rotate(i, resample=Image.Resampling.BICUBIC, fillcolor=(0,0,0)))

    frames[0].save(
        "assets/anim_sun.webp",
        "WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=60,
        loop=0
    )
    print("Created animated sun webp")
else:
    print("Source image not found.")

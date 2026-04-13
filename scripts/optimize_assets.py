import os
from PIL import Image, ImageSequence
import urllib.request
import io
import math

print("1. Optimizing BG for 2GB RAM...")
if os.path.exists('assets/bg.png'):
    bg = Image.open('assets/bg.png').convert('RGBA')
    # Resize keeping aspect ratio, but max width 1920
    bg.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
    bg.save('assets/bg.webp', 'WEBP', quality=80)
    print("BG size reduced and saved as webp.")

print("2. Removing black background from spaceships and shrinking...")
if os.path.exists('assets/ship.png'):
    ship = Image.open('assets/ship.png').convert('RGBA')
    ship.thumbnail((400, 400), Image.Resampling.LANCZOS)
    data = ship.getdata()
    new_data = []
    # thresholding for black color isolation
    for item in data:
        # Calculate brightness
        brightness = (item[0] + item[1] + item[2]) / 3
        if brightness < 40:
            new_data.append((item[0], item[1], item[2], 0))
        else:
            alpha = int(min(255, (brightness - 40) * 1.5))
            new_data.append((item[0], item[1], item[2], min(item[3], alpha)))
    ship.putdata(new_data)
    ship.save('assets/ship.webp', 'WEBP', quality=90)
    print("Ship bg removed and saved as webp.")

print("3. Fetching solar flare GIF and converting to animated WebP...")
url = "https://media.tenor.com/-43UV6Q48L0AAAAC/the-sun-solar-flare.gif"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
sun_gif = Image.open(io.BytesIO(response.read()))

frames = []
for frame in ImageSequence.Iterator(sun_gif):
    f = frame.convert('RGBA')
    # Ensure it's square
    w, h = f.size
    min_dim = min(w, h)
    f = f.crop((w//2 - min_dim//2, h//2 - min_dim//2, w//2 + min_dim//2, h//2 + min_dim//2))
    f = f.resize((300, 300), Image.Resampling.LANCZOS)
    
    # Circular mask to hide edges to make it orb-like
    mask = Image.new('L', (300, 300), 0)
    for y in range(300):
        for x in range(300):
            dist = math.hypot(x - 150, y - 150)
            if dist < 120:
                mask.putpixel((x, y), 255)
            elif dist < 145:
                # Fade out edge
                alpha_val = int(255 * (145 - dist) / 25)
                mask.putpixel((x, y), alpha_val)
    f.putalpha(mask)
    frames.append(f)

# Save animated webp
frames[0].save('assets/sun.webp', 'WEBP', save_all=True, append_images=frames[1:], duration=sun_gif.info.get('duration', 100), loop=0)
print("Solar flare animated WebP created.")

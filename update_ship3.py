import os
import rembg

in_path = r"C:\Users\Buvi\.gemini\antigravity\brain\f159dbc8-8eb0-4b52-a553-ca8d1b13c72f\media__1775783619639.jpg"
out_path = r"assets\ship3_bg.png"

with open(in_path, 'rb') as i:
    with open(out_path, 'wb') as o:
        output = rembg.remove(i.read())
        o.write(output)
print("Updated ship3_bg.png successfully!")

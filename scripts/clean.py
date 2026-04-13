from PIL import Image

for i in [1, 2, 3]:
    try:
        img = Image.open(f'assets/ship{i}.png').convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Replace white or nearly white with transparent
            if item[0] > 235 and item[1] > 235 and item[2] > 235:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        img.save(f'assets/ship{i}.webp', 'WEBP')
        print(f"Processed ship{i}")
    except Exception as e:
        print(f"Error on ship{i}: {e}")

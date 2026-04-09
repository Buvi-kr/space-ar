import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Layout for Horizontal (1920x1080)
html = re.sub(r'#draw-ui\s*\{[^}]*width:\s*min\(900px,\s*95vw\)[^}]*height:\s*70vh;[^}]*\}', 
              r'#draw-ui {\n      position: absolute;\n      bottom: -600px;\n      left: 50%;\n      transform: translateX(-50%);\n      width: 1000px;\n      height: 520px;\n      background: rgba(5, 10, 20, 0.97);\n      border: 1px solid rgba(255, 255, 255, 0.25);\n      border-bottom: none;\n      border-radius: 24px 24px 0 0;\n      box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.8);\n      z-index: 200;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      padding: 20px;\n      transition: bottom 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);\n      overflow: hidden;\n    }', html)

# 2. Dynamic Card CSS (Auto Width/Height)
html = re.sub(r'\.wish-card\s*\{[^}]*width:\s*280px;[^}]*height:\s*160px;[^}]*margin-left:\s*-140px;[^}]*margin-top:\s*-80px;[^}]*\}',
              r'.wish-card {\n      position: absolute;\n      /* No fixed width/height for dynamic sizing */\n      background: rgba(10, 15, 30, 0.85);\n      border-radius: 24px;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      justify-content: center;\n      padding: 15px;\n      pointer-events: none;\n      transition: left 2.5s cubic-bezier(0.25, 1, 0.5, 1), top 2.5s cubic-bezier(0.25, 1, 0.5, 1), transform 2.5s cubic-bezier(0.25, 1, 0.5, 1), opacity 1s;\n      transform-origin: center;\n    }', html)

# 3. Dynamic Engine Thrusters (Proportional base)
html = re.sub(r'\.drone-base\s*\{[^}]*bottom:\s*-60px;[^}]*width:\s*140px;[^}]*height:\s*80px;[^}]*\}',
              r'.drone-base {\n      position: absolute;\n      bottom: -40%;\n      left: 50%;\n      transform: translateX(-50%);\n      width: 80%; /* proportional */\n      height: 60px;\n      display: flex;\n      justify-content: space-between;\n      align-items: center;\n      padding: 0 10%;\n      z-index: 4;\n    }', html)

# 4. Phototime Class
if '.phototime' not in html:
    css_insert = """
    .wish-card.phototime {
      z-index: 9999 !important;
      left: 50% !important;
      top: 50% !important;
      transform: translate(-50%, -50%) scale(2) !important;
      transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
    }
    """
    html = html.replace('</style>', css_insert + '</style>')

# 5. JS Auto Crop Logic & PhotoTime Toggle
crop_js = """
    // 1. Auto Crop Canvas Function
    function cropCanvas(sourceCanvas, padding = 30) {
      const ctx = sourceCanvas.getContext('2d');
      const w = sourceCanvas.width;
      const h = sourceCanvas.height;
      const data = ctx.getImageData(0, 0, w, h).data;
      
      let minX = w, minY = h, maxX = 0, maxY = 0;
      let drawn = false;
      
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const alpha = data[(y * w + x) * 4 + 3];
          if (alpha > 0) {
            drawn = true;
            if (x < minX) minX = x;
            if (x > maxX) maxX = x;
            if (y < minY) minY = y;
            if (y > maxY) maxY = y;
          }
        }
      }
      
      if (!drawn) return sourceCanvas.toDataURL('image/webp', 0.6); // Empty
      
      // Apply Padding
      minX = Math.max(0, minX - padding);
      minY = Math.max(0, minY - padding);
      maxX = Math.min(w, maxX + padding);
      maxY = Math.min(h, maxY + padding);
      
      const width = maxX - minX;
      const height = maxY - minY;
      
      const cropCanvas = document.createElement('canvas');
      cropCanvas.width = width;
      cropCanvas.height = height;
      const cropCtx = cropCanvas.getContext('2d');
      
      cropCtx.drawImage(
        sourceCanvas,
        minX, minY, width, height,
        0, 0, width, height
      );
      
      return cropCanvas.toDataURL('image/webp', 0.8);
    }
"""

if 'cropCanvas' not in html:
    html = html.replace('document.getElementById(\'submit-btn\').addEventListener(\'click\', () => {', 
                        crop_js + "\n    document.getElementById('submit-btn').addEventListener('click', () => {")

html = html.replace("const dataURL = canvas.toDataURL('image/webp', 0.6); // 사이즈 압축",
                    "const dataURL = cropCanvas(canvas, 30); // 1. Auto Crop Applied")

# Update Wish Card Creation & Phototime Logic
html = re.sub(r"card\.innerHTML\s*=\s*`[^`]+`;", 
              r"""
        card.innerHTML = `
        <div class="speech-tail" style="border-top:16px solid ${data.color};"></div>
        <img src="${data.img}" style="pointer-events: auto;">
        <div class="drone-base" style="background:url('assets/ship${data.shipId}_bg.png') center/contain no-repeat;">
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
        </div>`;
      """, html)

# Phototime click listener update
click_js = """
      // 관리자 강제삭제 핸들러 & 포토타임 토글
      let isPhotoTime = false;
      let originalLeft, originalTop, originalTransform;
      card.addEventListener('click', () => {
        if (isAdminMode) { 
          card.remove(); grids[gridId].occupied = false; 
          allWishes = allWishes.filter(w => w !== wishObj); 
          saveToLocalStorage();
        } else {
          // 4. 포토타임 로직
          isPhotoTime = !isPhotoTime;
          if (isPhotoTime) {
            originalLeft = card.style.left;
            originalTop = card.style.top;
            originalTransform = card.style.transform;
            
            // Centering logic via class
            card.classList.add('phototime');
            card.classList.remove('floating');
            
            // Auto return after 5 seconds
            setTimeout(() => {
              if(isPhotoTime && document.body.contains(card)) {
                isPhotoTime = false;
                card.classList.remove('phototime');
                card.classList.add('floating');
              }
            }, 5000);
          } else {
            card.classList.remove('phototime');
            card.classList.add('floating');
          }
        }
      });
"""
html = re.sub(r"card\.addEventListener\('click',\s*\(\)\s*=>\s*\{[\s\S]*?\}\);", click_js, html)

# Dynamic center margins. Since width/height are variable, using translate(-50%, -50%) makes absolute positioning relative to center!
html = html.replace("card.style.left = finalX + 'px';", "card.style.left = finalX + 'px'; card.style.transform = 'translate(-50%, -50%)';")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

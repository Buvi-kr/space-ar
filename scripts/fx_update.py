import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add #phototime-fx DIV
if '<div id="phototime-fx"></div>' not in html:
    html = html.replace('<div id="scene"></div>', '<div id="scene"></div>\n  <div id="phototime-fx"></div>')

# 2. Add Spotlight / FX CSS
css_fx = """
    #phototime-fx {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      width: 150vw; height: 150vw;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.5s;
      z-index: 9998; /* Underneath the phototime card */
      background: 
        radial-gradient(circle at 50% 50%, rgba(255,255,230,0.5) 0%, rgba(255,220,100,0.2) 20%, transparent 60%),
        conic-gradient(from 0deg at 50% 50%, transparent 0deg, rgba(255,255,255,0.3) 45deg, transparent 90deg, rgba(255,255,255,0.3) 135deg, transparent 180deg, rgba(255,255,255,0.3) 225deg, transparent 270deg, rgba(255,255,255,0.3) 315deg, transparent 360deg);
      mix-blend-mode: screen;
    }
    #phototime-fx.active {
      opacity: 1;
      animation: spotlightSpin 15s linear infinite;
    }
    @keyframes spotlightSpin {
      0% { transform: translate(-50%, -50%) rotate(0deg); }
      100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
"""
if '#phototime-fx {' not in html:
    html = html.replace('</style>', css_fx + '</style>')

# 3. Block Grid Center & Bottom Center
grid_init = """
    function initGrids() {
      updateGridDimensions();
      grids = Array.from({length: MAX_WISHES}, (_, i) => {
        let isBlocked = false;
        // Block Center (Row 1, Col 2) -> Index 7
        // Block Bottom Center (Row 2, Col 2) -> Index 12
        if (i === 7 || i === 12) isBlocked = true;
        
        return {
          id: i,
          occupied: isBlocked, // Permanently mark as occupied so emptyGrids ignores it
          blocked: isBlocked,
          cx: (i % COLS) * cellWidth + cellWidth / 2,
          cy: (Math.floor(i / COLS)) * cellHeight + cellHeight / 2
        };
      });
    }
"""
html = re.sub(r'function initGrids\(\)\s*\{[\s\S]*?\}\n\s*initGrids\(\);', grid_init + '    initGrids();', html)

# 4. Trigger Phototime FX via click handling
# The existing click listener needs to toggle the #phototime-fx element
phototime_js = """
      // 관리자 강제삭제 핸들러 & 포토타임 토글
      let isPhotoTime = false;
      let originalLeft, originalTop, originalTransform;
      card.addEventListener('click', () => {
        if (isAdminMode) { 
          card.remove(); 
          if (!grids[gridId].blocked) grids[gridId].occupied = false; 
          allWishes = allWishes.filter(w => w !== wishObj); 
          saveToLocalStorage();
        } else {
          // 4. 포토타임 로직
          const fxLayer = document.getElementById('phototime-fx');
          isPhotoTime = !isPhotoTime;
          if (isPhotoTime) {
            originalLeft = card.style.left;
            originalTop = card.style.top;
            originalTransform = card.style.transform;
            
            card.classList.add('phototime');
            card.classList.remove('floating');
            fxLayer.classList.add('active'); // 스포트라이트 ON
            
            setTimeout(() => {
              if(isPhotoTime && document.body.contains(card)) {
                isPhotoTime = false;
                card.classList.remove('phototime');
                card.classList.add('floating');
                fxLayer.classList.remove('active'); // 스포트라이트 OFF
              }
            }, 5000);
          } else {
            card.classList.remove('phototime');
            card.classList.add('floating');
            fxLayer.classList.remove('active'); // 스포트라이트 OFF
          }
        }
      });
"""
html = re.sub(r'// 관리자 강제삭제 핸들러 & 포토타임 토글[\s\S]*?\}\);', phototime_js, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied phototime fx & grid blocks")

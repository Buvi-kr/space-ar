import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove grid logic
html = re.sub(r'let COLS = 5, ROWS = 3, MAX_WISHES = COLS \* ROWS;.*?function initGrids\(\s*\)\s*\{.*?\}\s*initGrids\(\);', 
              r'const MAX_WISHES = 12;\n    const colorPalette = ["#ff00ea", "#00d2ff", "#39ff14", "#ffeb3b", "#ff6b35", "#b15cff", "#ff5c8d", "#5cffda"];',
              html, flags=re.DOTALL)

# 2. Update `saveToLocalStorage` and `loadFromLocalStorage`
js_storage = """
    function saveToLocalStorage() {
      const data = allWishes.map(w => ({ img: w.imgSrc, color: w.color, finalX: w.finalX, finalY: w.finalY, shipId: w.shipId }));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
    
    function loadFromLocalStorage() {
      const svd = localStorage.getItem(STORAGE_KEY);
      if(!svd) return;
      try {
        const data = JSON.parse(svd);
        data.forEach(d => {
          createWishElement(d, d.finalX, d.finalY, true); // 바로 배치
        });
      } catch(e) {}
    }
"""
html = re.sub(r'function saveToLocalStorage\(\)\s*\{.*?\}\s*function loadFromLocalStorage\(\)\s*\{.*?\}', js_storage, html, flags=re.DOTALL)

# 3. Update `submit-btn` click handler to generate random color
# From: launchNewWish(dataURL, penColor);
# To: launchNewWish(dataURL); (color chosen inside)
html = html.replace("launchNewWish(dataURL, penColor);", "launchNewWish(dataURL);")

# 4. Rewrite `launchNewWish` and `createWishElement`
js_launch = """
    // 신규 소원 발사
    function launchNewWish(imgSrc) {
      const randomColor = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      
      let valid = false, fx = 0, fy = 0;
      let wW = window.innerWidth, wH = window.innerHeight;
      
      for(let i=0; i<100; i++) {
        // 화면 가장자리 여백 확보
        fx = 150 + Math.random() * (wW - 300);
        fy = 100 + Math.random() * (wH - 250);
        
        let cx = wW / 2, cy = wH / 2;
        
        // 중앙 포토타임 존 회피
        if(Math.abs(fx - cx) < 350 && Math.abs(fy - cy) < 250) continue;
        // 하단 UI 버튼 영역 회피
        if(fy > wH - 200 && Math.abs(fx - cx) < 400) continue;
        
        // 겹침 체크
        let overlap = false;
        for(let w of allWishes) {
          if(!w.el.classList.contains('departing') && Math.abs(fx - w.finalX) < 280 && Math.abs(fy - w.finalY) < 180) {
            overlap = true; break;
          }
        }
        if(!overlap) { valid = true; break; }
      }
      
      if(!valid || allWishes.length >= MAX_WISHES) {
        // 자리 없거나 최대 개수 초과 시 가장 오래된 것 삭제 (퇴장 애니메이션)
        const oldest = allWishes[0];
        if(oldest) {
          oldest.el.classList.add('departing');
          allWishes.shift();
          setTimeout(() => { try { oldest.el.remove(); } catch(e){} }, 2000);
        }
        // 삭제 후 자리 확보 없이 그냥 마지막에 구한 좌표(무작위 중복)에 발사
      }
      
      const dataInfo = { img: imgSrc, color: randomColor, shipId: (Math.floor(Math.random() * 3) + 1) };
      createWishElement(dataInfo, fx, fy, false);
    }
    
    function createWishElement(data, finalX, finalY, immediate) {
      const card = document.createElement('div');
      card.className = 'wish-card';
      card.style.border = `3px solid ${data.color}`;
      card.style.boxShadow = `0 0 25px ${data.color}80`;
      // 말풍선의 전체 배경을 반투명 랜덤 색상으로 부여
      card.style.backgroundColor = data.color + '40'; // 25% opacity hex
      card.style.backdropFilter = 'blur(4px)'; // 살짝 블러
      card.style.webkitBackdropFilter = 'blur(4px)';
      
      card.innerHTML = `
        <div class="speech-tail" style="border-top:16px solid ${data.color};"></div>
        <img src="${data.img}" style="pointer-events: auto;">
        <div class="drone-base" style="background:url('assets/ship${data.shipId}_bg.png') center/contain no-repeat;">
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
        </div>`;
      
      scene.appendChild(card);
      
      const wishObj = { el: card, createdAt: Date.now(), finalX: finalX, finalY: finalY, imgSrc: data.img, color: data.color, shipId: data.shipId };
      allWishes.push(wishObj);
      saveToLocalStorage();
      
      // 관리자 핸들러 & 포토타임
      let isPhotoTime = false;
      let originalLeft, originalTop, originalTransform;
      card.addEventListener('click', () => {
        if (isAdminMode) { 
          card.remove(); 
          allWishes = allWishes.filter(w => w !== wishObj); 
          saveToLocalStorage();
        } else {
          const fxLayer = document.getElementById('phototime-fx');
          isPhotoTime = !isPhotoTime;
          if (isPhotoTime) {
            originalLeft = card.style.left;
            originalTop = card.style.top;
            originalTransform = card.style.transform;
            card.classList.add('phototime');
            card.classList.remove('floating');
            fxLayer.classList.add('active'); 
            
            setTimeout(() => {
              if(isPhotoTime && document.body.contains(card)) {
                isPhotoTime = false;
                card.classList.remove('phototime');
                card.classList.add('floating');
                fxLayer.classList.remove('active');
              }
            }, 5000);
          } else {
            card.classList.remove('phototime');
            card.classList.add('floating');
            fxLayer.classList.remove('active');
          }
        }
      });

      if(immediate) {
        card.style.left = finalX + 'px'; card.style.transform = 'translate(-50%, -50%)';  
        card.style.top = finalY + 'px';
        card.classList.add('floating');
      } else {
        card.style.zIndex = 10;
        card.style.left = (window.innerWidth / 2) + 'px';
        card.style.top = (window.innerHeight + 200) + 'px'; 
        card.style.transform = 'translate(-50%, -50%) scale(0.3)';

        const pInterval = setInterval(() => {
          const r = card.getBoundingClientRect();
          const p = document.createElement('div'); p.className = 'particle';
          p.style.width = (Math.random() * 10 + 5) + 'px'; p.style.height = p.style.width;
          p.style.background = data.color; p.style.boxShadow = `0 0 10px ${data.color}`;
          p.style.left = (r.left + r.width/2 + (Math.random()*40-20)) + 'px';
          p.style.top = (r.top + r.height + (Math.random()*20)) + 'px';
          scene.appendChild(p);
          setTimeout(() => p.remove(), 1200);
        }, 120);

        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            card.style.left = finalX + 'px'; card.style.transform = 'translate(-50%, -50%) scale(1)';
            card.style.top = finalY + 'px';
            setTimeout(() => {
              clearInterval(pInterval);
              card.style.transform = 'translate(-50%, -50%)';
              card.classList.add('floating'); 
            }, 2500);
          });
        });
      }
    }
"""

html = re.sub(r'// 신규 소원 발사.*?function createWishElement.*?\}\n\s*\}\n', js_launch, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html to completely remove grids and scatter randomly.")

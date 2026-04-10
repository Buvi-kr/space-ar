import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS: Card boundaries and Fixed Drone sizes
css_updates = """
    /* 4. 소원 카드 체류 및 레이어 로직 */
    .wish-card {
      position: absolute;
      /* Box bounds to prevent distortion */
      min-width: 140px;
      max-width: 320px;
      min-height: 100px;
      max-height: 250px;
      
      background: rgba(10, 15, 30, 0.85);
      border-radius: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 15px;
      pointer-events: none;
      transition: left 2.5s cubic-bezier(0.25, 1, 0.5, 1), top 2.5s cubic-bezier(0.25, 1, 0.5, 1), transform 2.5s cubic-bezier(0.25, 1, 0.5, 1), opacity 1s;
      transform-origin: center;
    }
"""
html = re.sub(r'/\* 4\. 소원 카드 체류 및 레이어 로직 \*/\s*\.wish-card \{[\s\S]*?transform-origin: center;\s*\}', css_updates.strip(), html)

css_drone = """
    .drone-base {
      position: absolute;
      bottom: -65px; /* Absolute fixed distance below card */
      left: 50%;
      transform: translateX(-50%);
      width: 130px; /* Fixed width */
      height: 60px; /* Fixed height */
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 20px;
      z-index: 4;
    }
"""
html = re.sub(r'\.drone-base \{[\s\S]*?z-index: 4;\s*\}', css_drone.strip(), html)

# 2. Add drag visual logic for PhotoTime and Cloud Spawning Logic
js_launch = """
    // 구름 군락(Cloud Cluster) 노드들 정의
    const cloudNodes = [
      { cx: 250, cy: 300 }, // 좌상단
      { cx: 300, cy: 700 }, // 좌하단
      { cx: window.innerWidth - 300, cy: 300 }, // 우상단
      { cx: window.innerWidth - 250, cy: 700 }  // 우하단
    ];

    // 신규 소원 발사
    function launchNewWish(imgSrc) {
      const randomColor = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      
      let valid = false, fx = 0, fy = 0;
      let wW = window.innerWidth, wH = window.innerHeight;
      
      // 구름 기반 무작위 흩뿌림
      for(let i=0; i<100; i++) {
        // 랜덤 구름 노드 선택
        const node = cloudNodes[Math.floor(Math.random() * cloudNodes.length)];
        
        // 반경 내 랜덤 지터(떨림)
        fx = node.cx + (Math.random() * 300 - 150);
        fy = node.cy + (Math.random() * 250 - 125);
        
        let cx = wW / 2, cy = wH / 2;
        
        // 화면 가장자리 여백 확보
        if (fx < 150 || fx > wW - 150) continue;
        if (fy < 100 || fy > wH - 180) continue;
        
        // 중앙 포토타임 존 절대 침범 금지
        if(Math.abs(fx - cx) < 350 && Math.abs(fy - cy) < 250) continue;
        // 하단 소원 버튼 영역 절대 침범 금지
        if(fy > wH - Math.max(200, wH*0.2) && Math.abs(fx - cx) < 350) continue;
        
        // 우주선끼리 심한 겹침 방지 (공간 확보)
        let overlap = false;
        for(let w of allWishes) {
          if(!w.el.classList.contains('departing') && Math.abs(fx - w.finalX) < 180 && Math.abs(fy - w.finalY) < 150) {
            overlap = true; break;
          }
        }
        if(!overlap) { valid = true; break; }
      }
      
      if(!valid || allWishes.length >= MAX_WISHES) {
        const oldest = allWishes[0];
        if(oldest) {
          oldest.el.classList.add('departing');
          allWishes.shift();
          setTimeout(() => { try { oldest.el.remove(); } catch(e){} }, 2000);
        }
      }
      
      const dataInfo = { img: imgSrc, color: randomColor, shipId: (Math.floor(Math.random() * 3) + 1) };
      createWishElement(dataInfo, fx, fy, false);
    }
    
    function createWishElement(data, finalX, finalY, immediate) {
      const card = document.createElement('div');
      card.className = 'wish-card';
      card.style.border = `3px solid ${data.color}`;
      card.style.boxShadow = `0 0 25px ${data.color}80`;
      card.style.backgroundColor = data.color + '40'; 
      card.style.backdropFilter = 'blur(4px)'; 
      card.style.webkitBackdropFilter = 'blur(4px)';
      card.style.cursor = 'pointer'; // 드래그/클릭 유도
      
      card.innerHTML = `
        <div class="speech-tail" style="border-top:16px solid ${data.color};"></div>
        <img src="${data.img}" style="pointer-events: none; object-fit: contain;">
        <div class="drone-base" style="background:url('assets/ship${data.shipId}_bg.png') center/contain no-repeat;">
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
          <div class="drone-thruster" style="background:radial-gradient(circle,#fff 10%,${data.color} 60%,transparent 100%);"></div>
        </div>`;
      
      scene.appendChild(card);
      
      const wishObj = { el: card, createdAt: Date.now(), finalX: finalX, finalY: finalY, imgSrc: data.img, color: data.color, shipId: data.shipId };
      allWishes.push(wishObj);
      saveToLocalStorage();
      
      let isPhotoTime = false;
      let originalLeft = finalX + 'px';
      let originalTop = finalY + 'px';
      
      // 관리자 강제삭제 & 중앙 포토존 연동
      card.addEventListener('click', (e) => {
        if (isAdminMode) { 
          card.remove(); 
          allWishes = allWishes.filter(w => w !== wishObj); 
          saveToLocalStorage();
        } else {
          // 중앙 포토존 이동 연동 (클릭/터치)
          const fxLayer = document.getElementById('phototime-fx');
          isPhotoTime = !isPhotoTime;
          if (isPhotoTime) {
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

      // 마우스/터치 드래그 연동 기능 (포토존 유도용 단순 반응)
      let isDragging = false, startY = 0;
      card.addEventListener('mousedown', (e) => { if(!isAdminMode) { isDragging=true; startY=e.clientY; }});
      card.addEventListener('touchstart', (e) => { if(!isAdminMode) { isDragging=true; startY=e.touches[0].clientY; }});
      window.addEventListener('mouseup', () => { if(isDragging && !isPhotoTime) { isDragging=false; }});
      window.addEventListener('touchend', () => { if(isDragging && !isPhotoTime) { isDragging=false; }});

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
print("Updated index.html to apply cluster nodes and boundaries.")

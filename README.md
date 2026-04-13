# 🚀 소원 우주선 (Wish Spaceship)

**포천아트밸리 천문과학관**의 인터랙티브 전시 키오스크 프로젝트입니다. 사용자가 자신의 소원을 직접 그리고 스티커로 꾸며 우주로 날려보내는 특별한 경험을 제공합니다.

---

## ✨ 핵심 기능 (Features)

- **인터랙티브 드로잉**: 캔버스에 직접 소원을 그리고 다양한 색상과 굵기의 펜을 사용합니다.
- **스티커 꾸미기**: 행성, 별, 로켓 등 우주 테마의 이모지 스티커를 활용할 수 있습니다.
- **실시간 물리 엔진**: 화면에 떠다니는 우주선들이 서로 부딪히지 않게 유기적으로 움직이며, 실제 우주 공간과 같은 부유감을 제공합니다.
- **포토 타임 (PhotoTime)**: 생성된 우주선을 터치하면 화면 중앙으로 스포트라이트를 받으며 등장하는 연출을 제공합니다.
- **관리자 모드**: 전시 관리를 위한 데이터 관리 및 삭제 기능을 포함합니다.

---

## 📂 폴더 구조 (Project Structure)

```text
.
├── scripts/            # 자동화 및 리소스 최적화용 파이썬 스크립트 모음
│   ├── clean.py        # 리소스 정리 스크립트
│   ├── make_sun.py     # 태양 효과 생성 도구
│   ├── update.py       # 전체 업데이트 스크립트
│   └── (기타 스크립트...)
├── assets/             # 이미지, 웹피(WebP), 사운드 등 리소스 파일
├── index.html          # 메인 웹 어플리케이션 (Single Page App)
└── README.md           # 프로젝트 안내서
```

---

## 🛠️ 기술 사양 (Tech Stack)

- **Frontend**: Vanilla JS, HTML5 Canvas API
- **Styling**: Vanilla CSS (Modern Fluid Layout)
- **Animation**: CSS Keyframes, High-performance RequestAnimationFrame
- **Optimization**: WebP image format, Canvas cropping

---

## 🚀 시작하기 (How to Run)

1. 이 저장소를 클론하거나 다운로드합니다.
2. `index.html` 파을 브라우저에서 엽니다. (추천: Chrome 또는 Edge)
3. 전체화면 모드를 통해 현장 키오스크와 동일한 환경을 체험할 수 있습니다.

---

## 📝 관리자 가이드

- 화면 우측 상단의 시크릿 존을 5회 이상 클릭하면 **관리자 모드**가 활성화됩니다.
- 관리자 모드에서는 생성된 소원 우주선을 개별 삭제하거나 전체 초기화할 수 있습니다.

---

> 본 프로젝트는 저사양 환경(2GB RAM 등)에서도 미러링 및 전시가 가능하도록 최적화되어 설계되었습니다.

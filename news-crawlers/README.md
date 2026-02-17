# News Crawlers

AI_Brain Vault용 뉴스 크롤러 - GitHub Actions로 매일/매주 자동 실행

## 📁 구조

```
news-crawlers/
├── .github/workflows/
│   ├── trend-detector.yml    # 매일 오전 9시 (KST)
│   ├── tech-news.yml         # 매주 금요일 오전 9시
│   └── niche-crawler.yml     # 매주 화요일 오전 9시
├── crawlers/
│   ├── trend_detector/       # Google Trends, TikTok 트렌드
│   ├── tech_news/            # GitHub Trending 다이제스트
│   └── niche_crawler/        # YC RFS, Exploding Topics
└── README.md
```

## 🔐 필요한 Secrets

news-crawlers 레포에 등록:

| Secret | 설명 |
|--------|------|
| `GEMINI_API_KEY` | Google Gemini API 키 (트렌드 분석용) |
| `AI_BRAIN_TOKEN` | AI_Brain 레포에 push할 수 있는 Personal Access Token |

### AI_BRAIN_TOKEN 생성 방법

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. 권한: `repo` 체크
4. 생성된 토큰을 Secrets에 등록

## 📤 결과물

크롤러가 생성한 `.md` 파일은 AI_Brain 레포의 다음 폴더로 push됨:

```
AI_Brain/
└── 3_자료/
    └── 뉴스/
        ├── 1. Trend_detector/
        ├── 2. Niche_crawler/
        └── 3. Tech News/
```

## 🚀 수동 실행

GitHub 레포 → Actions → 원하는 workflow → Run workflow

## 📝 수정 필요

workflow 파일에서 AI_Brain 레포명 확인:
```yaml
repository: heoseogjun/AI_Brain  # 실제 레포명으로 변경
```

## 🛠 로컬 테스트

```bash
cd crawlers/trend_detector
pip install -r requirements.txt
GEMINI_API_KEY=your_key python main.py
```

## 📅 스케줄

| 크롤러 | 실행 주기 | 설명 |
|--------|-----------|------|
| Trend Detector | 매일 오전 9시 | 오늘의 트렌드 분석 |
| Tech News | 매주 금요일 오전 9시 | 주간 기술 뉴스 |
| Niche Crawler | 매주 화요일 오전 9시 | 스타트업 아이디어 |

---

Made by Claude Code

---
title: Atlas용 작업 지시서
date: 2026-02-17
type: instruction
---

# 🌐 Atlas 작업 지시서

## 1️⃣ news-crawlers.zip 업로드

```
AI_Brain/news-crawlers.zip 파일의 내용으로 GitHub에 news-crawlers 레포를 만들어줘.

절차:
1. github.com/new 접속해서 news-crawlers 레포 생성 (Private)
2. 레포 생성 후, AI_Brain/news-crawlers.zip 내용을 업로드
```

---

## 2️⃣ Secrets 등록 페이지까지 이동

```
news-crawlers 레포 → Settings → Secrets and variables → Actions

여기까지 열어두면 됨. 실제 키 입력은 석준님이 직접 할 거야.
```

---

## 📋 등록할 Secret (1개만)

| Secret 이름 | 설명 |
|-------------|------|
| `Z_AI_API_KEY` | z.ai Coding Plan API 키 |

**토큰이 2개에서 1개로 줄었음!** (AI_BRAIN_TOKEN 불필요)

---

## ✅ 완료 후 확인

```
1. Actions 탭에서 workflow 3개가 보이는지 확인
2. 하나 선택해서 "Run workflow"로 수동 실행 테스트
3. output/ 폴더에 결과물이 쌓이는지 확인
```

---

## 📂 결과물 위치

```
news-crawlers/
└── output/
    ├── trend_detector/   # 매일 업데이트
    ├── tech_news/        # 매주 금요일
    └── niche_crawler/    # 매주 화요일
```

---
#type/instruction

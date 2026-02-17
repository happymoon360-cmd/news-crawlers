#!/usr/bin/env python3
"""
Tech News - GitHub Trending digest using z.ai Coding Plan (GLM-5)
"""

import os
import requests
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configuration - z.ai Coding Plan API
Z_AI_API_KEY = os.environ.get("Z_AI_API_KEY")
Z_AI_BASE_URL = os.environ.get("Z_AI_BASE_URL", "https://api.z.ai/api/openai/v1")
MODEL = "glm-5"
TIMEOUT = 600  # 10 minutes

OUTPUT_DIR = Path("/tmp/output")
DATE = datetime.now().strftime("%Y-%m-%d")

client = OpenAI(
    api_key=Z_AI_API_KEY,
    base_url=Z_AI_BASE_URL,
    timeout=TIMEOUT
)


def fetch_github_trending() -> list:
    """Fetch trending repos from GitHub"""
    try:
        headers = {"Accept": "application/vnd.github.v3+json"}
        search_url = "https://api.github.com/search/repositories"
        params = {
            "q": "stars:>500 created:>2025-01-01",
            "sort": "stars",
            "order": "desc",
            "per_page": 10
        }

        resp = requests.get(search_url, params=params, headers=headers, timeout=60)
        data = resp.json()

        repos = []
        for item in data.get("items", [])[:5]:
            repos.append({
                "name": item["full_name"],
                "description": item.get("description", "No description"),
                "stars": item.get("stargazers_count", 0),
                "url": item["html_url"],
                "language": item.get("language", "Unknown")
            })
        return repos

    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return []


def analyze_repo(repo: dict) -> str:
    """Analyze repo relevance using z.ai API"""
    if not Z_AI_API_KEY:
        return "API 키 없음"

    prompt = f"""다음 GitHub 저장소를 한국어로 간단히 요약하고, 왜 주목할 만한지 설명해줘 (2-3문장).

저장소: {repo['name']}
설명: {repo['description']}
언어: {repo['language']}
스타: {repo['stars']}

요약:"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content or "분석 실패"
    except Exception as e:
        print(f"API Error: {e}")
        return f"분석 오류: {e}"


def generate_report(repos: list) -> str:
    """Generate markdown report"""

    weekday = datetime.now().strftime("%A")

    frontmatter = f"""---
title: Tech Digest
date: {DATE}
type: resource
topics:
  - 개발
  - GitHub
source: 뉴스
---
# 📰 Tech Digest - {DATE} ({weekday})

석준님, 이번 주 GitHub Trending에서 주목할 만한 저장소들입니다.

---
"""

    content = ""
    for i, repo in enumerate(repos, 1):
        analysis = analyze_repo(repo)
        content += f"""### ✅ Item {i}: [{repo['name']}]({repo['url']})

- **설명**: {repo['description']}
- **언어**: {repo['language']} | **스타**: {repo['stars']:,}
- **분석**: {analysis}

---

"""

    content += "#type/resource #topic/개발 #source/뉴스\n"
    return frontmatter + content


def main():
    print(f"Starting Tech News - {DATE}")
    print(f"Using model: {MODEL}")
    print(f"API endpoint: {Z_AI_BASE_URL}")

    repos = fetch_github_trending()
    print(f"Fetched {len(repos)} repos")

    report = generate_report(repos)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"tech-digest-{DATE}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved: {output_file}")
    print("\n--- Report Preview ---")
    print(report[:500] + "...")


if __name__ == "__main__":
    main()

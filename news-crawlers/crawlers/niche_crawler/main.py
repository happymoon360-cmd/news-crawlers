#!/usr/bin/env python3
"""
Niche Crawler - YC RFS, Exploding Topics using z.ai Coding Plan (GLM-5)
"""

import os
import requests
from datetime import datetime
from pathlib import Path
from openai import OpenAI
import time

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


def fetch_yc_rfs() -> list:
    """Fetch Y Combinator Requests for Startups"""
    try:
        rfs_list = [
            "Retraining Workers for the AI Economy",
            "Video Generation as a Primitive",
            "The First 10-person, $100B Company",
            "Infrastructure for Multi-Agent Systems",
            "AI Native Enterprise Software"
        ]
        return [{"title": rfs, "url": "https://www.ycombinator.com/rfs"} for rfs in rfs_list]
    except Exception as e:
        print(f"Error fetching YC RFS: {e}")
        return []


def fetch_exploding_topics() -> list:
    """Fetch trending topics"""
    try:
        return [
            {"name": "AI Agent Frameworks", "growth": "+150%", "category": "Technology"},
            {"name": "No-Code Builders", "growth": "+89%", "category": "SaaS"},
            {"name": "Personal Knowledge Management", "growth": "+67%", "category": "Productivity"}
        ]
    except Exception as e:
        print(f"Error fetching Exploding Topics: {e}")
        return []


def fetch_papers_with_code() -> list:
    """Fetch trending ML papers"""
    try:
        url = "https://paperswithcode.com/api/v1/papers/"
        resp = requests.get(url, params={"ordering": "-published", "page_size": 5}, timeout=60)
        papers = []
        data = resp.json()
        for paper in data.get("results", [])[:5]:
            papers.append({
                "title": paper.get("title", "Unknown"),
                "abstract": paper.get("abstract", "")[:200],
                "url": paper.get("url", "")
            })
        return papers
    except Exception as e:
        print(f"Error fetching Papers with Code: {e}")
        return []


def generate_startup_idea(source: str, topic: str, description: str) -> str:
    """Generate micro-SaaS idea using z.ai API"""
    if not Z_AI_API_KEY:
        return "API 키 없음"

    prompt = f"""다음 트렌드/주제를 바탕으로 1인 개발자가 만들 수 있는 마이크로 SaaS 아이디어를 제안해줘.

출처: {source}
주제: {topic}
설명: {description}

다음 형식으로 답변:
1. 핵심 문제
2. 솔루션 아이디어
3. 비즈니스 기회

(각 항목 1-2문장, 한국어)"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return response.choices[0].message.content or "분석 실패"
    except Exception as e:
        print(f"API Error: {e}")
        return f"분석 오류: {e}"


def generate_report(yc_rfs: list, exploding: list, papers: list) -> str:
    """Generate markdown report"""

    frontmatter = f"""---
title: 니치 아이디어
date: {DATE}
type: resource
topics:
  - LLM
  - 스타트업
  - SaaS
source: 뉴스
---
# 🧠 전문가 분석 니치 아이디어 ({DATE})

"""

    content = ""

    if yc_rfs:
        content += "## 🚀 Y Combinator RFS (스타트업 수요)\n\n"
        for rfs in yc_rfs[:3]:
            idea = generate_startup_idea("YC RFS", rfs['title'], "Y Combinator이 요청하는 스타트업 아이디어")
            content += f"""### [{rfs['title']}]({rfs['url']})

{idea}

"""
            time.sleep(2)  # Rate limiting

    if exploding:
        content += "---\n\n## 📈 Exploding Topics (시장 트렌드)\n\n"
        for topic in exploding[:3]:
            idea = generate_startup_idea("Exploding Topics", topic['name'], f"성장률: {topic['growth']}")
            content += f"""### {topic['name']} (↑ {topic['growth']})

{idea}

"""
            time.sleep(2)

    if papers:
        content += "---\n\n## 📄 Papers With Code (신기술 응용)\n\n"
        for paper in papers[:3]:
            idea = generate_startup_idea("Papers with Code", paper['title'], paper['abstract'])
            content += f"""### [{paper['title']}]({paper['url']})

{idea}

"""
            time.sleep(2)

    content += "---\n#type/resource #topic/LLM #source/뉴스\n"
    return frontmatter + content


def main():
    print(f"Starting Niche Crawler - {DATE}")
    print(f"Using model: {MODEL}")
    print(f"API endpoint: {Z_AI_BASE_URL}")

    yc_rfs = fetch_yc_rfs()
    exploding = fetch_exploding_topics()
    papers = fetch_papers_with_code()

    print(f"YC RFS: {len(yc_rfs)}, Exploding Topics: {len(exploding)}, Papers: {len(papers)}")

    report = generate_report(yc_rfs, exploding, papers)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"니치_아이디어_{DATE}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved: {output_file}")
    print("\n--- Report Preview ---")
    print(report[:500] + "...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Trend Detector - Daily trend analysis using z.ai Coding Plan (GLM-5)
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


def fetch_google_trends(geo: str = "US") -> list:
    """Fetch trending searches from Google Trends RSS"""
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    try:
        resp = requests.get(url, timeout=60)
        trends = []
        items = resp.text.split("<item>")
        for item in items[1:11]:
            title_start = item.find("<title>")
            title_end = item.find("</title>")
            if title_start != -1 and title_end != -1:
                title = item[title_start+7:title_end]
                traffic_start = item.find("<ht:approx_traffic>")
                traffic_end = item.find("</ht:approx_traffic>")
                traffic = item[traffic_start+19:traffic_end] if traffic_start != -1 else "N/A"
                trends.append({"keyword": title, "traffic": traffic})
        return trends
    except Exception as e:
        print(f"Error fetching Google Trends: {e}")
        return []


def analyze_trend(trend_data: dict, trend_type: str) -> str:
    """Analyze why a trend is viral using z.ai API"""
    if not Z_AI_API_KEY:
        return "API 키 없음"

    prompt = f"""다음 트렌드가 왜 바이럴되었는지 한국어로 2-3문장으로 분석해줘.

트렌드 유형: {trend_type}
키워드: {trend_data.get('keyword', 'Unknown')}
검색량: {trend_data.get('traffic', 'N/A')}
날짜: {DATE}

분석:"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content or "분석 실패"
    except Exception as e:
        print(f"API Error: {e}")
        return f"분석 오류: {e}"


def generate_report(us_trends: list, kr_trends: list) -> str:
    """Generate markdown report"""

    frontmatter = f"""---
title: 트렌드 감지 리포트
date: {DATE}
type: resource
topics:
  - 키워드
  - 트렌드
source: 뉴스
---
# 🔥 급상승 트렌드 분석 - {DATE}
"""

    content = ""

    if us_trends:
        content += "## 🌍 US Trends\n\n### 📊 Google Trends\n"
        for trend in us_trends[:5]:
            analysis = analyze_trend(trend, "Google Trends US")
            content += f"""#### {trend['keyword']} (↑ {trend['traffic']})
**바이럴 이유**: {analysis}

"""

    if kr_trends:
        content += "---\n\n## 🇰🇷 KR Trends\n\n### 📊 Google Trends\n"
        for trend in kr_trends[:5]:
            analysis = analyze_trend(trend, "Google Trends KR")
            content += f"""#### {trend['keyword']} (↑ {trend['traffic']})
**바이럴 이유**: {analysis}

"""

    content += "\n---\n#type/resource #topic/키워드 #source/뉴스\n"
    return frontmatter + content


def main():
    print(f"Starting Trend Detector - {DATE}")
    print(f"Using model: {MODEL}")
    print(f"API endpoint: {Z_AI_BASE_URL}")

    us_trends = fetch_google_trends("US")
    kr_trends = fetch_google_trends("KR")

    print(f"US Trends: {len(us_trends)}, KR Trends: {len(kr_trends)}")

    report = generate_report(us_trends, kr_trends)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"트렌드_감지_{DATE}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved: {output_file}")
    print("\n--- Report Preview ---")
    print(report[:500] + "...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Weekly Summary — runs every Sunday in GitHub Actions
Reads this week's daily-digest entries and compiles a weekly summary.
"""

import os
import re
from datetime import datetime, timezone, timedelta

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now(timezone.utc)
WEEK_NUM = TODAY.isocalendar()[1]
YEAR = TODAY.year
WEEK_START = (TODAY - timedelta(days=TODAY.weekday() + 1)).strftime("%Y-%m-%d")
WEEK_END = TODAY.strftime("%Y-%m-%d")


def read_this_week_digest():
    path = os.path.join(VAULT, "inbox", "daily-digest.md")
    if not os.path.exists(path):
        return {}

    content = open(path, encoding="utf-8").read()
    # Split by day sections
    days = {}
    sections = re.split(r'\n## (\d{4}-\d{2}-\d{2})\n', content)
    for i in range(1, len(sections), 2):
        date_str = sections[i]
        body = sections[i + 1] if i + 1 < len(sections) else ""
        # Only this week
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if (TODAY - d).days <= 7:
                days[date_str] = body
        except:
            pass
    return days


def read_new_notes():
    notes_dir = os.path.join(VAULT, "notes")
    if not os.path.isdir(notes_dir):
        return []
    results = []
    for f in os.listdir(notes_dir):
        if not f.endswith(".md"):
            continue
        path = os.path.join(notes_dir, f)
        mtime = os.path.getmtime(path)
        if (TODAY.timestamp() - mtime) < 7 * 86400:
            # Read first 5 lines for title/source
            try:
                lines = open(path, encoding="utf-8").readlines()
                title = f.replace(".md", "").replace("__", "/")
                for line in lines:
                    if line.startswith("# "):
                        title = line.strip("# \n")
                        break
                results.append(title)
            except:
                results.append(f)
    return results


def build_summary(days, notes):
    lines = [f"\n## 周报 {YEAR}-W{WEEK_NUM:02d}（{WEEK_START} 至 {WEEK_END}）\n"]

    lines.append("\n### 本周 ingest 了什么\n")
    if notes:
        for n in notes:
            lines.append(f"- {n}\n")
    else:
        lines.append("- 本周无新 ingest\n")

    lines.append("\n### 本周 Claude 大事\n")
    # Extract 📰 items from all days
    news_items = []
    for body in days.values():
        section = re.search(r'### 📰.*?\n(.*?)###', body, re.DOTALL)
        if section:
            for line in section.group(1).strip().split("\n"):
                if line.startswith("- ") and line != "- 无":
                    news_items.append(line)
    if news_items:
        for item in dict.fromkeys(news_items):  # dedupe
            lines.append(item + "\n")
    else:
        lines.append("- 本周无重大新闻\n")

    lines.append("\n### 本周值得看的讨论\n")
    hn_items = []
    for body in days.values():
        section = re.search(r'### 💡.*?\n(.*?)###', body, re.DOTALL)
        if section:
            for line in section.group(1).strip().split("\n"):
                if line.startswith("- ") and line != "- 无":
                    hn_items.append(line)
    if hn_items:
        for item in dict.fromkeys(hn_items)[:5]:
            lines.append(item + "\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 新发现的 Skill/Repo\n")
    gh_items = []
    for body in days.values():
        section = re.search(r'### 🔧.*?\n(.*?)###', body, re.DOTALL)
        if section:
            for line in section.group(1).strip().split("\n"):
                if line.startswith("- ") and line != "- 无":
                    gh_items.append(line)
    if gh_items:
        for item in dict.fromkeys(gh_items)[:5]:
            lines.append(item + "\n")
    else:
        lines.append("- 无\n")

    lines.append(f"\n*本周共 {len(days)} 天有摘要，ingest 了 {len(notes)} 份笔记*\n")
    lines.append("\n---\n")
    return "".join(lines)


def main():
    print(f"Building weekly summary for W{WEEK_NUM}")
    days = read_this_week_digest()
    notes = read_new_notes()
    summary = build_summary(days, notes)

    out_path = os.path.join(VAULT, "meta", "weekly-summary.md")
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(summary)

    print(summary)


if __name__ == "__main__":
    main()

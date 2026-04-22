#!/usr/bin/env python3
"""
Daily Claude Digest — runs in GitHub Actions (cloud, no local computer needed)
Discovers new Claude content from multiple sources and appends to daily-digest.md
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

GH_TOKEN = os.environ.get("GH_TOKEN", "")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CUTOFF = int(time.time()) - 86400  # 24 hours ago

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    if GH_TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"token {GH_TOKEN}")
    req.add_header("User-Agent", "claude-learning-digest/1.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()) if "json" in r.headers.get("Content-Type", "") else r.read().decode()
    except Exception as e:
        return None


def fetch_anthropic_news():
    """Read Anthropic news page for recent posts."""
    html = fetch("https://www.anthropic.com/news")
    if not html:
        return []
    # Extract titles + links from the news listing
    items = []
    pattern = r'href="(/news/[^"]+)"[^>]*>.*?<[^>]+>([^<]{10,})</'
    for m in re.finditer(pattern, html, re.DOTALL):
        path, title = m.group(1), m.group(2).strip()
        title = re.sub(r'\s+', ' ', title)
        if len(title) > 15 and path not in [i[1] for i in items]:
            items.append((title, "https://www.anthropic.com" + path))
        if len(items) >= 5:
            break
    return items[:3]


def fetch_hn():
    """HN posts about Claude in past 24h, points > 20."""
    data = fetch(
        f"https://hn.algolia.com/api/v1/search?query=claude+anthropic"
        f"&tags=story&numericFilters=created_at_i>{CUTOFF},points>20&hitsPerPage=5"
    )
    if not data or "hits" not in data:
        return []
    results = []
    for h in data["hits"]:
        title = h.get("title", "")
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        pts = h.get("points", 0)
        results.append((title, url, pts))
    return results


def fetch_github_repos():
    """New/updated Claude skill repos in past 24h."""
    data = fetch(
        "https://api.github.com/search/repositories"
        "?q=claude+skill+in:name,description&sort=updated&order=desc&per_page=15"
    )
    if not data or "items" not in data:
        return []

    # Load already-ingested repos
    originals_dir = os.path.join(VAULT, "originals")
    known = set()
    if os.path.isdir(originals_dir):
        known = {d.replace("__", "/") for d in os.listdir(originals_dir)}

    results = []
    for item in data["items"]:
        name = item["full_name"]
        updated = item.get("updated_at", "")
        stars = item.get("stargazers_count", 0)
        desc = item.get("description") or ""

        # Only past 24h
        if updated:
            try:
                t = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if t.timestamp() < CUTOFF:
                    continue
            except:
                pass

        if name in known:
            continue

        results.append((name, f"https://github.com/{name}", stars, desc))
        if len(results) >= 5:
            break
    return results


def read_inbox():
    """Read unprocessed URLs from inbox/urls.md"""
    path = os.path.join(VAULT, "inbox", "urls.md")
    if not os.path.exists(path):
        return [], []

    lines = open(path, encoding="utf-8").readlines()
    pending = []
    new_lines = []
    for line in lines:
        if line.strip().startswith("-") and "[done" not in line and "http" in line:
            url_match = re.search(r'https?://\S+', line)
            note_match = re.search(r'\|\s*(.+)$', line.rstrip())
            if url_match:
                url = url_match.group(0).rstrip(')')
                note = note_match.group(1).strip() if note_match else ""
                pending.append((url, note))
                # Mark as done
                new_lines.append(line.rstrip() + f" [done {TODAY}]\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Write back with done markers
    if pending:
        open(path, "w", encoding="utf-8").writelines(new_lines)

    return pending, new_lines


def build_digest(anthropic, hn, github, inbox):
    lines = [f"\n## {TODAY}\n"]

    # Claude news
    lines.append("\n### 📰 Claude 最新消息（过去24小时）\n")
    if anthropic:
        for title, url in anthropic:
            lines.append(f"- [{title}]({url})\n")
    else:
        lines.append("- 无\n")

    # HN
    lines.append("\n### 💡 HN 讨论（过去24小时）\n")
    if hn:
        for title, url, pts in hn:
            lines.append(f"- [{title}]({url}) — {pts} points\n")
    else:
        lines.append("- 无\n")

    # GitHub
    lines.append("\n### 🔧 新 Skill/Prompt repo（过去24小时有更新）\n")
    if github:
        for name, url, stars, desc in github:
            star_str = f" ⭐{stars}" if stars else ""
            desc_str = f" — {desc[:60]}" if desc else ""
            lines.append(f"- [{name}]({url}){star_str}{desc_str}\n")
    else:
        lines.append("- 无\n")

    # Inbox
    lines.append("\n### 📥 Inbox 处理\n")
    if inbox:
        for url, note in inbox:
            note_str = f" — {note}" if note else ""
            lines.append(f"- {url}{note_str} → 待人工 ingest\n")
    else:
        lines.append("- inbox 无待处理链接\n")

    lines.append("\n---\n")
    return "".join(lines)


def main():
    print(f"Running digest for {TODAY} (cutoff: {CUTOFF})")

    print("Fetching Anthropic news...")
    anthropic = fetch_anthropic_news()
    print(f"  → {len(anthropic)} items")

    print("Fetching HN...")
    hn = fetch_hn()
    print(f"  → {len(hn)} items")

    print("Fetching GitHub repos...")
    github = fetch_github_repos()
    print(f"  → {len(github)} items")

    print("Reading inbox...")
    inbox, _ = read_inbox()
    print(f"  → {len(inbox)} pending URLs")

    digest = build_digest(anthropic, hn, github, inbox)

    digest_path = os.path.join(VAULT, "inbox", "daily-digest.md")
    with open(digest_path, "a", encoding="utf-8") as f:
        f.write(digest)

    print(f"\nDigest written to {digest_path}")
    print("\n" + digest)


if __name__ == "__main__":
    main()

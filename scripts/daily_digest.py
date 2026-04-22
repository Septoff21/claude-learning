#!/usr/bin/env python3
"""
Daily Claude Digest — runs in GitHub Actions (cloud, no local computer needed)
Discovers new Claude content from multiple sources and appends to daily-digest.md
Sources: Anthropic blog, HN, GitHub, Reddit r/ClaudeAI, YouTube channels
"""

import json
import os
import re
import time
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

GH_TOKEN = os.environ.get("GH_TOKEN", "")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CUTOFF = int(time.time()) - 86400  # 24 hours ago

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# YouTube channels to monitor (channel_id -> display name)
YOUTUBE_CHANNELS = {
    "UCod1PxJAu3t0Td1XmMF8lCA": "Anthropic",
    "UCbmNph6atAoGfqLoCL_duAg": "AI Explained",
    "UCNQ04TBsHjJvEKOcwm2hkHg": "Matthew Berman",
    "UCX6OQ3DkcsbYNE6H8uQQuVA": "3Blue1Brown",  # occasionally covers AI
}

# Auto-ingest candidates (quality >= 4), written to file for auto_ingest.py
AUTO_INGEST_FILE = os.path.join(VAULT, "inbox", ".auto_ingest_candidates.json")


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    if GH_TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"token {GH_TOKEN}")
    req.add_header("User-Agent", "claude-learning-digest/1.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            ct = r.headers.get("Content-Type", "")
            raw = r.read()
            if "json" in ct:
                return json.loads(raw)
            return raw.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  fetch error {url[:60]}: {e}")
        return None


def fetch_anthropic_news():
    html = fetch("https://www.anthropic.com/news")
    if not html:
        return []
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
    data = fetch(
        f"https://hn.algolia.com/api/v1/search?query=claude+anthropic"
        f"&tags=story&numericFilters=created_at_i>{CUTOFF},points>20&hitsPerPage=5"
    )
    if not data or "hits" not in data:
        return []
    return [
        (h.get("title", ""), h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}", h.get("points", 0))
        for h in data["hits"]
    ]


def fetch_reddit():
    """r/ClaudeAI new posts in past 24h, upvotes > 10."""
    results = []
    for subreddit in ["ClaudeAI", "anthropic"]:
        data = fetch(f"https://www.reddit.com/r/{subreddit}/new.json?limit=10")
        if not data or "data" not in data:
            continue
        for post in data["data"].get("children", []):
            p = post.get("data", {})
            created = p.get("created_utc", 0)
            ups = p.get("ups", 0)
            title = p.get("title", "")
            url = p.get("url", "")
            permalink = "https://reddit.com" + p.get("permalink", "")

            if created < CUTOFF:
                continue
            if ups < 10:
                continue
            # Skip image/self posts with no external link
            link = url if url.startswith("http") and "reddit.com" not in url else permalink
            results.append((f"r/{subreddit}: {title}", link, ups))
        if len(results) >= 5:
            break
    return results[:5]


def fetch_youtube():
    """Check YouTube channel RSS feeds for videos in past 24h."""
    results = []
    for channel_id, name in YOUTUBE_CHANNELS.items():
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        xml_str = fetch(rss_url)
        if not xml_str:
            continue
        try:
            root = ET.fromstring(xml_str)
            ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
            for entry in root.findall("atom:entry", ns)[:5]:
                published = entry.findtext("atom:published", "", ns)
                title = entry.findtext("atom:title", "", ns)
                link_el = entry.find("atom:link", ns)
                video_url = link_el.get("href", "") if link_el is not None else ""

                if published:
                    try:
                        pub_ts = datetime.fromisoformat(published.replace("Z", "+00:00")).timestamp()
                        if pub_ts < CUTOFF:
                            continue
                    except:
                        continue

                # Filter: only Claude/Anthropic/AI related titles
                if any(kw in title.lower() for kw in ["claude", "anthropic", "llm", "ai agent", "mcp", "prompt"]):
                    results.append((f"{name}: {title}", video_url))
        except Exception as e:
            print(f"  YouTube parse error ({name}): {e}")
    return results[:4]


def fetch_github_repos():
    """New/updated Claude skill repos in past 24h."""
    data = fetch(
        "https://api.github.com/search/repositories"
        "?q=claude+skill+in:name,description&sort=updated&order=desc&per_page=20"
    )
    if not data or "items" not in data:
        return []

    originals_dir = os.path.join(VAULT, "originals")
    known = set()
    if os.path.isdir(originals_dir):
        known = {d.replace("__", "/") for d in os.listdir(originals_dir)}

    results = []
    auto_candidates = []

    for item in data["items"]:
        name = item["full_name"]
        updated = item.get("updated_at", "")
        stars = item.get("stargazers_count", 0)
        desc = item.get("description") or ""

        if updated:
            try:
                t = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if t.timestamp() < CUTOFF:
                    continue
            except:
                pass

        if name in known:
            continue

        # Estimate quality from stars + description length
        quality = 2
        if stars >= 50:
            quality = 3
        if stars >= 200 or (stars >= 50 and len(desc) > 80):
            quality = 4

        entry = (name, f"https://github.com/{name}", stars, desc, quality)
        results.append(entry)

        if quality >= 4:
            auto_candidates.append({"name": name, "url": f"https://github.com/{name}", "stars": stars, "desc": desc, "quality": quality})

        if len(results) >= 6:
            break

    # Write auto-ingest candidates for auto_ingest.py
    if auto_candidates:
        existing = []
        if os.path.exists(AUTO_INGEST_FILE):
            try:
                existing = json.loads(open(AUTO_INGEST_FILE).read())
            except:
                pass
        existing_urls = {c["url"] for c in existing}
        new_ones = [c for c in auto_candidates if c["url"] not in existing_urls]
        if new_ones:
            open(AUTO_INGEST_FILE, "w").write(json.dumps(existing + new_ones, indent=2))
            print(f"  {len(new_ones)} auto-ingest candidate(s) queued")

    return results


def read_inbox():
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
                new_lines.append(line.rstrip() + f" [done {TODAY}]\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if pending:
        open(path, "w", encoding="utf-8").writelines(new_lines)

    return pending, new_lines


def build_digest(anthropic, hn, reddit, youtube, github, inbox):
    lines = [f"\n## {TODAY}\n"]

    lines.append("\n### 📰 Claude 最新消息（过去24小时）\n")
    if anthropic:
        for title, url in anthropic:
            lines.append(f"- [{title}]({url})\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 💡 HN 讨论（过去24小时）\n")
    if hn:
        for title, url, pts in hn:
            lines.append(f"- [{title}]({url}) — {pts}pts\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 🟠 Reddit（过去24小时）\n")
    if reddit:
        for title, url, ups in reddit:
            lines.append(f"- [{title}]({url}) — ↑{ups}\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 📺 YouTube（过去24小时）\n")
    if youtube:
        for title, url in youtube:
            lines.append(f"- [{title}]({url})\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 🔧 新 Skill/Prompt repo（过去24小时）\n")
    if github:
        for name, url, stars, desc, quality in github:
            auto = " 🤖auto-ingest" if quality >= 4 else ""
            star_str = f" ⭐{stars}" if stars else ""
            desc_str = f" — {desc[:60]}" if desc else ""
            lines.append(f"- [{name}]({url}){star_str}{desc_str}{auto}\n")
    else:
        lines.append("- 无\n")

    lines.append("\n### 📥 Inbox 处理\n")
    if inbox:
        for url, note in inbox:
            note_str = f" — {note}" if note else ""
            lines.append(f"- {url}{note_str}\n")
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

    print("Fetching Reddit...")
    reddit = fetch_reddit()
    print(f"  → {len(reddit)} items")

    print("Fetching YouTube...")
    youtube = fetch_youtube()
    print(f"  → {len(youtube)} items")

    print("Fetching GitHub repos...")
    github = fetch_github_repos()
    print(f"  → {len(github)} items")

    print("Reading inbox...")
    inbox, _ = read_inbox()
    print(f"  → {len(inbox)} pending URLs")

    digest = build_digest(anthropic, hn, reddit, youtube, github, inbox)

    digest_path = os.path.join(VAULT, "inbox", "daily-digest.md")
    with open(digest_path, "a", encoding="utf-8") as f:
        f.write(digest)

    print(f"\nDigest written.")
    print(digest)


if __name__ == "__main__":
    main()

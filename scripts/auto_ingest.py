#!/usr/bin/env python3
"""
Auto Ingest — runs after daily_digest.py in GitHub Actions
For repos with quality >= 4: clones originals + creates skeleton note.
Full distillation still requires manual /ingest in Claude Code.
"""

import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone

GH_TOKEN = os.environ.get("GH_TOKEN", "")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATES_FILE = os.path.join(VAULT, "inbox", ".auto_ingest_candidates.json")


def fetch_json(url):
    req = urllib.request.Request(url)
    if GH_TOKEN:
        req.add_header("Authorization", f"token {GH_TOKEN}")
    req.add_header("User-Agent", "claude-learning/1.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except:
        return None


def get_readme(owner_repo):
    data = fetch_json(f"https://api.github.com/repos/{owner_repo}/readme")
    if not data:
        return ""
    import base64
    try:
        return base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
    except:
        return ""


def clone_repo(url, dest):
    if os.path.exists(dest):
        print(f"  Already exists: {dest}")
        return False
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, dest],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  Clone failed: {result.stderr[:200]}")
        return False
    # Remove .git to freeze snapshot
    git_dir = os.path.join(dest, ".git")
    if os.path.exists(git_dir):
        subprocess.run(["git", "-C", dest, "rev-parse", "HEAD"], capture_output=True, text=True)
        subprocess.run(["rm", "-rf", git_dir])
    return True


def detect_type(readme, desc):
    text = (readme + desc).lower()
    if "mcp" in text or "server" in text:
        return "tools-mcp"
    if "workflow" in text or "agent" in text or "orchestrat" in text:
        return "workflows"
    if "skill" in text or "prompt" in text:
        return "skills"
    return "skills"


def write_skeleton_note(name, url, stars, desc, readme, quality):
    owner, repo = name.split("/", 1)
    slug = f"{owner}__{repo}"
    note_path = os.path.join(VAULT, "notes", f"{slug}.md")

    if os.path.exists(note_path):
        print(f"  Note already exists: {note_path}")
        return

    content_type = detect_type(readme, desc)
    readme_excerpt = readme[:500].strip() if readme else ""

    note = f"""---
source: {url}
ingested_at: {TODAY}
type: {content_type}
quality: {quality}
stars: {stars}
tags: []
tried: false
auto_ingested: true
---

# {repo}

## 一句话
{desc or "（待补充）"}

## 核心内容
*(Auto-ingested — run `/ingest {url}` in Claude Code for full distillation)*

### README 摘要（前500字）
{readme_excerpt}

## 可以怎么用
（待手动蒸馏）

## 和已有内容的差异
（待手动蒸馏）

## 原文位置
`originals/{slug}/`
"""
    os.makedirs(os.path.dirname(note_path), exist_ok=True)
    open(note_path, "w", encoding="utf-8").write(note)
    print(f"  Note written: {note_path}")


def update_moc(name, note_type):
    moc_path = os.path.join(VAULT, "moc", "by-type.md")
    if not os.path.exists(moc_path):
        return
    content = open(moc_path, encoding="utf-8").read()
    owner, repo = name.split("/", 1)
    slug = f"{owner}__{repo}"
    link = f"- [{name}](../notes/{slug}.md) — auto-ingested 🤖"
    section = f"## {note_type}"
    if link in content:
        return
    if section in content:
        content = content.replace(section, f"{section}\n{link}", 1)
        open(moc_path, "w", encoding="utf-8").write(content)


def main():
    if not os.path.exists(CANDIDATES_FILE):
        print("No auto-ingest candidates.")
        return

    candidates = json.loads(open(CANDIDATES_FILE).read())
    if not candidates:
        print("Candidates file empty.")
        return

    print(f"Processing {len(candidates)} auto-ingest candidate(s)...")
    processed = []

    for c in candidates:
        name = c["name"]
        url = c["url"]
        stars = c.get("stars", 0)
        desc = c.get("desc", "")
        quality = c.get("quality", 4)

        owner, repo = name.split("/", 1)
        slug = f"{owner}__{repo}"
        dest = os.path.join(VAULT, "originals", slug)

        print(f"\nProcessing: {name} (q:{quality} ⭐{stars})")

        cloned = clone_repo(url, dest)
        readme = get_readme(name)
        write_skeleton_note(name, url, stars, desc, readme, quality)
        content_type = detect_type(readme, desc)
        update_moc(name, content_type)

        processed.append(name)

    # Clear processed candidates
    open(CANDIDATES_FILE, "w").write("[]")
    print(f"\nDone. Auto-ingested: {processed}")


if __name__ == "__main__":
    main()

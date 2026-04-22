#!/usr/bin/env python3
"""
Mark a note as tried — updates frontmatter tried:true + adds personal rating/comment.
Triggered via GitHub Actions workflow_dispatch.
"""

import os
import re
from datetime import datetime, timezone

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

slug = os.environ.get("NOTE_SLUG", "")
rating = os.environ.get("RATING", "3")
comment = os.environ.get("COMMENT", "")

if not slug:
    print("ERROR: NOTE_SLUG is required")
    exit(1)

note_path = os.path.join(VAULT, "notes", f"{slug}.md")
if not os.path.exists(note_path):
    print(f"ERROR: Note not found: {note_path}")
    exit(1)

content = open(note_path, encoding="utf-8").read()

# Update tried: false → true
content = re.sub(r'^tried: false', f'tried: true', content, flags=re.MULTILINE)

# Add personal_rating and tried_at if not present
if "personal_rating:" not in content:
    content = re.sub(
        r'^tried: true',
        f'tried: true\npersonal_rating: {rating}\ntried_at: {TODAY}',
        content, flags=re.MULTILINE
    )

# Append comment if provided
if comment:
    tried_section = "\n## 使用体验\n"
    entry = f"**{TODAY}** (⭐{rating}/5): {comment}\n"
    if tried_section in content:
        content = content.replace(tried_section, tried_section + entry)
    else:
        content = content.rstrip() + f"\n{tried_section}{entry}"

open(note_path, "w", encoding="utf-8").write(content)
print(f"Marked {slug} as tried (rating: {rating}/5)")
if comment:
    print(f"Comment: {comment}")

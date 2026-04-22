#!/usr/bin/env python3"""
Telegram Inbox — runs every 30min in GitHub Actions
Polls Telegram bot for new messages, extracts URLs, appends to inbox/urls.md
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFSET_FILE = os.path.join(VAULT, "inbox", ".tg_offset")
URLS_FILE = os.path.join(VAULT, "inbox", "urls.md")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def tg(method, params=None):
    url = f"{BASE}/{method}"
    if params:
        data = json.dumps(params).encode()
        req = urllib.request.Request(url, data=data,
                                     headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def load_offset():
    if os.path.exists(OFFSET_FILE):
        return int(open(OFFSET_FILE).read().strip())
    return 0


def save_offset(offset):
    open(OFFSET_FILE, "w").write(str(offset))


def extract_urls(text):
    return re.findall(r'https?://\S+', text or "")


def append_to_inbox(urls, note="via Telegram"):
    with open(URLS_FILE, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(f"- {url} | {note}\n")
    print(f"Added {len(urls)} URL(s) to inbox")


def reply(chat_id, text):
    try:
        tg("sendMessage", {"chat_id": chat_id, "text": text})
    except:
        pass


def main():
    offset = load_offset()
    print(f"Polling Telegram (offset={offset})")

    result = tg("getUpdates", {"offset": offset, "timeout": 5})
    updates = result.get("result", [])
    print(f"Got {len(updates)} update(s)")

    new_offset = offset
    all_urls = []

    for update in updates:
        new_offset = max(new_offset, update["update_id"] + 1)
        msg = update.get("message", {})
        text = msg.get("text", "") or msg.get("caption", "")
        chat_id = msg.get("chat", {}).get("id")

        urls = extract_urls(text)
        if urls:
            all_urls.extend(urls)
            if chat_id:
                reply(chat_id, f"✅ 收到 {len(urls)} 个链接，已加入 inbox")
        elif text and chat_id:
            reply(chat_id, "📎 发 URL 给我，我帮你加进 claude-learning inbox")

    if all_urls:
        append_to_inbox(all_urls)

    save_offset(new_offset)
    print(f"Done. New offset: {new_offset}")


if __name__ == "__main__":
    main()

# Claude Learning

> Personal knowledge vault for everything Claude — skills, prompts, workflows, patterns, and distilled insights.
> Automatically discovers, filters, and distills the best Claude-related content daily.

**Live site**: [septoff21.github.io/claude-learning](https://septoff21.github.io/claude-learning)

---

## What This Is

A self-updating knowledge base that:
1. **Discovers** new Claude-related content daily (GitHub, HN, Anthropic blog)
2. **Collects** URLs you send via Telegram bot
3. **Distills** repos and articles into structured notes (using `/ingest`)
4. **Publishes** everything as a browsable website automatically

---

## Repository Structure

```
claude-learning/
├── notes/              # Distilled notes — one file per source
├── originals/          # Full snapshots of ingested repos (frozen at ingest time)
├── moc/                # Map of Content — index by type and use case
├── meta/
│   ├── _rubric.md      # Filtering criteria (living doc)
│   ├── _learnings.md   # Meta-insights distilled from content
│   ├── sources.md      # Discovery source config
│   └── weekly-summary.md
├── inbox/
│   ├── urls.md         # Manual URL queue
│   ├── _pending.md     # Triage queue from scans
│   └── daily-digest.md # Auto-generated daily digest
├── scripts/
│   ├── daily_digest.py    # Daily multi-source scan
│   ├── weekly_summary.py  # Weekly rollup
│   └── telegram_inbox.py  # Telegram bot poller
├── .claude/commands/   # Claude Code slash commands
│   ├── ingest.md       # /ingest <url>
│   ├── ingest-youtube.md
│   └── triage-inbox.md
└── .github/workflows/
    ├── daily-digest.yml    # Weekdays 9pm SGT
    ├── weekly-summary.yml  # Sundays 8pm SGT
    ├── telegram-inbox.yml  # Every 30 min
    └── publish-site.yml    # Auto-publishes to GitHub Pages
```

---

## How It Works

### Automatic (no action needed)

| Schedule | What happens |
|----------|-------------|
| Every 30 min | Telegram bot polls for new URLs from owner |
| Weekdays 9pm SGT | Scans Anthropic blog, HN, GitHub for new Claude content |
| Sundays 8pm SGT | Compiles weekly summary from daily digests |
| On every push to `notes/` | Rebuilds and deploys the website |

### Manual

```
# Ingest any URL (GitHub repo, YouTube video, article)
/ingest <url>

# Process pending URLs in inbox
/triage-inbox
```

---

## Content Types

| Folder / Tag | What's stored |
|---|---|
| `skills` | Structured Claude Code skills with frontmatter |
| `prompts` | System prompts, personas |
| `workflows` | Multi-step agent patterns |
| `patterns` | Design principles, anti-patterns, insights |
| `tools-mcp` | MCP server definitions |
| `sdk-examples` | Anthropic SDK code snippets |
| `youtube` | Distilled video transcripts |
| `evals` | Testing and benchmark approaches |

---

## Note Format

Every distilled note follows this structure:

```markdown
---
source: <url>
ingested_at: YYYY-MM-DD
type: skills | prompts | workflows | ...
quality: 1-5
tags: []
tried: false
---

# Title

## One-liner
## Core content (≤200 words)
## Highlights
## How to use
## Difference from existing content
```

---

## Adding URLs

Send any URL to the Telegram bot `@dm54_claudebot`.
The bot only accepts messages from the owner. Unauthorized messages are silently ignored.

Or add directly to `inbox/urls.md`:
```
- https://example.com | optional note
```

---

## Secrets & Security

All secrets are stored in **GitHub Secrets**, never in code or files:

| Secret | Purpose |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot authentication |
| `TELEGRAM_OWNER_ID` | Whitelist — only this chat ID can send URLs |

The `GITHUB_TOKEN` (built-in) is used for all repo write operations. No external API keys required.

---

## Roadmap

### Now (v1 — complete)
- [x] Vault structure with Obsidian support
- [x] `/ingest` command (GitHub, YouTube, articles)
- [x] Daily digest (Anthropic blog + HN + GitHub)
- [x] Weekly summary
- [x] Telegram bot inbox
- [x] GitHub Actions cloud automation (no local computer needed)
- [x] Quartz site published to GitHub Pages

### Next (v2)
- [ ] Reddit source (r/ClaudeAI) in daily digest
- [ ] YouTube channel monitoring (Anthropic, AI Explained)
- [ ] Auto-ingest for quality ≥ 4 (skip manual approval)
- [ ] Full-text search across all notes
- [ ] `tried: true` workflow — mark skills you've actually tested

### Future (v3)
- [ ] Visual skill map / graph view
- [ ] Side-by-side comparison of similar skills
- [ ] Personal annotation layer on top of originals
- [ ] Export as PDF learning guide
- [ ] CLI tool: `claude-learn search <query>`

---

## Local Setup (optional)

This repo is designed to run entirely in the cloud. Local setup is only needed if you want to use Claude Code slash commands.

```bash
git clone https://github.com/Septoff21/claude-learning
cd claude-learning
# Open in Obsidian: File → Open Vault → select this folder
```

Requires: Claude Code CLI, Git, Python 3.

---

*Auto-updated daily. Last digest: see [inbox/daily-digest.md](inbox/daily-digest.md)*

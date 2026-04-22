# claude-learning

Personal Claude knowledge vault: 发现、过滤、蒸馏一切 Claude 相关的好东西。

## 结构

```
originals/          ← 原文快照（浅克隆，永久保存）
notes/              ← 蒸馏笔记（200字 + 精选 + 用法）
inbox/
  urls.md           ← 平时丢链接的地方
  _pending.md       ← 待审核队列
moc/                ← Map of Content（按类型 / 用途索引）
meta/
  _rubric.md        ← 筛选标准（活文档）
  _learnings.md     ← 元知识沉淀
.claude/commands/   ← Claude Code slash commands
```

## 命令

| 命令 | 用途 |
|------|------|
| `/ingest-repo <url>` | 把一个 repo ingest 进 vault |
| `/triage-inbox` | 处理 inbox/urls.md 里的链接 |
| `/weekly-scan` | 自动发现新 repo（定时任务用） |

## 工作流

1. 看到好东西 → 粘到 `inbox/urls.md`
2. 随时跑 `/triage-inbox` → 打分 → 审核 `_pending.md`
3. 决定要的 → `/ingest-repo <url>`
4. 每周自动扫描 → PR 供审核

## Obsidian

直接用 Obsidian 打开此文件夹，建议开启：
- Git plugin（提交/推送）
- Dataview plugin（查询 frontmatter）
- Templates plugin

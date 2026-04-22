# Sources — 发现源配置

weekly-scan 从这些源主动发现新内容。每个源标注频率和优先级。

---

## GitHub（主力）

**搜索关键词**（gh CLI）：
- `"claude skill"` — skill 集合
- `"claude prompt workflow"` — 工作流
- `"anthropic cookbook"` — 官方示例
- `"claude code MCP"` — MCP 服务器

**官方 repo 监控**（看新 commit）：
- `anthropics/anthropic-cookbook`
- `anthropics/claude-code`
- `anthropics/anthropic-sdk-python`

---

## YouTube（视频）

**频道监控**（每周看最新 1-2 个视频）：

| 频道 | URL | 类型 |
|------|-----|------|
| Anthropic 官方 | https://www.youtube.com/@anthropic | 官方发布、研究讲座 |
| AI Explained | https://www.youtube.com/@aiexplained-official | Claude 深度解析 |
| Matthew Berman | https://www.youtube.com/@matthew_berman | 新模型测评 |
| Fireship | https://www.youtube.com/@Fireship | 快速技术概览 |

**关键词搜索**（YouTube 搜索 API 替代方案，用 yt-dlp）：
- 每周搜 `"Claude" "Anthropic"` 最新视频，看标题判断是否值得 ingest

**工具**：`yt-dlp`（已安装）
```
C:/Users/algov/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/Scripts/yt-dlp.exe
```

---

## Hacker News（讨论）

**API**（免费，无需 key）：
```
https://hn.algolia.com/api/v1/search?query=claude+anthropic&tags=story&numericFilters=created_at_i>TIMESTAMP
```

筛选标准：points > 50，评论 > 20，最近 7 天内。

重点关注：Show HN、Ask HN、技术深度帖，忽略新闻聚合类。

---

## Reddit

**子版块**（Reddit JSON API，无需 key）：
- `https://www.reddit.com/r/ClaudeAI/new.json?limit=20`
- `https://www.reddit.com/r/artificial/search.json?q=claude&sort=new&limit=10`
- `https://www.reddit.com/r/LocalLLaMA/search.json?q=claude+anthropic&sort=new&limit=10`

筛选：upvotes > 30，最近 7 天，忽略纯抱怨帖和无实质内容的截图帖。

---

## Anthropic 官方

- **Blog**：WebFetch `https://www.anthropic.com/news` — 看新发布
- **Docs 更新**：WebFetch `https://docs.anthropic.com/` — 关注新功能文档
- **Research**：WebFetch `https://www.anthropic.com/research` — 论文和技术报告

---

## 手动 inbox（最重要）

你自己在 `inbox/urls.md` 丢进来的链接，优先级最高，每次 triage 必处理。

---

## 暂不处理的源

- **X/Twitter**：无免费 API，成本高，暂跳过
- **付费 Newsletter**：手动复制粘贴再丢 inbox
- **微信公众号**：暂跳过

# Weekly Summary

每周日自动生成，汇总本周摘要。

---

## 周报 2026-W17（2026-04-20 至 2026-04-26）

### 本周 ingest 了什么

- **forrestchang/andrej-karpathy-skills** — 把 Karpathy 观察到的 LLM 四大编码痛点浓缩成可直接安装的 SKILL，核心是"给成功标准，不给操作指令"
- **npow/claude-skills** — 以"协调者不自我评审"为铁律的多智体编排技能集，autopilot 的 Phase gate 结构是复杂任务的最佳参考框架
- **KirKruglov/claude-skills-kit** — 29 个面向 PM / 非技术用户的 skill，每个都是四件套（SKILL + README + INSTALL + USER-GUIDE），打包规范是目前最完整的
- **megabytespace/claude-skills** — "一行 prompt 生产 SaaS"的全链路 skill 系统（14 分类 66 模块），强绑定 Cloudflare Workers 技术栈，借鉴架构思路为主

### 本周 Claude 大事

本周 daily-digest 暂无自动抓取条目（digest agent 尚未产生输出）。

### 本周学到的新用法

1. **协调者不评判原则**：多步 AI 任务中，协调者只编排，评判必须委托给独立 agent 或独立会话——避免"自我批准"漏洞。实操：任何重要任务完成后，新开一个无上下文的会话来评审结果。

2. **可验证退出条件**：写 Claude 任务时在最后加"完成标准：……"比写"做 X"更有效——AI 会循环验证直到满足条件，而不是猜什么叫"做好了"。

### 待处理

`inbox/urls.md` 中还有 **1 条**未处理链接：`alchaincyf/huashu-design`

### 下周值得关注

1. **实际试用 4 个 repo 中的精选 skill**：npow 的 `autopilot`、KirKruglov 的 `context-builder-cowork`、karpathy-skills 的 CLAUDE.md——都还未 tried，试过才知道哪个真好用。
2. **triage inbox URL**：处理 `alchaincyf/huashu-design`，看是否值得 ingest 进 notes。

## 周报 2026-W21（2026-05-17 至 2026-05-24）

### 本周 ingest 了什么
- antigravity-awesome-skills
- KirKruglov/claude-skills-kit
- agencycli
- open-design
- everything-claude-code
- megabytespace/claude-skills
- andrej-karpathy-skills
- npow/claude-skills
- ring

### 本周 Claude 大事
- [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)

### 本周値得看的讨论
- 无

### 新发现的 Skill/Repo
- [nguyenthuhien-web/claude-skills-seongon](https://github.com/nguyenthuhien-web/claude-skills-seongon) — 3 Claude Code skills cho content SEO
- [kk-machinify/claude-config](https://github.com/kk-machinify/claude-config) — Personal Claude Code config: skills, agents, settings (WIP)
- [zbynekdrlik/airuleset](https://github.com/zbynekdrlik/airuleset) ⭐1 — Claude Code configuration management — centralized rules, sk
- [chrismccoy/skills](https://github.com/chrismccoy/skills) ⭐1 — Claude Code plugin marketplace — WordPress theme converter +
- [arbelamram/claude-code-reviewer](https://github.com/arbelamram/claude-code-reviewer) — AI-powered code reviewer skill for GitHub PRs using Claude

*本周共 5 天有摘要，ingest 了 9 份笔记*

---

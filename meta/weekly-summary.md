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

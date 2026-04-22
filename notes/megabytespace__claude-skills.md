---
source: https://github.com/megabytespace/claude-skills
source_commit: e5677852df7a504657cb43a8cf1f9350f3db81f7
ingested_at: 2026-04-22
type: skills
quality: 3
tags: [saas, fullstack, cloudflare, orchestration, operating-system, autonomous]
tried: false
---

# megabytespace/claude-skills

## 一句话

以"一行 prompt 生产 SaaS"为目标的全链路 skill 系统，有强主见的技术栈（Cloudflare Workers）和极度自主的 AI 决策哲学。

## 核心内容

这个 repo 不是一堆独立 skill，而是一套**完整的 AI 原生开发操作系统**，14 个分类 66 子模块串成一条流水线：

```
操作系统层（01）→ 目标/简报（02）→ 规划/研究（03）→ 偏好/记忆（04）
→ 架构/技术栈（05）→ 构建循环（06）→ QA/验证（07）→ 部署（08）
→ 品牌/内容（09）→ 设计系统（10）→ 动效（11）→ 媒体编排（12）
→ 可观测性（13）→ 创意引擎（14）
```

**最有价值的模块**：
- `01-operating-system`：Prime Directive 层，控制整体自主度。"不提供选项，直接选最优方案实现"——极度自主哲学
- `autonomous-orchestrator`：并行生成子 agent，独立执行互不依赖的工作流
- `04-preference-and-memory`：`brian-decision-model.md` 是一套个性化决策偏好模型，有意思但高度个人化
- `MASTER_PROMPT.md`：整套系统的入口 prompt，可直接研究其组织方式

**评分 3 而非 4 的原因**：技术栈强绑定 Cloudflare Workers + Coolify + 特定 MCP 组合。离开这个栈很多内容不适用。

## 精选文件

- `01-operating-system/SKILL.md` — 自主决策哲学和 Autonomy Rules 设计，可借鉴思路
- `01-operating-system/autonomous-orchestrator.md` — 并行 agent 编排的具体实现模式
- `MASTER_PROMPT.md` — 整套系统入口，研究大型 skill 系统如何组织
- `_router.md` — 路由层设计，多 skill 协调时如何分流

## 可以怎么用

**借鉴，不是直接用**：

- 看 `autonomous-orchestrator.md` 的并行 agent 模式 → 应用到自己的多任务场景
- 看 `01-operating-system/SKILL.md` 的"Do Without Asking"列表 → 思考自己的 AI 自主度边界在哪
- 看 14 层分类结构 → 如果要建大型 skill 系统，这个分层可作参考架构

直接用需要先有 Cloudflare Workers 环境和配套 MCP 服务器。

## 和已有内容的差异

比 npow 更重、更固执。npow 是通用编排框架，megabytespace 是特定技术栈下的完整 SaaS 工厂。规模最大、最自以为是，但也最完整。

## 原文位置

`originals/megabytespace__claude-skills/`

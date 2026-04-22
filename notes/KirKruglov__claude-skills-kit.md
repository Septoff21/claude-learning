---
source: https://github.com/KirKruglov/claude-skills-kit
source_commit: 26f50de1ed29173e229badf5d60ac6e76b921a06
ingested_at: 2026-04-22
type: skills
quality: 4
tags: [pm, productivity, non-technical, cowork, bilingual, packaging-standard]
tried: false
---

# KirKruglov/claude-skills-kit

## 一句话

29 个面向 PM / 非技术用户的 skill，每个都是完整包（SKILL + README + INSTALL + USER-GUIDE），是目前见过打包最规范的 skill 集合。

## 核心内容

大多数 skill repo 只有 SKILL.md。这个 repo 每个 skill 包含四件套：
- `SKILL.md` — Claude 执行指令
- `README.md`（英/俄双语）— 安装前先知道它能做什么
- `docs/INSTALL.md` — 三步安装，平台分流（Cowork / Claude.ai / Projects）
- `docs/USER-GUIDE.md` — 使用示例

**技能分类**（选出最实用的）：
- **项目管理**：project-management-kit（7 个 PMBoK 文档）、OKR 进度叙事、sprint retro 分析
- **生产力**：decision-log（从会议记录提取决策）、delegation-brief（5 问生成任务简报）、stakeholder-adapter（一份文档适配多受众）
- **个人知识**：context-builder-cowork（交互式生成 context.md）、weekly-digest-synthesizer
- **工程**：code-review、API-design-assistant、migration-planner

亮点是 `context-builder-cowork`——通过对话式 interview 帮你生成结构化的项目上下文文件，适合启动新的 Cowork 会话。

## 精选文件

- `skills/context-builder-cowork/SKILL.md` — 最实用，启动任何新项目都能用
- `skills/decision-log/SKILL.md` — 从混乱的会议记录提结构化决策，设计很精巧
- `skills/delegation-brief/SKILL.md` — 5 问生成可执行任务简报，适合把任务交给 AI 前的结构化
- `README.md` — 看这个了解全部 29 个 skill 的概览

## 可以怎么用

**场景 1**：开新项目时，先跑 `context-builder-cowork` 建 context.md，之后每次新会话导入，AI 秒懂背景。

**场景 2**：开会/读 Slack 后，丢进 `decision-log`，自动提炼决策 vs 行动项，不混在一起。

**场景 3**：把任务交给 AI 前，先用 `delegation-brief` 帮自己想清楚要求，再去做。

**这个 repo 更大的价值**：它的四件套打包结构是设计自己 skill 时的参考规范，比 SKILL.md only 更完整。

## 和已有内容的差异

npow 是技术向 / agent 编排，KirKruglov 是业务向 / 非技术用户。面向完全不同人群。打包规范（四件套）是这个 repo 独有的贡献。

## 原文位置

`originals/KirKruglov__claude-skills-kit/`

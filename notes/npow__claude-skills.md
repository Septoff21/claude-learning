---
source: https://github.com/npow/claude-skills
source_commit: 51b70c089fb4cd1f63d5d102a46647f7ddb40b60
ingested_at: 2026-04-22
type: skills
quality: 4
tags: [multi-agent, orchestration, autopilot, qa, skill-engineering]
tried: false
---

# npow/claude-skills

## 一句话

以"协调者永不自我评审"为铁律的多智体编排技能集，每个 skill 都内置对抗批评和多裁判机制。

## 核心内容

这个 repo 最有价值的不是单个 skill，而是**整套 skill 工程哲学**：

- **autopilot**：从模糊想法到可验证代码的全链路流水线。分 Phase 0-5，每个 Phase 委托给专门 skill，协调者只编排不评判。Phase 门控需要新 evidence 文件才能通过，防止协调者自我批准。
- **create-skill**：元技能，专门用来写其他 skill。包含 DESIGN / WRITING / EVALUATION / PRESSURE-TESTING 多个子文件，是学习"如何设计好 skill"的最佳资料。
- **deep-debug**：结构化 debug 流程，有 DIMENSIONS（问题维度分类）/ EVIDENCE（证据收集）/ TECHNIQUES（技术手段）分层。
- **team**：模拟多角色团队讨论，角色间可以对抗批评。

**核心设计原则**：协调者 orchestrate，不 evaluate。评判永远交给独立 agent 或独立 judge。这解决了 LLM 自我评估偏差问题。

## 精选文件

- `autopilot/SKILL.md` — 最完整的全链路 autonomous 编排示例，Phase gate 设计值得精读
- `create-skill/SKILL.md` + `create-skill/DESIGN.md` — 学习如何工程化设计 skill 的核心资料
- `create-skill/PRESSURE-TESTING.md` — skill 验证方法论，有具体检查清单

## 可以怎么用

**场景 1**：想设计自己的 skill 时，先读 `create-skill/DESIGN.md`，按它的框架想清楚再写。

**场景 2**：任何复杂任务想让 Claude 自主跑完，用 autopilot 的 Phase gate 结构作为模板——把大任务拆成带 verify 条件的阶段，每阶段结束前要求生成 evidence 文件。

**场景 3**：需要质量保证时，参考它的"三独立裁判"模式——同一任务让三个独立 agent 评判，协调者只汇总，不参与评判。

## 和已有内容的差异

karpathy-skills 给的是**行为准则**（怎么做），npow 给的是**执行架构**（怎么组织多步骤/多 agent）。两者互补：前者是单次交互的质量基线，后者是复杂任务的流程框架。

## 原文位置

`originals/npow__claude-skills/`

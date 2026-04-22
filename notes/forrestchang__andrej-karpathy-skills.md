---
source: https://github.com/forrestchang/andrej-karpathy-skills
source_commit: 2c606141936f1eeef17fa3043a72095b4765b9c2
ingested_at: 2026-04-22
type: skills
quality: 4
tags: [coding, behavioral-guidelines, claude-code, simplicity, surgical-changes]
tried: false
---

# andrej-karpathy-skills

## 一句话

把 Karpathy 观察到的 LLM 编码四大痛点，浓缩成一个可直接装进 Claude Code 的 SKILL。

## 核心内容

Karpathy 指出 LLM 的四个系统性缺陷：默默做假设、倾向于过度复杂化、改了不该改的代码、没有可验证的成功标准。这个 repo 用四条原则正面回应：

1. **Think Before Coding** — 先暴露假设，有歧义时列出选项而非悄悄选一个，敢于 push back
2. **Simplicity First** — 最小代码解决问题，没要求的不加，能 50 行别写 200 行
3. **Surgical Changes** — 只动必须动的，自己的改动产生的孤儿才清理，别"顺手优化"
4. **Goal-Driven Execution** — 把"做什么"转成"什么算成功"，给 LLM 可验证的循环目标

核心洞察来自 Karpathy："LLM 极擅长循环直到满足特定目标……别告诉它做什么，给它成功标准。"

## 精选文件

- `skills/karpathy-guidelines/SKILL.md` — 直接可用的 SKILL 定义，有 frontmatter，结构干净
- `CLAUDE.md` — 等效的 CLAUDE.md 版本，适合放进项目根目录
- `EXAMPLES.md` — 具体例子（未读，建议精读后更新此笔记）

## 可以怎么用

**场景 1**：新开项目时，用 `/plugin install` 或直接 curl CLAUDE.md，让这四条原则成为 Claude 的默认行为基线。

**场景 2**：和团队共享的 repo 里放 CLAUDE.md，所有人用 Claude Code 时行为一致。

**场景 3**：把四个原则用在自己写 prompt 时的自查 checklist：我有没有给成功标准？我有没有要求"顺手做 X"？

## 和已有内容的差异

首个 ingest，暂无对比基准。这是建立品味的起点。

## 原文位置

`originals/forrestchang__andrej-karpathy-skills/`

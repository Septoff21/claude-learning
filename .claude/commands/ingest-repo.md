# /ingest-repo

**用法**：`/ingest-repo <github-url>`

把一个 GitHub repo 完整 ingest 进 vault：原文快照 + 蒸馏笔记 + 更新 MOC。

---

## 步骤

### 1. 解析 URL
从 `$ARGUMENTS` 中提取 `owner/repo`，生成本地目录名 `<owner>__<repo>`。

### 2. 读 rubric
读 `meta/_rubric.md`，了解筛选标准和已有分类。

### 3. 浅克隆原文
```bash
git clone --depth 1 <url> originals/<owner>__<repo>
rm -rf originals/<owner>__<repo>/.git
```
记录 ingest 时的 commit SHA（从 clone 过程中获取）。

### 4. 分析内容
读取 `originals/<owner>__<repo>/` 下所有 .md 文件。判断：
- 这个 repo 的核心是什么？
- 属于哪个 type（skills / prompts / workflows / patterns / tools-mcp / sdk-examples / evals / meta）？
- rubric 打分（1-5）
- 哪 2-3 个文件最值得精读？

### 5. 写蒸馏笔记
在 `notes/<owner>__<repo>.md` 创建：

```markdown
---
source: <github-url>
source_commit: <sha>
ingested_at: <YYYY-MM-DD>
type: <skills|prompts|workflows|patterns|tools-mcp|sdk-examples|evals|meta>
quality: <1-5>
tags: []
tried: false
---

# <repo 名>

## 一句话
（这个 repo 解决了什么问题，给谁用）

## 核心内容
（200 字以内，你读完之后该知道的事）

## 精选文件
- `<path>` — <一句话说为什么值得看>

## 可以怎么用
（具体场景，越具体越好）

## 和已有内容的差异
（和 vault 里其他东西的关系：互补、重叠、更好）

## 原文位置
`originals/<owner>__<repo>/`
```

### 6. 更新 MOC
- 在 `moc/by-type.md` 对应 type 下追加一行链接
- 在 `moc/by-usecase.md` 对应用途下追加
- 更新 `moc/_index.md` 的统计数字

### 7. 更新 meta/_learnings.md
写一条"今天 ingest 了 X，学到了什么新视角"——用自己的话，不是摘要。

### 8. Git commit
```bash
git add .
git commit -m "ingest: <owner>/<repo> (quality:<score>)"
git push
```

---

完成后输出：笔记路径 + 三句话总结这个 repo 的价值。

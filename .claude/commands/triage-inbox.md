# /triage-inbox

处理 `inbox/urls.md` 里积累的 URL，产出打分结果到 `inbox/_pending.md`。

---

## 步骤

### 1. 读 inbox
读 `inbox/urls.md` 中所有未处理的链接（没有 `[done]` 标记的）。

### 2. 读 rubric + 已有 originals
读 `meta/_rubric.md` 和 `originals/` 目录列表（避免重复 ingest）。

### 3. 对每个 URL
- 用 WebFetch 或 `gh repo view` 获取 repo 基本信息（README 前 100 行、stars、last commit）
- 按 rubric 打分
- 写一段 50 字以内的理由

### 4. 写进 _pending.md
格式：
```markdown
## YYYY-MM-DD 批次

### ✅ 建议 ingest（分数 ≥ 3）

#### [owner/repo](url)
- **类型**：skills
- **评分**：4/5
- **理由**：...
- **操作**：<!-- 你在这里写 ✅ ingest 或 ❌ skip -->

---

### ❌ 建议跳过（分数 < 3）

#### [owner/repo](url)
- **评分**：2/5
- **理由**：纯 awesome-list，无实质内容
```

### 5. 在 urls.md 标记已处理
把处理过的 URL 加上 `[done YYYY-MM-DD]`。

---

完成后告诉你：本批次几个建议 ingest，几个建议跳过。

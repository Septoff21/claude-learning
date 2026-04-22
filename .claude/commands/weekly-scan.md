# /weekly-scan

定时任务调用的命令。自动发现新的 Claude 相关 repo，产出 pending 供你审核。

---

## 步骤

### 1. 准备
读 `meta/_rubric.md` 和 `originals/` 目录（去重用）。

### 2. 多源发现

**GitHub 搜索**（用 gh CLI）：
```bash
gh search repos "claude skill" --sort=updated --limit=20 --json nameWithOwner,description,updatedAt,stargazersCount
gh search repos "claude prompt workflow" --sort=updated --limit=20 --json nameWithOwner,description,updatedAt,stargazersCount
gh search repos "anthropic skill" --sort=updated --limit=10 --json nameWithOwner,description,updatedAt,stargazersCount
```

**Anthropic 官方**：
- WebFetch `https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md`
- WebFetch `https://api.github.com/repos/anthropics/anthropic-cookbook/commits?per_page=5` （看是否有新 commit）

**手动 inbox**：
- 读 `inbox/urls.md` 中未处理链接（加入本批次一起处理）

### 3. 去重 + 初筛
- 已在 `originals/` 的跳过
- 已在 `_pending.md` 且有决策的跳过
- 按 rubric 快速打分（不需要深读，看 README 前 50 行）

### 4. 产出 pending
格式同 `/triage-inbox`，追加到 `inbox/_pending.md`，标注"来源：weekly-scan"。

### 5. 创建分支 + push
```bash
git checkout -b weekly-scan/$(date +%Y-%m-%d)
git add inbox/_pending.md inbox/urls.md
git commit -m "weekly-scan: $(date +%Y-%m-%d) — N candidates"
git push -u origin weekly-scan/$(date +%Y-%m-%d)
gh pr create --title "Weekly scan $(date +%Y-%m-%d)" --body "..."
```

---

**注意**：不自动 ingest。等你审核 PR、merge 后，再手动跑 `/ingest-repo`。

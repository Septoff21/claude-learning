# /ingest

**用法**：`/ingest <url>`

支持任意 URL：GitHub repo、YouTube 视频、网页文章、HN 帖子都行。自动判断类型处理。

---

## 判断 URL 类型

- `github.com/<owner>/<repo>` → GitHub repo 流程
- `youtube.com` / `youtu.be` → YouTube 流程
- 其他 → 网页文章流程

---

## GitHub Repo

```bash
git clone --depth 1 <url> originals/<owner>__<repo>
# 记录 SHA
git -C originals/<owner>__<repo> rev-parse HEAD
rm -rf originals/<owner>__<repo>/.git
```

读所有 .md 文件（限总量 200KB），按 rubric 打分，写蒸馏笔记到 `notes/<owner>__<repo>.md`。

## YouTube 视频

```bash
YT_DLP="C:/Users/algov/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/Scripts/yt-dlp.exe"
"$YT_DLP" --write-auto-subs --sub-lang en --skip-download --convert-subs vtt \
  --output "originals/youtube__%(id)s/%(title)s" <url>
"$YT_DLP" --dump-json --skip-download <url> > originals/youtube__<id>/meta.json
```

读字幕文本（去时间戳），蒸馏成笔记到 `notes/youtube__<id>.md`。

## 网页文章

WebFetch 全文，蒸馏成笔记到 `notes/article__<slug>.md`。

---

## 蒸馏笔记模板（所有类型通用）

```markdown
---
source: <url>
ingested_at: YYYY-MM-DD
type: skills/youtube/article/...
quality: <1-5>
tags: []
tried: false
---

# <标题>

## 一句话
## 核心内容（200字以内）
## 精选 / 关键时间戳
## 可以怎么用
## 和已有内容的差异
```

---

## 完成后

1. 更新 `moc/by-type.md` 对应分类
2. 如有新洞察写进 `meta/_learnings.md`
3. `git add . && git commit -m "ingest: <标题前40字>" && git push`

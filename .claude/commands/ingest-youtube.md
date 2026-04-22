# /ingest-youtube

**用法**：`/ingest-youtube <youtube-url>`

把一个 YouTube 视频的字幕/文字稿拉下来，蒸馏成笔记存进 vault。

---

## 步骤

### 1. 解析 URL
从 `$ARGUMENTS` 提取 video ID（`v=XXXX` 或短链 `youtu.be/XXXX`）。

### 2. 用 yt-dlp 拉字幕

```bash
YT_DLP="C:/Users/algov/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/Scripts/yt-dlp.exe"

# 先尝试手动字幕，没有就用自动生成字幕
"$YT_DLP" --write-subs --write-auto-subs --sub-lang en,zh-Hans,zh-Hant \
  --skip-download --output "originals/youtube__%(id)s/%(title)s" \
  --convert-subs vtt \
  "$ARGUMENTS"

# 同时拿 metadata（标题、频道、时长、发布日期）
"$YT_DLP" --dump-json --skip-download "$ARGUMENTS" > originals/youtube__<VIDEO_ID>/meta.json
```

### 3. 处理字幕文件
- 读取 .vtt 文件，去掉时间戳标签，合并成纯文本
- 如果字幕超过 8000 字，按章节或时间段分块处理

### 4. 读 rubric
读 `meta/_rubric.md` 了解什么值得记录。

### 5. 写蒸馏笔记

在 `notes/youtube__<VIDEO_ID>.md` 创建：

```markdown
---
source: <youtube-url>
video_id: <id>
channel: <频道名>
published: <YYYY-MM-DD>
duration: <时长，分钟>
ingested_at: <YYYY-MM-DD>
type: youtube
tags: []
quality: <1-5>
tried: false
---

# <视频标题>

**频道**：<channel> | **时长**：<duration>min | **发布**：<date>

## 一句话
（这个视频讲了什么，给谁看）

## 核心观点
（按时间顺序或主题列出 3-7 个要点，每条一句话，重要的配上时间戳 [MM:SS]）

## 值得引用的原话
（1-3 句真正有洞察的话，配时间戳）

## 可以怎么用
（具体场景）

## 字幕位置
`originals/youtube__<VIDEO_ID>/`
```

### 6. 更新 MOC
在 `moc/by-type.md` 的 `## youtube` 区块追加一行。

### 7. 更新 meta/_learnings.md
如果视频有新的洞察，写一条 learning。

### 8. Git commit
```bash
git add originals/youtube__<VIDEO_ID>/ notes/youtube__<VIDEO_ID>.md moc/ meta/
git commit -m "ingest-youtube: <视频标题前40字> (quality:<score>)"
git push
```

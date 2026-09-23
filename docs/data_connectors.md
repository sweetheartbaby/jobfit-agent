# Data Connectors

JobFit Agent separates job acquisition from job matching. The core workflow only needs normalized job descriptions.

## Supported Inputs

| Input | Status | Notes |
| --- | --- | --- |
| Local `.md` / `.txt` | Supported | Best for manual JD collection |
| CSV | Supported | Best for spreadsheet workflows |
| JSONL | Supported | Best for crawler/export pipelines |
| HTML snapshot | Supported | Best for browser-saved job pages |
| Live crawler | Not built-in | Use optional external tools and convert to JSONL |

## Why JSONL?

JSONL is easy to stream, append, diff, and generate from external crawlers.

Example:

```json
{"company":"ByteDance","title":"AI Agent Engineer","jd_text":"负责 Agent 工作流..."}
{"company":"Example","title":"RAG Engineer","jd_text":"负责企业知识库 RAG..."}
```

## MediaCrawler Integration Strategy

Do not couple JobFit Agent directly to a crawler. Recommended pipeline:

```text
MediaCrawler or other authorized collector
        |
        v
raw JSON / CSV
        |
        v
integrations/mediacrawler/export_jobs.py
        |
        v
JobFit JSONL
        |
        v
JobFit Agent matching workflow
```

This keeps the agent stable even when a data source changes.

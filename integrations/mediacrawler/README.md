# MediaCrawler Adapter

This folder contains an adapter for converting crawler output into JobFit Agent's standard JSONL format.

## Important

This adapter does **not** crawl any website. It only converts data that you already collected and are authorized to process.

JobFit Agent does not encourage bypassing access controls, scraping private data, or violating platform terms.

## Standard JobFit JSONL Schema

Each line is one job:

```json
{"job_id":"job-001","company":"Example","title":"AI Agent Engineer","location":"Beijing","salary":"25k-45k","source_url":"https://example.com/job/1","jd_text":"负责 AI Agent 应用开发..."}
```

Required fields:

- `title`
- `company`
- `jd_text`

Optional fields:

- `job_id`
- `location`
- `salary`
- `source_url`

## Convert Existing Crawler JSON

```bash
python integrations/mediacrawler/export_jobs.py \
  --input ../MediaCrawler/data_out/jobs_raw.json \
  --output examples/jobs_from_crawler.jsonl
```

Then run JobFit Agent:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs_from_crawler.jsonl \
  --output reports
```

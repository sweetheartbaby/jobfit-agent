# Demo

This demo shows how JobFit Agent ranks multiple job descriptions against a local resume.

## Run

```bash
python3 -m src.jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports
```

## Example Console Output

```text
1. RAG Engineer (KnowledgeBase Inc.) - 88.0 - Strong Match
2. AI Agent Engineer (ByteDance) - 60.5 - Possible, needs tailoring
3. AI Frontend Application Engineer (StartupX) - 56.4 - Possible, needs tailoring
```

## Generated Files

- `reports/match_report.md`
- `reports/match_report.json`
- `reports/interview_questions.md`
- `reports/resume_tailoring.md`

## Example Report Sections

The Markdown report includes:

- Overall ranking
- Dimension scores
- Resume evidence
- Skill gaps
- Resume suggestions
- Interview questions

## Input Formats

### Local Job Files

Put `.md` or `.txt` files under a directory:

```text
examples/jobs/
├── ai_agent_engineer.md
├── rag_engineer.md
└── frontend_ai_app.md
```

### CSV

```csv
company,title,jd_text
ByteDance,AI Agent Engineer,"负责 AI Agent 应用开发..."
```

### HTML Snapshot

Save a job detail page as `.html`, then run:

```bash
python3 -m src.jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/html_jobs \
  --output reports
```

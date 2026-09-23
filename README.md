# JobFit Agent

<p align="center">
  <b>Local-first JD-resume matching and interview preparation agent.</b><br>
  Rank job descriptions by resume fit, explain the evidence, find skill gaps, and prepare interviews.
</p>

![Tests](https://github.com/sweetheartbaby/jobfit-agent/actions/workflows/test.yml/badge.svg)

---

## Why JobFit Agent?

Job seekers often collect many job descriptions but struggle to decide which roles are truly worth applying for. JobFit Agent helps answer:

- Which job is the strongest match for my resume?
- Which JD requirements are already supported by resume evidence?
- What skill gaps should I prepare before applying?
- Which project experience should I emphasize for each role?
- What interview questions are likely to be asked?

JobFit Agent is **not** an auto-apply or mass-application tool. It is a local-first decision assistant for job matching and interview preparation.

## Use Cases

- Rank saved job descriptions before applying
- Compare AI Agent, RAG, backend, and frontend AI roles
- Prepare interview questions based on skill gaps
- Tailor resume wording without inventing experience
- Convert crawler or spreadsheet job data into a standard analysis pipeline

## Features

- Local-first resume and JD analysis
- Batch ranking for multiple jobs
- Local `.md` / `.txt` job input
- CSV job input
- JSONL job input for crawler/export pipelines
- HTML job snapshot input
- Evidence-based matching explanations
- Skill gap analysis
- Interview preparation questions
- Fact-grounded resume tailoring suggestions
- Browser-friendly HTML report
- Configurable scoring weights and keyword taxonomy
- Optional OpenAI-compatible LLM parsing with JSON repair and rule fallback

## Documentation

- [Demo](docs/demo.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Data Connectors](docs/data_connectors.md)
- [Resume Project Write-up](docs/resume_project_writeup.md)
- [Limitations](docs/limitations.md)
- [Changelog](CHANGELOG.md)

## Quick Start

### Option 1: Run without installation

```bash
git clone https://github.com/sweetheartbaby/jobfit-agent.git
cd jobfit-agent

PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --config examples/jobfit.yaml
```

### Option 2: Install as a CLI

Use a virtual environment if your Python is externally managed:

```bash
git clone https://github.com/sweetheartbaby/jobfit-agent.git
cd jobfit-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -e .

jobfit rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --config examples/jobfit.yaml
```

## Example Output

Console output:

```text
1. RAG Engineer (KnowledgeBase Inc.) - 88.0 - Strong Match
2. AI Agent Engineer (ByteDance) - 60.5 - Possible, needs tailoring
3. AI Frontend Application Engineer (StartupX) - 56.4 - Possible, needs tailoring
```

Generated files:

```text
reports/
├── match_report.md
├── match_report.json
├── match_report.html
├── interview_questions.md
└── resume_tailoring.md
```

## Input Formats

### 1. Local JD files

Put `.md` or `.txt` files into a directory:

```text
examples/jobs/
├── ai_agent_engineer.md
├── rag_engineer.md
└── frontend_ai_app.md
```

Run:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports
```

### 2. CSV jobs

CSV format:

```csv
company,title,jd_text
ByteDance,AI Agent Engineer,"负责 AI Agent 应用开发..."
```

Run:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs.csv \
  --output reports
```

### 3. JSONL jobs

JSONL is recommended for crawler/export pipelines:

```json
{"company":"ByteDance","title":"AI Agent Engineer","jd_text":"负责 AI Agent 应用开发..."}
```

Run:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs.jsonl \
  --output reports
```

### 4. HTML snapshots

Save a job detail page as `.html`, then run:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/html_jobs \
  --output reports
```

## Workflow

```text
Resume + Jobs
    |
    v
JobLoaderAgent / CSVJobLoader / HTMLSnapshotLoader
    |
    v
JDParserAgent -----------+
                         |
ResumeParserAgent -------+--> EvidenceMatcherAgent
                              |
                              v
                         FitScoringAgent
                              |
                              v
                         GapAnalyzerAgent
                              |
                              v
                         InterviewPrepAgent
                              |
                              v
                         ReportAgent
```

## Scoring Dimensions

| Dimension | Default Weight |
| --- | ---: |
| Required Skills Match | 30% |
| Project Experience Match | 25% |
| Agent / RAG Experience | 20% |
| Engineering Ability | 10% |
| Business Understanding | 10% |
| Education / Background | 5% |

## Configuration

You can customize scoring weights, keyword taxonomy, and manual review threshold:

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --config examples/jobfit.yaml
```

Example config:

```yaml
manual_review_threshold: 65

scoring:
  required_skills: 0.30
  project_experience: 0.25
  agent_rag: 0.20
  engineering: 0.10
  business: 0.10
  background: 0.05

keywords:
  agent_rag:
    - Agent
    - RAG
    - LangGraph
    - Tool Calling
```

## Optional LLM-enhanced Parsing

Default mode does not require an API key. To enable OpenAI-compatible parsing:

```bash
export OPENAI_API_KEY=your_api_key

PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --llm gpt-4o-mini
```

If the API key is missing, the network fails, or the model returns invalid JSON, JobFit Agent falls back to rule-based parsing.

## Fact-grounded Resume Tailoring

JobFit Agent generates `reports/resume_tailoring.md` with one principle:

> Improve wording based on existing resume evidence. Do not invent experience.

It lists:

- Capabilities worth emphasizing for each role
- Evidence-based rewrite drafts
- Missing keywords that should not be claimed unless true
- Evidence to prepare before interviews

## Limitations

- Rule-based matching may miss semantic matches.
- HTML snapshot parsing may include noisy text.
- LLM-enhanced parsing is optional and depends on user configuration.
- Fit scores are decision support, not hiring predictions.

See [Limitations](docs/limitations.md) for details.

## Compliance Notice

JobFit Agent only analyzes resumes and job descriptions provided by the user. It does not encourage bypassing access controls, collecting private data, violating platform terms, or mass-applying to jobs. Optional future connectors should only be used for public pages or data the user is authorized to access.

## Resume Project Description

You can describe this project like this:

> Designed and implemented JobFit Agent, a local-first job matching assistant that ranks multiple job descriptions against a resume and generates evidence-based match reports, skill gap analysis, interview questions, and fact-grounded resume tailoring suggestions. The system uses a multi-stage Agent workflow with JD parsing, resume parsing, evidence matching, fit scoring, gap analysis, and report generation, with JSON repair and rule-based fallback for robust optional LLM parsing.

## MediaCrawler Adapter

JobFit Agent does not directly depend on MediaCrawler. Instead, it provides a JSONL import format and an adapter under `integrations/mediacrawler/` for converting authorized crawler output into JobFit-compatible job data. See [Data Connectors](docs/data_connectors.md).

# Architecture

JobFit Agent is organized as a deterministic workflow with optional LLM enhancement.

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

## Design Principles

### Local-first

The default mode does not require an API key and does not upload a resume.

### Evidence-grounded

A requirement is treated as matched only when a keyword or capability can be traced back to resume text.

### Safe fallback

Optional LLM parsing is additive. If the LLM call fails or returns invalid JSON, the workflow falls back to rule-based parsing.

### Extensible connectors

Job sources are normalized into a common `Job` schema, so future connectors can be added without changing the matching workflow.

# Resume Project Write-up

Use this document to describe JobFit Agent in a resume or interview.

## One-line Description

JobFit Agent is a local-first AI agent that ranks job descriptions by resume fit and generates evidence-based match reports, skill gaps, interview questions, and resume tailoring suggestions.

## Resume Bullet - English

Designed and implemented JobFit Agent, a local-first job matching assistant that ranks multiple job descriptions against a resume and generates evidence-based match reports, skill gap analysis, interview questions, and fact-grounded resume tailoring suggestions. The system uses a multi-stage Agent workflow with JD parsing, resume parsing, evidence matching, fit scoring, gap analysis, report generation, optional LLM parsing, JSON repair, and rule-based fallback.

## 简历项目描述 - 中文

设计并实现 JobFit Agent 本地岗位匹配助手，支持批量导入岗位 JD 与个人简历，自动完成 JD 要求拆解、简历证据检索、岗位匹配评分、能力缺口分析、面试问题生成和事实约束简历优化。项目采用多阶段 Agent 工作流，并通过证据绑定、低置信标记、JSON 修复和规则兜底机制提升结果可解释性与稳定性。

## Interview Talking Points

### Why this project?

Job seekers need to compare many JDs quickly, but manual comparison is time-consuming and subjective. The project turns this into a structured agent workflow.

### How is the task decomposed?

The workflow is split into job loading, JD parsing, resume parsing, evidence matching, scoring, gap analysis, interview preparation, and report generation.

### What tools are used?

The MVP uses local file loaders, CSV/JSONL/HTML importers, rule-based keyword extraction, optional OpenAI-compatible parsing, JSON repair, and Markdown/HTML report generation.

### How are failures handled?

If LLM parsing fails, the system falls back to deterministic rules. If resume evidence is missing, the system does not claim a match and marks it as a gap. If the score is low, the report flags manual review.

### How is effectiveness evaluated?

Use JD parsing accuracy, evidence coverage, ranking reasonableness, gap quality, interview question usefulness, and regression tests.

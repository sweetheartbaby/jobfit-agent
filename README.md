# JobFit Agent

本地优先的岗位匹配与面试准备 Agent。输入一份简历和一批岗位 JD，自动输出岗位匹配排序、证据解释、能力缺口、简历优化建议和面试问题。

> MVP 目标：不做海投、不依赖招聘网站登录、不上传隐私简历；先把“哪个岗位最适合我”这件事做稳。

<p align="center">
  <b>Rank job descriptions by resume fit. Get evidence-based gaps, interview questions, and resume tailoring suggestions.</b>
</p>

![Tests](https://github.com/sweetheartbaby/jobfit-agent/actions/workflows/test.yml/badge.svg)

## Features

- Local-first resume and JD analysis
- Batch ranking for multiple jobs
- Local `.md` / `.txt` job input
- CSV job input
- HTML job snapshot input
- Evidence-based matching explanations
- Skill gap analysis
- Interview preparation questions
- Fact-grounded resume tailoring suggestions
- Optional OpenAI-compatible LLM parsing with JSON repair and rule fallback

## Documentation

- [Demo](docs/demo.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)

## MVP 方案

### 1. 用户问题

求职者通常会同时看到多个岗位，但不知道：

- 哪个岗位和自己的经历最匹配？
- JD 里的关键要求有哪些？
- 简历中哪些项目可以作为证据？
- 哪些能力是短板？
- 面试前应该重点准备什么？

JobFit Agent 用一个可解释的多阶段工作流解决这个问题。

### 2. 输入与输出

输入：

- `resume.md`：本地简历文本
- `jobs/`：多个岗位 JD，支持 `.txt` / `.md`

输出：

- `reports/match_report.md`：人类可读岗位匹配报告
- `reports/match_report.json`：结构化结果，方便二次开发
- `reports/interview_questions.md`：按岗位生成的面试准备问题
- `reports/resume_tailoring.md`：基于事实证据的简历优化建议

### 3. Agent 工作流

```text
JobLoaderAgent
  读取 jobs 目录中的 JD 文件

JDParserAgent
  抽取岗位要求：技能、Agent/RAG、模型基础、工程能力、业务能力、学历背景

ResumeParserAgent
  抽取简历中的技能、项目、业务、模型与工程经验

EvidenceMatcherAgent
  将 JD 要求和简历原文证据进行匹配

FitScoringAgent
  按维度计算匹配分并排序岗位

GapAnalyzerAgent
  分析缺口与补齐建议

InterviewPrepAgent
  生成面试追问

ReportAgent
  输出 Markdown 与 JSON 报告
```

### 4. MVP 不做什么

- 不自动海投
- 不绕过招聘平台反爬
- 不伪造简历经历
- 不强依赖 LLM API

### 5. 评分维度

| 维度 | 权重 |
| --- | ---: |
| 必备技术技能 | 30% |
| 项目经历匹配 | 25% |
| Agent / RAG 经验 | 20% |
| 工程能力 | 10% |
| 业务理解 | 10% |
| 学历/背景 | 5% |

### 6. 失败处理

| 场景 | 处理方式 |
| --- | --- |
| JD 文件为空 | 跳过并记录 warning |
| 简历信息不足 | 标记低置信并生成补充问题 |
| 没找到证据 | 不判定为匹配，只列为 gap |
| 岗位之间分数接近 | 标记需要人工决策 |
| 输出文件失败 | 保留控制台结果 |

## Roadmap

- [x] Local JD directory import
- [x] CSV job import
- [x] Evidence-based fit scoring
- [x] Markdown / JSON reports
- [x] HTML snapshot import
- [x] Optional LLM-enhanced parsing with JSON repair and rule fallback
- [x] Fact-grounded resume tailoring suggestions
- [ ] Streamlit web UI
- [ ] Optional crawler adapter for public career pages

## 安装与运行

当前 MVP 无第三方依赖，Python 3.9+ 可直接运行。

### 方式一：本地开发安装

```bash
cd jobfit-agent
pip install -e .
jobfit rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports
```

### 方式二：不安装直接运行

```bash
cd jobfit-agent
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports
```

## 示例输出

```text
# JobFit Match Report

| Rank | Role | Company | Fit Score | Recommendation |
| --- | --- | --- | ---: | --- |
| 1 | AI Agent Engineer | ByteDance | 82.5 | Strong Match |

## Why it matches
- JD requires RAG, and resume evidence mentions enterprise knowledge base RAG.

## Gaps
- JD asks for LoRA/SFT, but resume has no direct evidence.
```

## 简历写法示例

> 设计并实现 JobFit Agent 本地岗位匹配助手，支持批量导入岗位 JD 与个人简历，自动完成 JD 要求拆解、简历证据检索、岗位匹配评分、能力缺口分析和面试问题生成。项目采用多阶段 Agent 工作流，并通过证据绑定、低置信标记和规则兜底机制避免模型无依据判断，帮助求职者快速筛选最适合投递的岗位。

## CSV 导入

```bash
python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs.csv \
  --output reports
```

## 合规说明

JobFit Agent 默认只分析用户主动提供的简历和岗位 JD。本项目不鼓励绕过访问控制、采集非公开数据或违反平台服务条款；后续可选采集器仅应用于公开页面或用户有权限访问的数据。

## HTML 快照导入

把招聘页面另存为 `.html` 文件后放入目录：

```bash
python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/html_jobs \
  --output reports
```

## 事实约束简历优化

JobFit Agent 会生成 `reports/resume_tailoring.md`，但它遵守一个原则：**只基于原简历证据优化表达，不编造经历**。

报告会列出：

- 当前岗位最应该突出的能力
- 可基于原文证据强化的项目表达
- 不建议声称的缺失能力点
- 面试前需要准备的数据和案例

## 可选 LLM 增强模式

默认模式不需要 API Key。若希望增强 JD/简历解析，可配置 OpenAI-compatible API：

```bash
export OPENAI_API_KEY=your_api_key
python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --llm gpt-4o-mini
```

如果 API Key 缺失、网络失败、模型输出不是 JSON，系统会自动回退到规则模式。

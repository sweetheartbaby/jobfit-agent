# JobFit Agent 中文文档

JobFit Agent 是一个**本地优先的岗位匹配与面试准备 Agent**。它读取你的简历和一批岗位 JD，自动生成岗位匹配排序、证据解释、能力缺口、面试问题和事实约束的简历优化建议。

> 它不是自动海投工具，而是帮你判断“哪个岗位最值得投、为什么值得投、差距在哪里”。

## 适用场景

- 你手里有多个岗位 JD，不知道优先投哪个
- 你想知道简历和某个岗位到底匹不匹配
- 你想根据岗位要求准备面试问题
- 你想优化简历表达，但不想编造经历
- 你想把爬虫/表格导出的岗位数据统一做匹配分析

## 功能

- 本地简历与 JD 分析
- 多岗位批量排序
- 支持 `.md` / `.txt` 岗位文件
- 支持 CSV 岗位表
- 支持 JSONL 岗位数据，适合爬虫/导出管道
- 支持 HTML 岗位页面快照
- 基于简历证据的匹配解释
- 能力缺口分析
- 面试问题生成
- 事实约束简历优化建议
- HTML 可视化报告
- 可配置评分权重和关键词库
- 可选 LLM 增强解析，失败后自动回退规则模式

## 快速开始

### 方式一：直接运行示例

```bash
git clone https://github.com/sweetheartbaby/jobfit-agent.git
cd jobfit-agent

PYTHONPATH=src python3 -m jobfit_agent.cli sample --output reports
```

运行后打开：

```text
reports/match_report.html
```

### 方式二：分析自己的简历和岗位

```bash
PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --config examples/jobfit.yaml
```

## 输入格式

### 1. 本地 JD 文件

把岗位 JD 保存成 `.md` 或 `.txt` 文件：

```text
examples/jobs/
├── ai_agent_engineer.md
├── rag_engineer.md
└── frontend_ai_app.md
```

### 2. CSV 岗位表

```csv
company,title,jd_text
ByteDance,AI Agent Engineer,"负责 AI Agent 应用开发..."
```

### 3. JSONL 岗位数据

适合 MediaCrawler 或其他采集工具导出的数据：

```json
{"company":"ByteDance","title":"AI Agent Engineer","jd_text":"负责 AI Agent 应用开发..."}
```

### 4. HTML 页面快照

把招聘网站岗位详情页保存为 `.html` 文件，然后让 JobFit Agent 解析本地快照。

## 输出文件

```text
reports/
├── match_report.md             # Markdown 匹配报告
├── match_report.json           # 结构化结果
├── match_report.html           # 浏览器可视化报告
├── interview_questions.md      # 面试问题
└── resume_tailoring.md         # 简历优化建议
```

## Agent 工作流

```text
简历 + 岗位 JD
    |
    v
JobLoaderAgent / CSVJobLoader / JSONLJobLoader / HTMLSnapshotLoader
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

## 评分维度

| 维度 | 默认权重 |
| --- | ---: |
| 必备技术技能 | 30% |
| 项目经历匹配 | 25% |
| Agent / RAG 经验 | 20% |
| 工程能力 | 10% |
| 业务理解 | 10% |
| 学历/背景 | 5% |

## 配置文件

可以通过 `examples/jobfit.yaml` 自定义权重、关键词和人工复核阈值：

```yaml
manual_review_threshold: 65

scoring:
  required_skills: 0.30
  project_experience: 0.25
  agent_rag: 0.20
  engineering: 0.10
  business: 0.10
  background: 0.05
```

## 可选 LLM 模式

默认模式不需要 API Key。若希望增强 JD/简历解析，可以配置 OpenAI-compatible API：

```bash
export OPENAI_API_KEY=your_api_key

PYTHONPATH=src python3 -m jobfit_agent.cli rank \
  --resume examples/resume.md \
  --jobs examples/jobs \
  --output reports \
  --llm gpt-4o-mini
```

如果 API Key 缺失、网络失败或模型输出不是合法 JSON，系统会自动回退到规则模式。

## 和自动海投的区别

JobFit Agent 不做自动投递，不绕过招聘网站访问控制，也不鼓励批量海投。它只分析用户主动提供的简历和 JD，帮助用户做更好的投递决策。

## 中文简历写法

> 设计并实现 JobFit Agent 本地岗位匹配助手，支持批量导入岗位 JD 与个人简历，自动完成 JD 要求拆解、简历证据检索、岗位匹配评分、能力缺口分析、面试问题生成和事实约束简历优化。项目支持 Markdown/TXT、CSV、JSONL、HTML 快照等多种岗位输入，并提供可配置评分权重、可选 LLM 增强解析、JSON 修复和规则兜底机制，提升结果可解释性和稳定性。

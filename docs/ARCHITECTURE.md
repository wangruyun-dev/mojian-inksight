# 墨见 Inksight · 产品架构

> 让每一句回答，都有出处 · *Every claim, traceable.*

## 一句话定义

**墨见 = 一个科研阅读 Agent，把每句 AI 回答都钉回论文原文段落，附带可点击的引用链。**

它不是聊天机器人，也不是普通的 PDF 阅读器——它是你读论文时的"诚实副驾驶"。

---

## 🎯 两大护城河（这是评委会盯着看的点）

| 护城河 | 对应评分 | 目标分数 |
|--------|----------|----------|
| **抗幻觉溯源**（Citation Engine） | Agent 35% + 创新 25% | 9+ |
| **中英联动阅读**（Bilingual Reader） | 创新 25% + UI 10% | 9+ |

这两点同时也是市面上**几乎没有同类产品**做到的事——是你的差异化护城河，不是可选项。

---

## 🏛 系统全景（8 大模块）

### ① PDF 解析层 · Parser

**职责**：把任意 PDF 变成结构化数据
**技术**：PyMuPDF（文本/表格）+ PaddleOCR（扫描件/双栏）+ Unstructured（智能分块）
**输入**：用户上传的 PDF 文件
**输出**：标题树 / 段落 / 公式 / 表格 / 参考文献的 JSON

---

### ② RAG 检索层 · Retriever

**职责**：把文档段落变成可搜索的"知识库"
**技术**：LlamaIndex 编排 + BGE-M3 Embedding（中文友好）+ Chroma 向量库
**关键设计**：
- 切块粒度：200–500 tokens，块间 overlap 50 tokens
- Hybrid Search：BM25（关键词召回）+ 向量检索（语义召回）合并
- 段落级元数据：page / source / section / chunk_id
**输入**：解析后的结构化文档
**输出**：可被问答检索的向量索引

---

### ③ LLM 路由层 · LLM Router

**职责**：让不同问题用最合适的模型
**技术**：DeepSeek-V3.5（主力，便宜）+ Qwen2.5-72B（复杂推理）+ GLM-4-Plus（中文特化）
**路由策略**：

| 问题类型 | 路由目标 |
|---------|---------|
| 简单定义问答 | DeepSeek |
| 多步推理/数学证明 | Qwen |
| 中文文学/翻译/摘要 | GLM |

**输入**：用户问题 + 检索段落
**输出**：原始答案（不含引用）

---

### ④ 溯源引擎 · Citation Engine ⭐ 核心亮点 1

**职责**：让每一句话都能翻回原文
**技术**：Prompt 强制约束 + 自研 Guardrails（事实验证）
**关键设计**：

```python
# 强制 Prompt 模板（核心 5 行）
SYSTEM = """
你必须严格基于以下【检索段落】回答问题。
每个事实陈述后必须附 [n] 引用标号，n 对应段落的编号。
如果【检索段落】中找不到答案，请直接说"超出文献范围"，不要编造。
"""
```

**引用结构**：
```json
{
  "answer": "Transformer 的核心是自注意力机制 [1]，它解决了 RNN 长依赖问题 [2]。",
  "citations": [
    {"id": 1, "chunk_id": "paper_001#4", "source": "1706.03762v7", "page": 4, "snippet": "The Transformer follows the encoder-decoder structure..."},
    {"id": 2, "chunk_id": "paper_001#7", "source": "1706.03762v7", "page": 7, "snippet": "...allowing for parallelization..."}
  ]
}
```

**Guardrails 检测**：
- 检测答案中的每个事实陈述
- 在检索段落中查找对应支持
- 找不到支持的事实 → 标记为"未验证" + 警告

**输入**：原始答案 + 检索段落
**输出**：带引用标号的最终答案 + 引用链 + 溯源置信度

---

### ⑤ 中英联动阅读 · Bilingual Reader ⭐ 核心亮点 2

**职责**：让英文论文像读中文一样自然
**技术**：双栏布局 + 同步滚动 + 划词翻译
**关键设计**：

| 体验细节 | 技术指标 |
|---------|---------|
| 双栏同步滚动 | 延迟 ≤ 16ms（一帧） |
| 划词翻译 | hover 0.2s 弹气泡 |
| 引用跳转 | 点击 [1] → 原文对应位置高亮 |
| 公式/表格 | 保留原始 LaTeX / 排版结构 |
| 章节定位 | 点击目录树节点直接跳转 |

**输入**：原文 PDF + 翻译缓存
**输出**：可交互的双栏阅读界面

---

### ⑥ Agent 编排 + 工具链 · Agent

**职责**：让 LLM 自主完成多步骤任务
**技术**：LangChain Agent + Function Calling
**工具集**：

| 工具 | 功能 |
|-----|------|
| arXiv Search | 自动搜索最新论文 |
| Python Sandbox | 跑代码 + 画图 |
| GitHub Code Search | 找开源实现 |
| Reference Parser | 解析参考文献 |

**典型 Agent 任务**：
- "帮我下这篇论文并生成中文摘要 + 对比实验部分"
- "找出这 20 篇论文里被引最多的 3 篇"
- "读这个 PDF 里的实验表格，画成柱状图"

**输入**：用户复杂任务
**输出**：分解后的执行链 + 最终结果

---

### ⑦ 引用图谱挖掘 · Citation Graph

**职责**：把 20+ 篇论文变成可探索的图
**技术**：NetworkX + PageRank + Cytoscape.js（前端可视化）
**关键能力**：
- 自动抓取参考文献 → 构建有向图谱
- PageRank 找"奠基论文"（被引最多的）
- 自动综述生成：聚合 20+ 篇核心观点

**输入**：20+ 篇论文的 PDF
**输出**：可视化图谱 + 综述草稿

---

### ⑧ 写作 Copilot · Writing

**职责**：基于已读 PDF 生成论文框架
**技术**：RAG + LLM + Pandoc
**关键能力**：
- 论文大纲生成（基于读过的论文）
- Figure Caption 自动提炼
- CSV → 学术图表

**输入**：已上传的 PDF 集合 + 写作主题
**输出**：可编辑的论文框架（Markdown / LaTeX）

---

## 🌊 端到端数据流

```
[用户上传 PDF]
   ↓
① PDF Parser (PyMuPDF + OCR)
   ↓
② Chunker (LlamaIndex)
   ↓
Embedder (BGE-M3) → Chroma 向量库
                                            ↑
                                            │ Hybrid Search
                                            │
[用户提问]                                  │
   ↓                                       │
⑤ Hybrid Retriever (BM25 + 向量) ──────────┘
   ↓
③ LLM Router (DeepSeek / Qwen / GLM)
   ↓
④ Generation + Citation Engine ⭐
   ↓
Stream 流式输出到前端
   ↓
⑤ Bilingual Reader 渲染（双栏 / 图谱 / 写作）
```

---

## 📊 评分对齐

| 评分项 | 权重 | 墨见对应模块 | 目标分 |
|--------|------|-------------|--------|
| **Agent 技术深度** | 35% | ⑥ Agent 工具链 + ④ 溯源引擎 | 9+ |
| **创新性** | 25% | ④ 抗幻觉溯源 + ⑤ 中英联动 | 9+ |
| **工程实现** | 10% | Docker / 测试 / CI / 监控 | 8+ |
| **实用性** | 10% | 真实科研场景 | 9+ |
| **UI/UX** | 10% | 莫兰迪设计 + 交互细节 | 9+ |
| **学术价值** | 10% | ⑦ 引用图谱 + 自动综述 | 8+ |

> **火力分配原则**：把 70% 的精力投在 35% + 25% 两项主战场（溯源 + 中英联动），剩下 30% 分给其他。这是评委权重决定的，不是拍脑袋。

---

## 🎬 MVP 范围 vs 完整版

### MVP（D15 截止）— 保底交付

**必须做：**
- ① PDF 解析 + ② RAG 检索 + ③ LLM 路由 + ④ 溯源引擎
- 单 PDF 上传 + 问答 + 引用标注
- 基础 Web UI（左右分栏：左边 PDF，右边问答）

**可暂缓：**
- ⑤ 中英联动（放到 D20）
- ⑥ Agent 工具链（放到 D25）
- ⑦ 引用图谱（放到 D30）
- ⑧ 写作 Copilot（放到 D40）

### v1.0（D31 截止）— 完整版

8 个模块全部到位，中英联动做精，引用图谱做深，演示视频打磨完。

---

## 🛠 技术栈全景

| 层级 | 选型 | 理由 |
|------|------|------|
| **前端** | Next.js 14 + Tailwind + shadcn/ui + Mermaid + Cytoscape.js + ECharts | 移动端优先 / 组件丰富 / 图谱可视化强 |
| **后端** | FastAPI + WebSocket + Uvicorn | 异步流式输出 / 自动生成文档 |
| **Agent 编排** | LangChain | 业界最熟 / 文档全 |
| **RAG** | LlamaIndex | 检索抽象好 / 中文支持强 |
| **向量库** | Chroma（本地起步）→ Qdrant（生产） | 学习曲线低 / 后期可扩展 |
| **PDF 解析** | PyMuPDF + PaddleOCR + Unstructured | 中文 OCR 最强 / 表格保留 |
| **LLM** | DeepSeek-V3.5 + Qwen2.5-72B + GLM-4-Plus | 国产便宜 / 三家能力互补 |
| **部署** | HF Spaces（后端） + Vercel（前端） | 零成本 / 评审计分友好 |

---

## ⚠️ 风险登记与对策

| 风险 | 等级 | 对策 |
|------|------|------|
| LLM API 限流 | 中 | 多模型路由自动降级（DeepSeek → Qwen → GLM） |
| 扫描件 PDF 解析失败 | 中 | PaddleOCR 兜底，预处理时间预估 30s |
| 单 PDF 超大（>100MB） | 低 | 流式解析 + 分批入库 |
| 演示时网络抽风 | 中 | HF Spaces + 本地 Docker 双备份 |
| 评委追问技术选型 | 低 | 本文档即是答案，准备好讲解 |
| 引用准确度被质疑 | 高 | Guardrails 自检 + 展示"未验证"标记 |

---

## 📁 项目结构

```
inksight/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI 入口
│   │   ├── config.py          # 配置 + 环境变量
│   │   ├── routers/           # API 路由
│   │   │   ├── chat.py        # 问答接口
│   │   │   ├── docs.py        # PDF 上传/解析
│   │   │   └── citation.py    # 引用查询
│   │   ├── services/          # 业务逻辑
│   │   │   ├── parser.py      # ① PDF 解析
│   │   │   ├── retriever.py   # ② RAG 检索
│   │   │   ├── llm_router.py  # ③ LLM 路由
│   │   │   ├── citation.py    # ④ 溯源引擎 ⭐
│   │   │   ├── agent.py       # ⑥ Agent 编排
│   │   │   └── graph.py       # ⑦ 引用图谱
│   │   └── models/            # Pydantic 数据模型
│   ├── requirements.txt
│   └── .env.example
├── frontend/                  # Next.js 14（⑤ 中英联动 UI）
├── deploy/
│   └── hf-space/              # HF Spaces 部署配置
├── docs/
│   ├── ARCHITECTURE.md        # ← 本文档
│   ├── DEPLOY.md              # 部署手册
│   └── API.md                 # 接口文档
├── data/
│   ├── pdfs/                  # 测试 PDF 数据
│   └── chroma/                # 向量库本地存储
└── tests/                     # pytest 测试
```

---

## 🏁 现在你应该清楚的

- **墨见是什么**：一个把 LLM 回答钉回原文的科研阅读 Agent
- **它在解决什么问题**：AI 一本正经地胡说八道 + 英文论文读起来累
- **它由哪几块组成**：8 个模块，其中 ④ 溯源 + ⑤ 中英联动是核心亮点
- **它怎么拿分**：火力集中在 Agent 35% + 创新 25% 这两项
- **你的下一步**：D3 接入第一个真实 PDF，把 RAG 链路跑通——让墨见"睁开眼"

---

*最后更新：2026-10-10 · 项目阶段：D1 收尾 · 进度 5%*

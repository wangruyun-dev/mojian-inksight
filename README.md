# 墨见 Inksight

<div align="center">

**让每一句回答，都有出处。**
*Every claim, traceable.*

基于大模型与 Agent 架构的全流程科研阅读助手
A full-pipeline research reading copilot powered by LLM & Agent architecture

</div>

---

## 为什么是「墨见」？

墨，是学术的重量；见，是洞察的锋芒。
Inksight = Ink + Insight。

大模型时代最大的信任危机，是 AI 一本正经地"编造"论文、数据与结论。
墨见要做的只有一件事：**让 AI 的每一句话，都能翻回原文。**

## 核心能力

- **细粒度解析** — 双栏 PDF / 扫描件 OCR / 公式 / 表格 / 标题树 / 参考文献结构化抽取
- **抗幻觉问答（RAG + 溯源）** — 每个答案附段落级原文锚点；超纲问题主动声明"超出文献范围"
- **中英联动阅读** — 双栏对照、同步滚动、划词翻译、引用标记 ↔ 参考文献双向跳转
- **文献追踪与推荐** — arXiv 动态抓取、语义级版本去重（v1 vs v7）、优先推荐附带开源代码的论文
- **引用图谱挖掘** — 20+ 篇文献局域引用网络、基石论文挖掘（PageRank）、自动综述生成
- **写作 Copilot** — 无幻觉论文框架生成、CSV → 学术图表、Figure Caption 自动提炼

## 系统架构

```
                    ┌─────────────────────────────┐
                    │        Frontend (Next.js)    │
                    │  阅读 · 问答 · 图谱 · 写作面板  │
                    └──────────────┬──────────────┘
                                   │ WebSocket / SSE
                    ┌──────────────┴──────────────┐
                    │      Backend (FastAPI)       │
                    │  Agent 编排 · 任务规划 · 流式输出 │
                    └──┬───────┬───────┬───────┬──┘
                       │       │       │       │
                 ┌─────┴─┐ ┌───┴──┐ ┌──┴───┐ ┌─┴─────┐
                 │ LLM 路由│ │ RAG  │ │PDF 解析│ │ 工具链 │
                 │DeepSeek│ │LlamaIndex│ │PyMuPDF│ │arXiv/GitHub│
                 │ Qwen/GLM│ │+Chroma│ │+OCR  │ │/Python沙箱│
                 └────────┘ └──────┘ └──────┘ └───────┘
```

## 快速开始

```bash
# 后端（仓库根目录执行）
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env              # 填入你的 API Key
uvicorn backend.app.main:app --reload

# 验证：浏览器打开 http://127.0.0.1:8000/docs

# 前端（D20 后接入）
cd frontend
npm install && npm run dev
```

## 项目结构

```
inksight/
├── backend/          # FastAPI + Agent 编排 + RAG
├── frontend/         # Next.js 阅读与交互界面
├── docs/             # 技术文档 · 架构图 · 白皮书
├── data/pdfs/        # 测试数据集（赛事官方 PDF）
└── tests/            # pytest 测试
```

## 路线图

- [x] v0.1 · 单 PDF 解析 + RAG 问答 + 溯源（2026-10 第 1 周）
- [ ] v0.5 · 六大模块 MVP（2026-10-26 前后）
- [ ] v1.0 · 抗幻觉溯源 + 中英联动阅读 深耕版（2026-11-10 前后）

## 参赛信息

全国高校 AI 大模型挑战赛（传智杯）· 省赛 B 组 · 2026

## 许可

Apache-2.0

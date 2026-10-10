"""墨见 Inksight · 后端入口

架构分层（后续逐层填充）：
    app/main.py        <- FastAPI 应用与路由（本文件）
    app/config.py      <- 配置与环境变量
    app/routers/       <- API 路由（chat / docs / citation）
    app/services/      <- 业务逻辑（rag / agent / parser）
    app/models/        <- Pydantic 数据模型
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Inksight API",
    version="0.1.0",
    description="墨见 Inksight —— 让每一句回答，都有出处",
)

# CORS：允许前端（Vercel / localhost:3000）跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://vercel.app",  # 后续替换为实际 Vercel 域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """健康检查：部署平台和监控用。"""
    return {"status": "ok", "app": "inksight", "version": "0.1.0"}


@app.post("/api/chat")
def chat(payload: dict):
    """对话接口（占位）—— D3 之后接入 RAG 流水线。

    payload: {"question": "Transformer 的注意力机制是什么？"}
    return : {"answer": ..., "citations": [...]}  <- 溯源结构先定好
    """
    question = payload.get("question", "")
    return {
        "answer": f"[占位回复] 你问的是：{question}。RAG 流水线将在 D3-D7 接入。",
        "citations": [],  # 未来: [{"chunk_id": 3, "source": "1706.03762v7", "page": 4}]
    }

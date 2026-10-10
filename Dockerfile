# 墨见 Inksight · Hugging Face Spaces 部署镜像
#
# HF Spaces 免费层：2 vCPU / 16GB RAM，Docker SDK，睡眠后冷启动约 30s
# 评审期保持可用的做法：每天定时 ping /health（见 docs/DEPLOY.md）

FROM python:3.11-slim

WORKDIR /app

# 系统依赖（PyMuPDF 运行时库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先装依赖（利用 Docker 层缓存，改代码不用重装）
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# 再拷代码
COPY backend/ ./backend/

# HF Spaces 约定：容器必须监听 7860 端口
ENV PORT=7860
EXPOSE 7860

# 启动：绑定 0.0.0.0 才能被外部访问
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]

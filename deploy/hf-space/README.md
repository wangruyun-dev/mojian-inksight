---
title: 墨见 Inksight
emoji: 📜
colorFrom: orange
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: 让每一句回答，都有出处 · Every claim, traceable.
---

# 墨见 Inksight API

基于大模型与 Agent 架构的全流程科研阅读助手 · 传智杯 AI 大模型创新应用挑战赛作品

## 接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/chat` | POST | 对话问答（带引用溯源） |

## 文档

- 自动交互式文档：`/docs`（FastAPI 内置 Swagger UI）

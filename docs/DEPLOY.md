# 部署手册 · 墨见 Inksight

## 一、本地开发环境（已搭好）

```bash
# 进入项目根目录
cd inksight

# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\activate

# 启动后端（热重载，改代码自动重启）
uvicorn backend.app.main:app --reload --port 8000

# 验证：浏览器打开 http://127.0.0.1:8000/docs
# 能看到 Swagger 界面 = 后端跑通
```

## 二、Hugging Face Spaces 部署（免费 · 后端）

### 前置：HF 账号与 Token
1. 注册 https://huggingface.co （可正常访问，无需科学上网）
2. 头像 → Settings → Access Tokens → New token（Write 权限）

### 创建 Space
1. https://huggingface.co/new-space
2. Space name: `inksight-api` · SDK: **Docker** · CPU Basic（免费）
3. 创建后把本仓库内容推上去：

```bash
# 把 deploy/hf-space/README.md 作为 Space 根的 README（含 HF 必需的 YAML 头）
git clone https://huggingface.co/spaces/<你的用户名>/inksight-api space-deploy
# 复制 Dockerfile、backend/、deploy/hf-space/README.md → space-deploy/
# 注意 Space 根目录需要 Dockerfile + README.md + backend/
git add -A && git commit -m "deploy: inksight api" && git push
```

4. 推送后 HF 自动构建，约 3-5 分钟
5. 验证：访问 `https://<你的用户名>-inksight-api.hf.space/health`
   返回 `{"status":"ok"}` = 部署成功

### API 密钥注入（重要）
进入 Space → Settings → **Variables and secrets**：
- `DEEPSEEK_API_KEY` = sk-xxx（Secret，不公开）
- `DASHSCOPE_API_KEY` / `ZHIPU_API_KEY` 同理

代码里通过 `os.getenv()` 读取，**绝不写进代码**。

### 评审期保活（免费层 48h 无访问会休眠）
- 方案 A：在 Vercel 前端加一个定时函数，每小时 ping `/health`
- 方案 B：本地电脑挂一个计划任务每天 ping 两次
- 提交前一周改为方案 A 并写进 README（评审期在线承诺）

## 三、Vercel 部署（免费 · 前端，D20 后接入）

```bash
cd frontend
vercel   # 按提示登录并关联，一路默认
```

## 四、常见问题

| 症状 | 原因 | 解法 |
|------|------|------|
| HF 构建失败 | requirements 版本冲突 | 看 Space 的 Logs 标签页，锁版本号 |
| /health 超时 | Space 休眠中 | 等 30-60s 冷启动再试 |
| CORS 报错 | 前端域名没加白名单 | main.py 的 allow_origins 加上实际域名 |

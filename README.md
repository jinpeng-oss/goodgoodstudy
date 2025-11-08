# 初中日常学习小助手（模板）

本仓库为前后端分离的示例模板，前端使用 Vue + Vite，后端使用 FastAPI，并通过 LangChain 调用 LLM 生成回答。

快速开始（本地开发）：

1. 准备环境变量
   - 在项目根或 backend 目录下创建 `.env`，填入你的 OPENAI_API_KEY 或其它必要配置：
     ```
     OPENAI_API_KEY=your_key_here
     ```

2. 启动后端（开发）
   ```
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

3. 启动前端（开发）
   ```
   cd frontend
   npm install
   npm run dev
   ```
   然后在浏览器打开 http://localhost:5173

4. 使用 docker-compose（可选）
   - 在项目根创建 `.env`（包含 OPENAI_API_KEY），然后：
   ```
   docker-compose up --build
   ```

后续建议：
- 在 backend/app/core/langchain_client.py 中实现真实的 LangChain 流程（检索 + 检索增强生成、提示模板、温度等）。
- 增加用户对话上下文管理（conversation history），以及对敏感或未回答问题的处理策略。
- 将密钥放在 CI/CD secrets 或云 provider 的 secret 管理中，不要硬编码到仓库。

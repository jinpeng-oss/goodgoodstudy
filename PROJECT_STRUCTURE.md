# 初中日常学习小助手 — 项目结构说明

项目采用前后端分离：
- 前端：Vue 3 + Vite，负责 UI 与与后端的交互（/api/qa）。
- 后端：FastAPI，负责接收问题、调用 LangChain（或其他 LLM 工具链）并返回回答。
- 可选：使用 Docker / docker-compose 进行本地开发与部署。

推荐的目录结构：

/  
├─ docker-compose.yml  
├─ README.md  
├─ frontend/  
│  ├─ Dockerfile  
│  ├─ package.json  
│  ├─ vite.config.ts  
│  └─ src/  
│     ├─ main.ts  
│     ├─ App.vue  
│     └─ components/  
│        └─ Chat.vue  
└─ backend/  
   ├─ Dockerfile  
   ├─ requirements.txt  
   └─ app/  
      ├─ main.py                 # FastAPI 启动文件  
      ├─ core/  
      │  ├─ config.py            # 配置（环境变量、API keys）  
      │  └─ langchain_client.py  # 封装 LangChain 的调用逻辑（占位）  
      ├─ api/  
      │  └─ routers/  
      │     └─ qa.py             # 问答路由：/api/qa  
      └─ models/  
         └─ schemas.py           # 请求/响应 pydantic 模型

说明（快速导读）：
- backend/app/core/langchain_client.py：放置 LangChain client 的初始化和问答封装，建议将联网/模型配置与业务分离。
- backend/app/api/routers/qa.py：接收前端请求，校验输入，调用 langchain_client.answer(...) 并返回结果。
- frontend/src/components/Chat.vue：一个简单的聊天组件，展示对话并调用后端 API。

运行建议：
- 开发时可以直接分别启动前端（npm run dev）和后端（uvicorn）；
- 使用 docker-compose.yml 可同时启动两个服务并配置跨域代理（若需要）。

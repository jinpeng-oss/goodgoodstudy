from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import qa

app = FastAPI(title="初中学习小助手 API")

# 简单 CORS，开发时可放宽，生产按需收紧
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa.router, prefix="/api/qa", tags=["qa"])

@app.get("/health")
async def health():
    return {"status": "ok"}

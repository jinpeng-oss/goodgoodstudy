from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.langchain_client import LangChainClient

router = APIRouter()

# 请求/响应模型
class QARequest(BaseModel):
    question: str
    context: str | None = None  # 可选：比如课本章节、错题描述等

class QAResponse(BaseModel):
    answer: str

# 初始化 LangChain 客户端（根据实际改造）
lc = LangChainClient()

@router.post("/", response_model=QAResponse)
async def answer_question(req: QARequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="question is required")
    # 调用封装的 langchain client
    try:
        answer = await lc.answer(req.question, context=req.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return QAResponse(answer=answer)

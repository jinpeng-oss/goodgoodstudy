from pydantic import BaseModel

class QARequest(BaseModel):
    question: str
    context: str | None = None

class QAResponse(BaseModel):
    answer: str

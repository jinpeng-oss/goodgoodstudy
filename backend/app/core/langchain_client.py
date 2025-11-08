import os
from typing import Optional
from app.core.config import settings

# 下面给出一个示例性的 async 封装（伪代码 + 占位）
# 需要根据你选择的 LLM 提供者（OpenAI / Azure / 本地 LLM）与 LangChain 版本调整实现

class LangChainClient:
    def __init__(self):
        # 在此初始化 LangChain 所需的链、检索器、向量数据库等组件
        # 例如：从 settings 中加载 OPENAI_API_KEY，初始化 OpenAI LLM wrapper
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        # TODO: 初始化实际的 langchain chain，例如 LLM, PromptTemplate, ConversationalRetrievalChain 等
        # self.chain = ...
    
    async def answer(self, question: str, context: Optional[str] = None) -> str:
        """
        简单封装：接受问题和可选上下文，返回生成的回答字符串。
        请将此处替换为真实的 LangChain 调用逻辑（调用 self.chain(...)/run(...) 或 LLM 直接请求）。
        """
        # 占位实现（开发时临时返回固定文本）
        if not self.api_key:
            # 如果没有配置 key，返回可读的错误提示或抛错
            raise RuntimeError("OPENAI_API_KEY not configured")
        # 示例：将 context 拼入 prompt（生产中建议用 PromptTemplate）
        prompt = f"你是一个友好的初中学习助手，回答学生的问题。\n问题: {question}\n"
        if context:
            prompt += f"上下文: {context}\n"
        prompt += "请给出简洁、准确并带学习建议的回答。"

        # TODO: 用 LangChain/LLM 进行调用并返回结果
        # 例如：resp = await self.chain.apredict(question=question, context=context) 或 openai.ChatCompletion.create(...)
        # 这里返回占位文字
        return "（占位回答）这里会返回模型的回答，请在 backend/app/core/langchain_client.py 中实现实际调用。"

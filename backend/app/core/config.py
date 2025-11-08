from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    # 其它可配置项：模型名、温度、向量数据库配置等
    MODEL_NAME: str = "gpt-4o"  # 示例，按你实际使用的模型调整

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

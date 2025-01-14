# llm-chat/backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    allowed_origins: list = [
        "https://super-yodel-9w7qpgwj56h7j5q-3000.app.github.dev",
        "https://super-yodel-9w7qpgwj56h7j5q-8000.app.github.dev",
        ],
    rate_limit_documents: str = "5/minute"
    rate_limit_queries: str = "10/minute"

settings = Settings()

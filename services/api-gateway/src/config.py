from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INTERNAL_API_KEY: str = "supersecretkey"
    LANGGRAPH_AGENT_URL: str = "http://langgraph-agent:8000"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

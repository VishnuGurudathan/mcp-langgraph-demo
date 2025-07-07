import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, ValidationError

class Settings(BaseSettings):
    API_GATEWAY_URL: AnyHttpUrl = "http://localhost:8000"
    INTERNAL_API_KEY: str = "supersecretkey"

    class Config:
        env_prefix = ""
        env_file = ".env"

def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        raise RuntimeError(f"Invalid configuration: {e}")


settings = Settings()
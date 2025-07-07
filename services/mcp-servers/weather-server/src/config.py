from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INTERNAL_API_KEY: str = "supersecretkey"
    WEATHER_API_KEY: str
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

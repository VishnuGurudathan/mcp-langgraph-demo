from pydantic_settings import BaseSettings
from pydantic import Field
import json
from typing import Dict, Any

class Settings(BaseSettings):
    INTERNAL_API_KEY: str
    GROQ_API_KEY: str
    LOG_LEVEL: str = "INFO"
    MCP_TOOL_CONFIG: str = Field(..., env="MCP_TOOL_CONFIG")

    @property
    def mcp_tool_config(self) -> Dict[str, Any]:
        return json.loads(self.MCP_TOOL_CONFIG)

    class Config:
        env_file = ".env"

settings = Settings()

from fastapi import FastAPI
from .routes.ask import router as ask_router
from .exceptions import register_exception_handlers
from .logger import setup_logger

logger = setup_logger("langgraph-agent")
app = FastAPI(title="LangGraph Agent")

app.include_router(ask_router)
register_exception_handlers(app)

@app.get("/health")
async def health():
    logger.info("Health check OK")
    return {"status": "ok"}

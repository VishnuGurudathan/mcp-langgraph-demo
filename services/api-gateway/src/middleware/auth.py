from fastapi import Request, HTTPException
from ..config import settings
from ..logger import setup_logger

logger = setup_logger("auth-middleware")

async def internal_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/health"):
        return await call_next(request)

    key = request.headers.get("X-INTERNAL-KEY")
    logger.debug(f"Received request with path: {request.url.path}")
    if key != settings.INTERNAL_API_KEY:
        logger.warning("Invalid internal API key")
        raise HTTPException(status_code=403, detail="Invalid internal API key")

    return await call_next(request)

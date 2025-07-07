from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.ask import router as ask_router
from .middleware.auth import internal_key_middleware
from .logger import setup_logger
from .exceptions import (
    http_exception_handler, validation_exception_handler, unhandled_exception_handler
)

logger = setup_logger("api-gateway")

app = FastAPI(title="API Gateway")

# Middleware & CORS
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
app.middleware("http")(internal_key_middleware)

# Routers
app.include_router(ask_router)

# Exception handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/health")
async def health():
    logger.info("Health check OK")
    return {"status": "ok"}
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the API Gateway!"}
from fastapi import APIRouter, Request, HTTPException, Depends
from ..config.settings import settings
from ..tools.mcp_client import MCPClient
from ..agents.chain_agent import build_agent
from ..logger import setup_logger

router = APIRouter()
logger = setup_logger("ask-route")
mcp_client = MCPClient()
agent = None

@router.on_event("startup")
async def startup():
    await mcp_client.init()
    global agent
    agent = await build_agent(mcp_client.client)
    logger.info("LangGraph agent initialized with tools %s", settings.mcp_tool_config)

@router.post("/ask")
async def ask(req: Request):
    if req.headers.get("X-INTERNAL-KEY") != settings.INTERNAL_API_KEY:
        logger.warning("Unauthorized attempt")
        raise HTTPException(status_code=403, detail="Unauthorized")

    payload = await req.json()
    query = payload.get("query")
    logger.info("Received query: %s", query)
    try:
        resp = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        logger.info("Agent responded")
        return {"response": resp}
    except Exception as e:
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail="Agent execution failed")

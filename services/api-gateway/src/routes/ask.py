from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config import settings
from ..logger import setup_logger
import httpx

logger = setup_logger("ask-route")
router = APIRouter()

@router.post("/ask")
async def ask_proxy(payload: dict):
    logger.info("Received query for proxy")
    try:
        async with httpx.AsyncClient() as client:
            print(f"Forwarding to {settings.LANGGRAPH_AGENT_URL}/ask")
            resp = await client.post(
                f"{settings.LANGGRAPH_AGENT_URL}/ask",
                json=payload,
                headers={"X-INTERNAL-KEY": settings.INTERNAL_API_KEY}
            )
        logger.info("Forwarded query to langgraph-agent")
        logger.debug(f"Response from langgraph-agent: {resp.status_code} - {resp.text}")
        ai_content = extract_ai_content(resp.json())

        return JSONResponse(status_code=resp.status_code, content={"content": ai_content})
    except Exception as e:
        logger.exception("Error forwarding to langgraph-agent")
        return JSONResponse(status_code=500, content={"detail": "Gateway error"})

# def extract_ai_content(response_json: dict) -> str:
#     """
#     Extract the 'content' from the first AI message in the response JSON.
#     Returns a default message if no AI content is found.
#     """
#     messages = response_json.get("messages", [])
#     for msg in messages:
#         if msg.get("type") == "ai":
#             return msg.get("content", "")
#     return "No response content found."

def extract_ai_content(data: dict) -> str:
    """
    Extract AI response content from LLM JSON response
    """
    try:
        messages = data["response"]["messages"]
        # Find the last AI message
        for message in reversed(messages):
            if message.get("type") == "ai":
                return message.get("content", "")
        
        return "No AI response found"
    
    except (KeyError, TypeError) as e:
        return f"Error extracting response: {str(e)}"

import requests
from .config import settings
from .logger import setup_logger

logger = setup_logger()

def post_agentic_query(query: str) -> dict:
    """
    Sends a POST request to the Agentic RAG API endpoint.
    """
    try:
        headers = {"X-INTERNAL-KEY": settings.INTERNAL_API_KEY}
        payload = {"query": query}
        response = requests.post(f"{settings.API_GATEWAY_URL}/ask", json=payload, headers=headers, timeout=15)

        if response.ok:
            return {"status": "success", "content": response.json()}
        else:
            logger.warning("API call failed: %s - %s", response.status_code, response.text)
            return {"status": "error", "content": response.json().get("detail", "Unknown error")}

    except Exception as e:
        logger.exception("API call error")
        return {"status": "error", "content": "Internal error occurred"}
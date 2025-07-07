import os
import httpx
from mcp.server.fastmcp import FastMCP
from config import settings
from logger import setup_logger
from exceptions import WeatherError

logger = setup_logger("weather-tool")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

mcp = FastMCP(name="weather", port=8002, host= "0.0.0.0")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    try:
        logger.info("Fetching weather for %s", city)
        async with httpx.AsyncClient() as client:
            resp = await client.get(BASE_URL, params={
                "q": city,
                "appid": settings.WEATHER_API_KEY,
                "units": "metric"
            })
            resp.raise_for_status()
            data = resp.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        result = f"{city}: {desc}, {temp}°C"
        logger.info("Weather fetched successfully for %s", city)
        return result

    except httpx.HTTPStatusError as e:
        logger.error("API error fetching weather: %s", e)
        raise WeatherError(f"API returned error: {e}")
    except Exception as e:
        logger.exception("Unhandled error in weather tool")
        raise WeatherError(f"Error fetching weather for {city}: {e}")

if __name__ == "__main__":
    # Uses the latest streamable-HTTP transport
    mcp.run(transport="streamable-http")

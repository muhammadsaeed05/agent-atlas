import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

mcp = FastMCP("Weather MCP Server")

@mcp.tool()
def get_current_weather(city: str):
    """Get current weather for a city."""
    response = requests.get(
      "http://api.openweathermap.org/data/2.5/weather",
      params={
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
      }
    )

    data = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Error: {data['message']}")

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


@mcp.tool()
def get_forecast(city: str, days: int = 5):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Error: {data['message']}")

    forecast = []
    for item in data["list"][:days]:
        forecast.append({
            "date": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["description"]
        })

    return {
        "city": city,
        "forecast": forecast
    }

if __name__ == "__main__":
    mcp.run()
    
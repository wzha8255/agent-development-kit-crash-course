from google.adk.agents import Agent
## google built-in tools 
from google.adk.tools import google_search
from datetime import datetime
import requests

"""
    Calling multiple function tools in one agent. 
    -  when mix function tool with built-in tool e.g. google_search, there are errors.

"""


def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_sydney_weather():
    """
    Get the current weather in Sydney using the Open-Meteo free API.
    Returns a dictionary with temperature and weather description.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -33.87,
        "longitude": 151.21,
        "current_weather": True
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data.get("current_weather", {})
        return {
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "weathercode": weather.get("weathercode")
        }

    else:
        print(f"Failed to fetch weather: {response.status_code}")
        return None



root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time
    - get_sydney_weather
    """,
    # tools=[google_search],
    # tools=[get_current_time],
    tools=[ get_current_time, get_sydney_weather ], # <--- Doesn't work
)

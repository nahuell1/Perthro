from telegram import Update
from telegram.ext import ContextTypes
from langchain_ollama import ChatOllama
import json
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
import openmeteo_requests
import requests_cache
from retry_requests import retry


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


@tool
def get_current_weather(latitude: float, longitude: float, unit: str = "celsius"):
    """
    Get the current weather in a given location
    Example:
    Input:
        latitude = -34.6131
        longitude = -58.3772
    Output:
    {
        "unit": "celsius",
        "temperature": 12.199999809265137,
        "humidity": 85.0,
        "current_apparent_temperature": 10.35183334350586,
        "current_precipitation": 0.0,
        "current_rain": 0.0,
    }
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
        ],
        "timezone": "auto",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()

    weather_info = {
        "temperature": current.Variables(0).Value(),
        "humidity": current.Variables(1).Value(),
        "current_apparent_temperature": current.Variables(2).Value(),
        "current_precipitation": current.Variables(3).Value(),
        "current_rain": current.Variables(4).Value(),
    }
    return json.dumps(weather_info)


url = "https://api.open-meteo.com/v1/forecast"

"""
params = {
    "latitude": -34.6131,
    "longitude": -58.3772,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "precipitation",
        "rain",
    ],
    "timezone": "auto",
    "forecast_days": 1,
} """


async def tiempo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.replace(
        "/tiempo ", "", 1
    )  # Elimina el comando "/ollama" del mensaje
    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
    )
    llm_with_tools = llm.bind_tools(
        [get_current_weather], tool_choice="get_current_weather"
    )
    messages = [
        SystemMessage(
            content="Sos un asistente con muchas ganas de ayudar. Tu idioma es español argentino. En caso de que no especifiquen la ubicación, da por hecho que es Buenos Aires, Argentina."
        ),
        HumanMessage(user_input),
    ]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"get_current_weather": get_current_weather}[
            tool_call["name"].lower()
        ]
        tool_output = selected_tool.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    await update.message.reply_text(llm.invoke(messages).content)

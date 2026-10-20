"""Hourly and daily forecasts from WeatherAPI and OpenWeather."""
from typing import Any

from colorama import Fore

from api_client import get_json
from config import OPENWEATHER_API_KEY, WEATHERAPI_API_KEY, has_key

WEATHERAPI_FORECAST_URL  = "https://api.weatherapi.com/v1/forecast.json"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_hourly_forecasts(city: str) -> dict[str, list[dict[str, Any]]] | None:
    """Fetch today's hourly forecast from WeatherAPI and OpenWeather, or None if either fails."""
    if not (has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY) and has_key("OPENWEATHER_API_KEY", OPENWEATHER_API_KEY)):
        return None
    try:
        wapi_data = get_json(WEATHERAPI_FORECAST_URL, {"key": WEATHERAPI_API_KEY, "q": city, "hours": 24})
    except Exception as e:
        print(Fore.RED + f"ERROR_03: Fetching hourly forecast from WeatherAPI: {e}")
        return None

    try:
        openw_data = get_json(OPENWEATHER_FORECAST_URL, {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    except Exception as e:
        print(Fore.RED + f"ERROR_04: Fetching hourly forecast from OpenWeather: {e}")
        return None

    return {
        "weatherapi": wapi_data.get("forecast", {}).get("forecastday", [{}])[0].get("hour", []),
        "openweather": openw_data.get("list", [])
    }


def fetch_daily_forecasts(city: str) -> dict[str, list[dict[str, Any]]] | None:
    """Fetch a 3 day forecast from WeatherAPI, or None if it fails.

    Not shown in the report yet: the OpenWeather daily endpoint (One Call) needs a separate
    One Call 3.0 subscription, so there is nothing to compare it with.
    """
    if not has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY):
        return None
    try:
        wapi_data = get_json(WEATHERAPI_FORECAST_URL, {"key": WEATHERAPI_API_KEY, "q": city, "days": 3})
    except Exception as e:
        print(Fore.RED + f"ERROR_05: Fetching daily forecast from WeatherAPI: {e}")
        return None
    return {"weatherapi": wapi_data.get("forecast", {}).get("forecastday", [])}

"""Hourly and daily forecasts from WeatherAPI and OpenWeather."""
import time
from typing import Any

from colorama import Fore

from api_client import get_json
from config import OPENWEATHER_API_KEY, WEATHERAPI_API_KEY, has_key

WEATHERAPI_FORECAST_URL  = "https://api.weatherapi.com/v1/forecast.json"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Max seconds between two forecast times to still compare them.
# 30 minutes also covers cities with a half-hour UTC offset (e.g. India)
MAX_TIME_GAP = 30 * 60


def fetch_hourly_forecasts(city: str) -> dict[str, list[dict[str, Any]]] | None:
    """Fetch the raw hourly forecasts for today and tomorrow from WeatherAPI and OpenWeather, or None if either fails.

    WeatherAPI returns one entry per hour, OpenWeather one entry per 3 hours.
    """
    if not (has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY) and has_key("OPENWEATHER_API_KEY", OPENWEATHER_API_KEY)):
        return None
    try:
        # 2 days, so late in the evening there are still hours left to compare
        wapi_data = get_json(WEATHERAPI_FORECAST_URL, {"key": WEATHERAPI_API_KEY, "q": city, "days": 2})
    except Exception as e:
        print(Fore.RED + f"ERROR_03: Fetching hourly forecast from WeatherAPI: {e}")
        return None

    try:
        openw_data = get_json(OPENWEATHER_FORECAST_URL, {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    except Exception as e:
        print(Fore.RED + f"ERROR_04: Fetching hourly forecast from OpenWeather: {e}")
        return None

    return {
        "weatherapi": [hour for day in wapi_data.get("forecast", {}).get("forecastday", []) for hour in day.get("hour", [])],
        "openweather": openw_data.get("list", [])
    }


def normalize_weatherapi_hour(hour: dict[str, Any]) -> dict[str, Any]:
    """Pick the fields to compare from one WeatherAPI forecast hour."""
    return {
        "epoch": hour['time_epoch'],
        "time": hour['time'],  # local time of the city
        "temp": hour['temp_c'],
        "condition": hour['condition']['text'],
        "wind_kph": hour['wind_kph'],
        "humidity": hour['humidity'],
        "pressure": hour['pressure_mb'],
    }


def normalize_openweather_slot(slot: dict[str, Any]) -> dict[str, Any]:
    """Pick the fields to compare from one OpenWeather 3-hour forecast slot."""
    return {
        "epoch": slot['dt'],
        "time": slot['dt_txt'],  # UTC
        "temp": slot['main']['temp'],
        "condition": slot['weather'][0]['description'],
        "wind_kph": slot['wind']['speed'] * 3.6,  # m/s -> km/h
        "humidity": slot['main']['humidity'],
        "pressure": slot['main']['pressure'],
    }


def pair_hourly_forecasts(wapi_hours: list[dict[str, Any]], openw_slots: list[dict[str, Any]],
                          hours_ahead: int = 24, now: float | None = None) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Pair every OpenWeather slot in the next `hours_ahead` hours with the WeatherAPI hour closest to it in time.

    Both APIs give a Unix timestamp per entry, so they are matched on that instead of the
    time strings (WeatherAPI uses the city's local time, OpenWeather uses UTC).
    """
    now   = time.time() if now is None else now
    wapi  = [normalize_weatherapi_hour(hour) for hour in wapi_hours]
    pairs = []
    if not wapi:
        return pairs

    for slot in openw_slots:
        openw = normalize_openweather_slot(slot)
        if not now - MAX_TIME_GAP <= openw["epoch"] <= now + hours_ahead * 3600:
            continue
        closest = min(wapi, key=lambda hour: abs(hour["epoch"] - openw["epoch"]))
        if abs(closest["epoch"] - openw["epoch"]) <= MAX_TIME_GAP:
            pairs.append((closest, openw))
    return pairs


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

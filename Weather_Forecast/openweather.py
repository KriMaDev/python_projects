"""Current weather from OpenWeather."""
from typing import Any

from colorama import Fore

from api_client import get_json
from config import OPENWEATHER_API_KEY, has_key

URL        = "https://api.openweathermap.org/data/2.5/weather"
RAIN_TYPES = {"Rain", "Drizzle"}


def parse_openweather(data: dict[str, Any]) -> dict[str, Any]:
    """Pick the fields used in the report from an OpenWeather response."""
    condition = data['weather'][0]['main']
    return {
        "condition": condition,
        "rain": condition in RAIN_TYPES,
        "temp": data['main']['temp'],
        "low": data['main']['temp_min'],
        "high": data['main']['temp_max'],
        "feels": data['main']['feels_like'],
        "humidity": data['main']['humidity'],
        "s_pressure": data['main']['sea_level'],
        "g_pressure": data['main']['grnd_level'],
        "vision": data['visibility'] / 1000,   # m -> km
        "w_spd": data['wind']['speed'] * 3.6,  # m/s -> km/h
    }


def fetch_openweather(city: str) -> dict[str, Any] | None:
    """Fetch the current weather for a city, or None if it fails."""
    if not has_key("OPENWEATHER_API_KEY", OPENWEATHER_API_KEY):
        return None
    try:
        data = get_json(URL, {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
        return parse_openweather(data)
    except Exception as e:
        print(Fore.RED + f"ERROR_00: Fetching from OpenWeather: {e}")
        return None

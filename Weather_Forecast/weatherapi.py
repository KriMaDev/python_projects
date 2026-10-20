"""Current weather from WeatherAPI."""
from typing import Any

from colorama import Fore

from api_client import get_json
from config import WEATHERAPI_API_KEY, has_key

URL        = "https://api.weatherapi.com/v1/current.json"
RAIN_TYPES = {'Light drizzle', 'Rain', 'Moderate rain', 'Light rain'}


def parse_weatherapi(data: dict[str, Any]) -> dict[str, Any]:
    """Pick the fields used in the report from a WeatherAPI response."""
    location  = data['location']
    current   = data['current']
    condition = current['condition']['text']
    return {
        "condition": condition,
        "rain": condition in RAIN_TYPES,
        "region": location['region'],
        "country": location['country'],
        "lat": location['lat'],
        "lon": location['lon'],
        "localtime": location['localtime'],
        "temp": current['temp_c'],
        "feels": current['feelslike_c'],
        "humidity": current['humidity'],
        "w_temp": current['windchill_c'],
        "w_spd": current['wind_kph'],
        "w_deg": current['wind_degree'],
        "w_dir": current['wind_dir'],
        "gust_spd": current['gust_kph'],
        "mbar_p": current['pressure_mb'],
        "in_p": current['pressure_in'],
        "vision": current['vis_km'],
        "uv": current['uv'],
    }


def fetch_weatherapi(city: str) -> dict[str, Any] | None:
    """Fetch the current weather for a city, or None if it fails."""
    if not has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY):
        return None
    try:
        data = get_json(URL, {"key": WEATHERAPI_API_KEY, "q": city})
        return parse_weatherapi(data)
    except Exception as e:
        print(Fore.RED + f"ERROR_01 Fetching from WeatherAPI: {e}")
        return None

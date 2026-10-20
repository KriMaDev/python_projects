"""Current weather from Weatherstack."""
from typing import Any

from colorama import Fore

from api_client import ApiError, get_json
from config import WEATHERSTACK_API_KEY, WEATHERSTACK_HTTPS, has_key

# The free plan rejects HTTPS, so by default the key is sent unencrypted.
# Acceptable for a free key (worst case someone uses up the quota); set WEATHERSTACK_HTTPS=1 on a paid plan.
URL        = f"{'https' if WEATHERSTACK_HTTPS else 'http'}://api.weatherstack.com/current"
RAIN_TYPES = {'Light drizzle', 'Rain', 'Moderate rain', 'Light rain'}


def parse_weatherstack(data: dict[str, Any]) -> dict[str, Any]:
    """Pick the fields used in the report from a Weatherstack response."""
    # Weatherstack answers errors with HTTP 200 and success=false
    if data.get('success') is False:
        raise ApiError(data['error']['info'])

    current   = data['current']
    condition = current['weather_descriptions'][0]
    return {
        'condition': condition,
        'rain': condition in RAIN_TYPES,
        'temp': current['temperature'],
        'feels': current['feelslike'],
        'humidity': current['humidity'],
        'pressure': current['pressure'],
        'w_spd': current['wind_speed'],
        'w_deg': current['wind_degree'],
        'w_dir': current['wind_dir'],
        'lan': data['location']['lat'],
        'lon': data['location']['lon'],
        'vision': current['visibility'],
        'uv': current['uv_index'],
    }


def fetch_weatherstack(city: str) -> dict[str, Any] | None:
    """Fetch the current weather for a city, or None if it fails."""
    if not has_key("WEATHERSTACK_API_KEY", WEATHERSTACK_API_KEY):
        return None
    try:
        data = get_json(URL, {"access_key": WEATHERSTACK_API_KEY, "query": city})
        return parse_weatherstack(data)
    except Exception as e:
        print(Fore.RED + f"ERROR_02: Fetching from Weatherstack: {e}")
        return None

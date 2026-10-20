"""Hourly and daily forecasts from WeatherAPI and OpenWeather."""
import requests
from colorama import Fore

from config import OPENWEATHER_API_KEY, WEATHERAPI_API_KEY, has_key


# Fetch hourly forecasts from WeatherAPI & OpenWeather
def fetch_hourly_forecasts(city):
    if not (has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY) and has_key("OPENWEATHER_API_KEY", OPENWEATHER_API_KEY)):
        return None
    try:
        # Fetch hourly forecast from WeatherAPI
        weatherapi_url  = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_API_KEY}&q={city}&hours=24"
        wapi_response   = requests.get(weatherapi_url)
        wapi_data       = wapi_response.json()
    except Exception as e:
        print(Fore.RED + f"ERROR_03: Fetching hourly forecast from WeatherAPI: {e}")
        return None

    try:
        # Fetch hourly forecast from OpenWeather
        openweather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        openw_response  = requests.get(openweather_url)
        openw_data      = openw_response.json()
    except Exception as e:
        print(Fore.RED + f"ERROR_04: Fetching hourly forecast from OpenWeather: {e}")
        return None

    return {
        "weatherapi": wapi_data.get("forecast", {}).get("forecastday", [{}])[0].get("hour", []),
        "openweather": openw_data.get("list", [])
    }

# Fetch daily forecasts from WeatherAPI & OpenWeather
def fetch_daily_forecasts(city):
    if not has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY):
        return None
    try:
        # Fetch daily forecast from WeatherAPI
        weatherapi_url  = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_API_KEY}&q={city}&days=3"
        wapi_response   = requests.get(weatherapi_url)
        wapi_data       = wapi_response.json()
    except Exception as e:
        print(Fore.RED + f"ERROR_05: Fetching daily forecast from WeatherAPI: {e}")
        return None
    '''
    try:
        # Use OpenWeather One Call API for daily forecasts
        openweather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={wapi_data['location']['lat']}&lon={wapi_data['location']['lon']}&exclude=hourly,minutely&appid={OPENWEATHER_API_KEY}&units=metric"
        openw_response  = requests.get(openweather_url)
        openw_data      = openw_response.json()
    except Exception as e:
        print(Fore.RED + f"ERROR_06: Fetching daily forecast from OpenWeather: {e}")
        return None
    print(f"\n\n{wapi_data} \n--------\n{openw_data}\n\n") # TODO OpenWeather Data is not received ok!!
    return {
        "weatherapi": wapi_data.get("forecast", {}).get("forecastday", []),
        "openweather": openw_data.get("daily", [])
    }
    '''
    return {"weatherapi": wapi_data.get("forecast", {}).get("forecastday", [])}

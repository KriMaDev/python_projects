"""Current weather from OpenWeather."""
import requests
from colorama import Fore

from config import OPENWEATHER_API_KEY, has_key


# Fetch weather from OpenWeather
def fetch_openweather(city):
    if not has_key("OPENWEATHER_API_KEY", OPENWEATHER_API_KEY):
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        # Get full data
        response = requests.get(url)
        data     = response.json()
        # print(f"OpenWeather response:\n{data}\n")
        # Create needed vars with data
        temp      = data['main']['temp']
        feels     = data['main']['feels_like']
        low       = data['main']['temp_min']
        high      = data['main']['temp_max']
        humid     = data['main']['humidity']
        sea_pre   = data['main']['sea_level']
        grd_pre   = data['main']['grnd_level']
        vision    = data['visibility'] / 1000
        wind_spd  = data['wind']['speed'] * 3.6
        # Condition & Rain Status
        condition = data['weather'][0]['main']
        rain_type = {'Rain', 'Drizzle'}
        rain = False
        for rtype in rain_type:
            if rtype == data['weather'][0]['main']:
                rain = True

        return {
            "condition": condition,
            "rain": rain,
            "temp": temp,
            "low": low,
            "high": high,
            "feels": feels,
            "humidity": humid,
            "s_pressure": sea_pre,
            "g_pressure": grd_pre,
            "vision": vision,
            "w_spd": wind_spd
        }
    
    except Exception as e:
        print(Fore.RED + f"ERROR_00: Fetching from OpenWeather: {e}")
        return None

"""Current weather from WeatherAPI."""
import requests
from colorama import Fore

from config import WEATHERAPI_API_KEY, has_key


# Fetch weather from WeatherAPI
def fetch_weatherapi(city):
    if not has_key("WEATHERAPI_API_KEY", WEATHERAPI_API_KEY):
        return None
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_API_KEY}&q={city}"
    try:
        # Get full data
        response = requests.get(url)
        data     = response.json()
        # print(f"WeatherAPI response:\n{data}\n")
        # Create needed vars with data
        region    = data['location']['region']
        country   = data['location']['country']
        lat       = data['location']['lat']
        lon       = data['location']['lon']
        local_t   = data['location']['localtime']
        temp      = data['current']['temp_c']
        feels     = data['current']['feelslike_c']
        humidity  = data['current']['humidity']
        wind_temp = data['current']['windchill_c']
        wind_spd  = data['current']['wind_kph']
        wind_deg  = data['current']['wind_degree']
        wind_dir  = data['current']['wind_dir']
        gust_spd  = data['current']['gust_kph']
        mbar_pres = data['current']['pressure_mb']
        in_pres   = data['current']['pressure_in']
        vision    = data['current']['vis_km']
        uv        = data['current']['uv']
        # Condition & Rain Status
        condition = data['current']['condition']['text']
        rain_type = {'Light drizzle', 'Rain', 'Moderate rain', 'Light rain'}
        rain = False
        for rtype in rain_type:
            if rtype == data['current']['condition']['text']:
                rain = True

        return {
            "condition": condition,
            "rain": rain,
            "region": region,
            "country": country,
            "lat": lat,
            "lon": lon,
            "localtime": local_t,
            "temp": temp,
            "feels": feels,
            "humidity": humidity,
            "w_temp": wind_temp,
            "w_spd": wind_spd,
            "w_deg": wind_deg,
            "w_dir": wind_dir,
            "gust_spd": gust_spd,
            "mbar_p": mbar_pres,
            "in_p": in_pres,
            "vision": vision,
            "uv": uv
        }
    
    except Exception as e:
        print(Fore.RED + f"ERROR_01 Fetching from WeatherAPI: {e}")
        return None

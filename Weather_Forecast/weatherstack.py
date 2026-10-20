"""Current weather from Weatherstack."""
import requests
from colorama import Fore

from config import WEATHERSTACK_API_KEY, WEATHERSTACK_HTTPS, has_key


# Fetch weather from WeatherStack
def fetch_weatherstack(city):
    if not has_key("WEATHERSTACK_API_KEY", WEATHERSTACK_API_KEY):
        return None
    # Weatherstack free plan does not allow HTTPS, so this key is sent unencrypted.
    scheme = "https" if WEATHERSTACK_HTTPS else "http"
    url = f"{scheme}://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city}"
    try:
        response = requests.get(url)
        data     = response.json()
        
        if 'success' in data and data['success'] is False:
            raise Exception(data['error']['info'])
    
        #print(f"Weatherstack response:\n{data}\n")
        
        # Extract relevant data from the response
        temperature = data['current']['temperature']
        feels_like  = data['current']['feelslike']
        humidity    = data['current']['humidity']
        pressure    = data['current']['pressure']
        wind_speed  = data['current']['wind_speed']
        wind_degree = data['current']['wind_degree']
        wind_dir    = data['current']['wind_dir']
        visibility  = data['current']['visibility']
        uv_index    = data['current']['uv_index']
        langtitute  = data['location']['lat']
        longtitute  = data['location']['lon']
        # Condition & Rain Status
        condition   = data['current']['weather_descriptions'][0]
        rain_type = {'Light drizzle', 'Rain', 'Moderate rain', 'Light rain'}
        rain = False
        for rtype in rain_type:
            if rtype == data['current']['weather_descriptions'][0]:
                rain = True

        
        # Print or return the formatted data
        return {
            'condition': condition,
            'rain': rain,
            'temp': temperature,
            'feels': feels_like,
            'humidity': humidity,
            'pressure': pressure,
            'w_spd': wind_speed,
            'w_deg': wind_degree,
            'w_dir': wind_dir,
            'lan': langtitute,
            'lon': longtitute,
            'vision': visibility,
            'uv': uv_index
        }
    
    except Exception as e:
        print(Fore.RED + f"ERROR_02: Fetching from Weatherstack: {e}")
        return None

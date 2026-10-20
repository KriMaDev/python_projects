import requests
from colorama import Fore, init
import time
from config import OPENWEATHER_API_KEY, WEATHERAPI_API_KEY, WEATHERSTACK_API_KEY, WEATHERSTACK_HTTPS, has_key

# Initialize colorama for Windows compatibility
init(autoreset=True)

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

# Fetch weather from AccuWeather
'''
def fetch_accuweather_location(city):
    url = f"https://dataservice.accuweather.com/locations/v1/cities/search?q={city}&apikey={ACCUWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if len(data) > 0:
            location_key = data[0]["Key"]
            print(f"AccuWeather location key for {city}: {location_key}")
            return location_key
        else:
            print(f"No location found for {city}")
            return None

    except Exception as e:
        print(f"ERROR_01 Fetching AccuWeather location key: {e}")
        return None

def fetch_accuweather_weather(location_key):
    url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={ACCUWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data:
            print(f"AccuWeather weather data:\n{data}\n")
            return data
        else:
            print(f"No weather data found for location key: {location_key}")
            return None

    except Exception as e:
        print(f"ERROR_02 Fetching AccuWeather weather data: {e}")
        return None
'''

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

# Comparison between forecasts
def compare_forecasts(openw_d, wapi_d, wstk_d):
    print(Fore.LIGHTGREEN_EX + f"\n        | Data Comparing |")

    if openw_d and wapi_d and wstk_d:

        # Check if all forecasts respond with same status for rain.
        if openw_d['rain'] == wapi_d['rain'] == wstk_d['rain']:
            print(Fore.GREEN + "\nAll forecasts agree on rain status!")
        else:
            print(Fore.RED + "\nThe forecasts disagree on rain status!")

        # Compare Conditions
        if openw_d['condition'] == wapi_d['condition'] == wstk_d['condition']:
            print(Fore.GREEN + "All forecasts agree on conditions!")
        else:
            print(Fore.RED + "The forecasts show different conditions!")

        # Compare Temperatures
        max_temp = max(openw_d['temp'], wapi_d['temp'], wstk_d['temp'])
        min_temp = min(openw_d['temp'], wapi_d['temp'], wstk_d['temp'])
        if max_temp != min_temp:
            print(Fore.YELLOW + f"The temperature difference is {max_temp - min_temp:.2f}°C between the forecasts.")
        else:
            print(Fore.GREEN + "All forecasts report the same temperature.")

        # Compare Humidity
        max_humidity = max(openw_d['humidity'], wapi_d['humidity'], wstk_d['humidity'])
        min_humidity = min(openw_d['humidity'], wapi_d['humidity'], wstk_d['humidity'])
        if max_humidity != min_humidity:
            print(Fore.YELLOW + f"The humidity difference is {max_humidity - min_humidity:.2f}% between the forecasts.")
        else:
            print(Fore.GREEN + "All forecasts report the same humidity.")

        # Compare Pressures
        max_pressure = max(openw_d['s_pressure'], wapi_d['mbar_p'], wstk_d['pressure'])
        min_pressure = min(openw_d['s_pressure'], wapi_d['mbar_p'], wstk_d['pressure'])
        if max_pressure != min_pressure:
            print(Fore.YELLOW + f"The pressure difference is {max_pressure - min_pressure:.2f} mbar between the forecasts.")
        else:
            print(Fore.GREEN + "All forecasts report the same pressure.")

        # Compare Wind Speeds
        max_wind_speed = max(openw_d['w_spd'], wapi_d['w_spd'], wstk_d['w_spd'])
        min_wind_speed = min(openw_d['w_spd'], wapi_d['w_spd'], wstk_d['w_spd'])
        if max_wind_speed != min_wind_speed:
            print(Fore.YELLOW + f"The wind speed difference is {max_wind_speed - min_wind_speed:.2f} kmh between the forecasts.")
        else:
            print(Fore.GREEN + "All forecasts report the same wind speed.")

        # Compare Visibility
        max_visibility = max(openw_d['vision'], wapi_d['vision'], wstk_d['vision'])
        min_visibility = min(openw_d['vision'], wapi_d['vision'], wstk_d['vision'])
        if max_visibility != min_visibility:
            print(Fore.YELLOW + f"The visibility difference is {max_visibility - min_visibility:.2f} km between the forecasts.")
        else:
            print(Fore.GREEN + "All forecasts report the same visibility.")
    
    else:
        print(Fore.RED + f"ERROR_07: Comparing data")
        return None

# Comparison between hourly & daily forecasts
def compare_future_forecasts(forecast1, forecast2, forecast_type='hourly'):
    print(Fore.LIGHTBLUE_EX + f"\n        | Future Average Forecast ({forecast_type}) |\n\n")
    
    try:
        for i in range(min(len(forecast1), len(forecast2))):
            if forecast_type == 'hourly':
                # Extract hourly data
                time1 = forecast1[i]['time'] if 'time' in forecast1[i] else forecast1[i].get('dt_txt')
                temp1 = forecast1[i].get('temp_c', forecast1[i].get('main', {}).get('temp'))
                temp2 = forecast2[i].get('temp_c', forecast2[i].get('main', {}).get('temp'))
                
                condition1 = forecast1[i].get('condition', {}).get('text', forecast1[i].get('weather', [{}])[0].get('description'))
                condition2 = forecast2[i].get('weather', [{}])[0].get('description')
                
                wind_speed1 = forecast1[i].get('wind_kph', forecast1[i].get('wind', {}).get('speed'))
                wind_speed2 = forecast2[i].get('wind', {}).get('speed')
                
                humidity1 = forecast1[i].get('humidity')
                humidity2 = forecast2[i].get('main', {}).get('humidity')
                
                pressure1 = forecast1[i].get('pressure_mb', forecast1[i].get('main', {}).get('pressure'))
                pressure2 = forecast2[i].get('main', {}).get('pressure')
            
            elif forecast_type == 'daily':
                # Extract daily data
                time1 = forecast1[i].get('date')  # WeatherAPI date
                temp1 = forecast1[i].get('day', {}).get('avgtemp_c', forecast1[i].get('temp', {}).get('day'))  # WeatherAPI temp
                temp2 = forecast2[i].get('temp', {}).get('day')  # OpenWeather daily temp
                
                condition1 = forecast1[i].get('day', {}).get('condition', {}).get('text')
                condition2 = forecast2[i].get('weather', [{}])[0].get('description')
                
                wind_speed1 = forecast1[i].get('day', {}).get('maxwind_kph')
                wind_speed2 = forecast2[i].get('wind_speed')
                
                humidity1 = forecast1[i].get('day', {}).get('avghumidity')
                humidity2 = forecast2[i].get('humidity')
                
                pressure1 = forecast1[i].get('day', {}).get('pressure_mb')
                pressure2 = forecast2[i].get('pressure')

            # Print comparison
            print(Fore.LIGHTBLUE_EX + f"\n"
                f"Date                       : {time1}\n"
                f"Temperature Difference     : {abs(temp1 - temp2):.2f}°C      (Avg: {(temp1 + temp2) / 2:.2f} °C)\n"
                f"Conditions                 : {condition1} vs {condition2}\n"
                f"Wind Speed Difference      : {abs(wind_speed1 - wind_speed2):.2f} km/h   (Avg: {(wind_speed1 + wind_speed2) / 2:.2f} km/h)\n"
                f"Humidity Difference        : {abs(humidity1 - humidity2):.2f}%        (Avg: {(humidity1 + humidity2) / 2:.2f}%)\n"
                f"Pressure Difference        : {abs(pressure1 - pressure2):.2f} mbar   (Avg: {(pressure1 + pressure2) / 2:.2f} mbar)\n"
                "\n")
    except Exception as e:
        print(Fore.RED + f"ERROR_08: Comparing future forecast data: {e}")
        return None

# Calculate average results
def calc_average(openw_d, wapi_d, wstk_d):
    if openw_d and wapi_d and wstk_d:
        # Simple Variables
        temperature = (openw_d['temp'] + wapi_d['temp'] + wstk_d['temp']) / 3
        humidity    = (openw_d['humidity'] + wapi_d['humidity'] + wstk_d['humidity']) / 3
        vision      = (openw_d['vision'] + wapi_d['vision'] + wstk_d['vision']) / 3
        pressure    = (openw_d['s_pressure'] + wapi_d['mbar_p'] + wstk_d['pressure']) / 3
        w_speed     = (openw_d['w_spd'] + wapi_d['w_spd'] + wstk_d['w_spd']) / 3

        print(Fore.LIGHTGREEN_EX + f"\n        | Average Forecast |\n\n"
            f"Temperature            : {temperature:.2f} °C\n"
            f"Humidity               : {humidity:.2f} %\n"
            f"Pressure               : {pressure:.2f} mbar (hPa)\n"
            f"Wind Speed             : {w_speed:.2f} /kmh\n"
            f"Visibility             : {vision:.2f} km"
        )
        # Conditions
        if openw_d['condition'] == wapi_d['condition'] == wstk_d['condition']:
            print(Fore.LIGHTGREEN_EX + f"Condition status is    : {openw_d['condition']}")
        else:
            print(Fore.LIGHTGREEN_EX + f"Condition statuses are : | {openw_d['condition']} | {wapi_d['condition']} | {wstk_d['condition']} |")
        # Rain Status
        if openw_d['rain'] == wapi_d['rain'] == wstk_d['rain']:
            print(Fore.LIGHTGREEN_EX + f"Rain status is         : {openw_d['rain']}")
        else:
            print(Fore.LIGHTGREEN_EX + f"Statuses for rain are  : | {openw_d['rain']} | {wapi_d['rain']} | {wstk_d['rain']} |")
    else:
        print(Fore.RED + f"ERROR_09: Calculating average")
        return None

# Display forecast & comparisson results
def show_forecast_results(city):
    openw_d = fetch_openweather(city)
    wapi_d  = fetch_weatherapi(city)
    wstk_d  = fetch_weatherstack(city)

    if openw_d or wapi_d or wstk_d:
        print(Fore.LIGHTBLUE_EX + f"\n| Weather forecast for {city.capitalize()} at {time.strftime('%d/%m/%Y %H:%M:%S')} |\n"
              "\n| Selected data from all sources used for the report |\n")

        # OpenWeather Data Printing
        if openw_d:
            print(Fore.LIGHTBLUE_EX + f"        | OpenWeather |\n\n"
                f"Condition         : {openw_d['condition']}\n"
                f"Temperature       : {openw_d['temp']} °C\n"
                f"Feels Like        : {openw_d['feels']} °C\n"
                f"Lowest  °C        : {openw_d['low']} °C\n"
                f"Highest °C        : {openw_d['high']} °C\n"
                f"Humidity          : {openw_d['humidity']} %\n"
                f"Sea Pressure      : {openw_d['s_pressure']} hPa\n"
                f"Ground Pressure   : {openw_d['g_pressure']} hPa\n"
                f"Visibillity       : {openw_d['vision']} km\n"
                f"Wind Speed        : {openw_d['w_spd']:.2f} /kmh\n"
                f"Rain              : {openw_d['rain']}\n"
            )
        else:
            print(Fore.RED + f"ERROR_10: Couldn't fetch OpenWeather!\n")

        # WeatherAPI Data Printing
        if wapi_d:
            print(Fore.LIGHTBLUE_EX + f"        | WeatherAPI |\n\n"
                f"Condition         : {wapi_d['condition']}\n"
                f"Temperature       : {wapi_d['temp']} °C\n"
                f"Feels Like        : {wapi_d['feels']} °C\n"
                f"Humidity          : {wapi_d['humidity']} %\n"
                f"Pressure          : {wapi_d['mbar_p']} mbar\n" 
                f"Visibility        : {wapi_d['vision']} km\n"      
                f"Region            : {wapi_d['region']}\n"
                f"Country           : {wapi_d['country']}\n"
                f"Local Time        : {wapi_d['localtime']}\n"
                f"Latitude          : {wapi_d['lat']}\n"
                f"Longtitude        : {wapi_d['lon']}\n"
                f"Wind Speed        : {wapi_d['w_spd']} /kmh\n"
                f"Wind Temperature  : {wapi_d['w_temp']} °C\n"
                f"Wind Degree       : {wapi_d['w_deg']} °\n"
                f"Wind Direction    : {wapi_d['w_dir']}\n"
                f"Gust Speed        : {wapi_d['gust_spd']} /kmh\n"
                f"UV Index          : {wapi_d['uv']}\n"
                f"Rain              : {wapi_d['rain']}\n"
            )
        else:
            print(Fore.RED + f"ERROR_11: Couldn't fetch WeatherAPI!\n")

        # WeatherStack Data Printing
        if wstk_d:
            print(Fore.LIGHTBLUE_EX + f"        | WeatherStack |\n\n"
                f"Condition         : {wstk_d['condition']}\n"
                f"Temperature       : {wstk_d['temp']} °C\n"
                f"Feels Like        : {wstk_d['feels']} °C\n"
                f"Humidity          : {wstk_d['humidity']} %\n"
                f"Pressure          : {wstk_d['pressure']} mbar\n"
                f"Visibility        : {wstk_d['vision']} km\n"
                f"Wind Speed        : {wstk_d['w_spd']} /kmh\n"
                f"Wind Degree       : {wstk_d['w_deg']} °\n"
                f"Wind Direction    : {wstk_d['w_dir']}\n"
                f"UV Index          : {wstk_d['uv']}\n"
                f"Rain              : {wstk_d['rain']}\n"
            )
        else:
            print(Fore.RED + f"ERROR_12: Couldn't fetch WeatherStack!\n")
        
        # Compare Data From All Forecasts
        compare_forecasts(openw_d, wapi_d, wstk_d)
        # Show Calculated Average Forecast Data
        calc_average(openw_d, wapi_d, wstk_d)

    else:
        print(Fore.RED + f"ERROR_13: Couldn't fetch anything...\n")
        return None

# =======================================================================================================================
#                                                                                                                    MAIN
# =======================================================================================================================

city = input(str(Fore.LIGHTBLUE_EX + f"Enter name of city\n: "))
show_forecast_results(city)

# Fetch hourly forecasts
pass_h = False
print("\n\n")
while not pass_h:
    hour = input(str(Fore.LIGHTBLUE_EX + f"Do you want to see the hourly forecast for today? ({time.strftime('%d/%m/%Y')})\n: "))
    yea  = {"yes", "y", "YES", "Y", "1", "True"}
    nah  = {"no", "n", "NO", "N", "0", "False"}
    if hour in yea:
        hourly_forecasts = fetch_hourly_forecasts(city)
        compare_future_forecasts(hourly_forecasts["weatherapi"], hourly_forecasts["openweather"], forecast_type="hourly")
        pass_h = True
        #print(hourly_forecasts)
    elif hour in nah:
        print(Fore.LIGHTBLUE_EX + f"You do not want to see the hourly forecast.")
        pass_h = True
    else:
        print(Fore.RED + f"Please enter a proper value! (yes, y, YES, Y, no, n, NO, N)")

# Fetch daily forecasts
pass_d = False
print("\n\n")
while not pass_d:
    day  = input(str(Fore.LIGHTBLUE_EX + f"Do you want to see tomorrow's forecast? (NOT YET WORKING :))\n: "))
    yea  = {"yes", "y", "YES", "Y"}
    nah  = {"no", "n", "NO", "N"}
    if day in yea:
        daily_forecasts = fetch_daily_forecasts(city)
        # compare_future_forecasts(daily_forecasts["weatherapi"], daily_forecasts["openweather"], forecast_type="daily") # Cannot fetch OpenWeather daily data
        pass_d = True
        # print(daily_forecasts)
    elif day in nah:
        print(Fore.LIGHTBLUE_EX + f"You do not want to see tomorrow's forecast.")
        pass_d = True
    else:
        print(Fore.RED + f"Please enter a proper value! (yes, y, YES, Y, no, n, NO, N)")

print(Fore.LIGHTCYAN_EX + f"\nProgram execution successful.")

# TODO: Add city 2 and create comparison between the results generated for both cities
# !!! Number of cities being checked per run is equal to number of API calls (Counter is not!)
#city02 = input(str(Fore.LIGHTBLUE_EX + f"Enter name of second city : "))
#show_forecast_results(city02)

# TODO: Fix AccuWeather data fetching
#city = "Brussels"
#location_key = fetch_accuweather_location(city)
#if location_key:
#    weather_data = fetch_accuweather_weather(location_key)

# TODO: Fix OpenWeather daily data not being fetched so I can do a comparisson!
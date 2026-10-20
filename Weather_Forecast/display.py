"""Print, compare and average the weather data from all providers."""
import time
from typing import Any

from colorama import Fore

from openweather import fetch_openweather
from weatherapi import fetch_weatherapi
from weatherstack import fetch_weatherstack

Weather = dict[str, Any] | None


def compare_forecasts(openw_d: Weather, wapi_d: Weather, wstk_d: Weather) -> None:
    """Print where the three providers agree or differ for the current weather."""
    print(Fore.LIGHTGREEN_EX + "\n        | Data Comparing |")

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
        print(Fore.RED + "ERROR_07: Comparing data")
        return None

def compare_future_forecasts(forecast1: list[dict[str, Any]], forecast2: list[dict[str, Any]], forecast_type: str = 'hourly') -> None:
    """Print the difference and average between two hourly or daily forecasts, entry by entry."""
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

def calc_average(openw_d: Weather, wapi_d: Weather, wstk_d: Weather) -> None:
    """Print the average of the three providers' current weather."""
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
        print(Fore.RED + "ERROR_09: Calculating average")
        return None

def show_forecast_results(city: str) -> None:
    """Fetch the current weather from all providers and print each report, the comparison and the average."""
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
            print(Fore.RED + "ERROR_10: Couldn't fetch OpenWeather!\n")

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
            print(Fore.RED + "ERROR_11: Couldn't fetch WeatherAPI!\n")

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
            print(Fore.RED + "ERROR_12: Couldn't fetch WeatherStack!\n")
        
        # Compare Data From All Forecasts
        compare_forecasts(openw_d, wapi_d, wstk_d)
        # Show Calculated Average Forecast Data
        calc_average(openw_d, wapi_d, wstk_d)

    else:
        print(Fore.RED + "ERROR_13: Couldn't fetch anything...\n")
        return None

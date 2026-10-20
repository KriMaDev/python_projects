import time

from colorama import Fore, init

from display import compare_future_forecasts, show_forecast_results
from forecasts import fetch_daily_forecasts, fetch_hourly_forecasts

# Initialize colorama for Windows compatibility
init(autoreset=True)

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
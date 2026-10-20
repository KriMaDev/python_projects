"""Compare the current weather and today's hourly forecast for a city across three weather APIs."""
import argparse
import time

from colorama import Fore, init

from display import compare_future_forecasts, show_forecast_results
from forecasts import fetch_hourly_forecasts

YES = {"yes", "y", "1", "true"}
NO  = {"no", "n", "0", "false"}


def parse_yes_no(answer: str) -> bool | None:
    """Turn a yes/no answer into True/False, or None if it is neither."""
    answer = answer.strip().lower()
    if answer in YES:
        return True
    if answer in NO:
        return False
    return None


def ask_yes_no(question: str) -> bool:
    """Keep asking until the user answers yes or no."""
    while True:
        answer = parse_yes_no(input(Fore.LIGHTBLUE_EX + f"{question}\n: "))
        if answer is not None:
            return answer
        print(Fore.RED + "Please enter a proper value! (yes, y, no, n)")


def show_hourly_forecast(city: str) -> None:
    """Fetch and print the hourly comparison between WeatherAPI and OpenWeather."""
    hourly_forecasts = fetch_hourly_forecasts(city)
    if hourly_forecasts:
        compare_future_forecasts(hourly_forecasts["weatherapi"], hourly_forecasts["openweather"], forecast_type="hourly")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("city", nargs="?", help="city to check (asked interactively if omitted)")
    parser.add_argument("--hourly", action=argparse.BooleanOptionalAction, default=None,
                        help="show or skip today's hourly forecast (asked interactively if omitted)")
    args = parser.parse_args()

    # Initialize colorama for Windows compatibility
    init(autoreset=True)

    city = args.city or input(Fore.LIGHTBLUE_EX + "Enter name of city\n: ").strip()
    if not city:
        print(Fore.RED + "No city given.")
        return
    show_forecast_results(city)

    print("\n\n")
    hourly = args.hourly
    if hourly is None:
        hourly = ask_yes_no(f"Do you want to see the hourly forecast for today? ({time.strftime('%d/%m/%Y')})")
    if hourly:
        show_hourly_forecast(city)
    else:
        print(Fore.LIGHTBLUE_EX + "You do not want to see the hourly forecast.")

    print(Fore.LIGHTCYAN_EX + "\nProgram execution successful.")


if __name__ == "__main__":
    main()

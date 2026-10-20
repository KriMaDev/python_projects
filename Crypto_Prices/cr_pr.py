"""Live cryptocurrency prices from CoinGecko, coloured green/red when they go up/down. Press 'esc' to exit."""
import argparse
import threading
import time

import keyboard
import requests
from colorama import Fore, init

API_URL         = "https://api.coingecko.com/api/v3/simple/price"
DEFAULT_COINS   = "bitcoin,ethereum,cronos,pepe,pax-gold"
REQUEST_TIMEOUT = 10

# Create a global stop flag
stop_flag = threading.Event()

# =======================================================================================================================
#                                                                                                     FUNCTION DEFINITION
# =======================================================================================================================

def format_price(price: object) -> str:
    """Format a price with 8 decimals below $1 and 2 decimals otherwise, or 'N/A' if it isn't a number."""
    if isinstance(price, (float, int)):  # Handle both floats and integers
        return f"{price:.8f}" if price < 1 else f"{price:.2f}"
    return 'N/A'


def price_direction(price: object, prev_price: object) -> str:
    """Return '↑', '↓' or '-' comparing a price with the previous one. Missing prices count as no change."""
    if not isinstance(price, (float, int)) or not isinstance(prev_price, (float, int)):
        return '-'
    if price > prev_price:
        return '↑'
    if price < prev_price:
        return '↓'
    return '-'


# Function to listen for the exit key
def listen_for_exit() -> None:
    """Block until 'esc' is pressed, then tell the price thread to stop."""
    keyboard.wait('esc')  # Wait for the 'esc' key press
    print("Exiting program...")
    stop_flag.set()  # Signal the stop flag to stop the other thread


def fetch_prices(coins: list[str], interval: float) -> None:
    """Fetch and print the USD price of each coin every `interval` seconds until stop_flag is set."""
    previous_prices: dict[str, object] = {}

    while not stop_flag.is_set():
        try:
            response = requests.get(API_URL, params={"ids": ",".join(coins), "vs_currencies": "usd"}, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data     = response.json()

            # Get the current prices (as raw numerical values)
            current_prices = {coin: data.get(coin, {}).get('usd', 'N/A') for coin in coins}

            # Display the current prices and compare with the previous prices
            display_prices(current_prices, previous_prices)

            # Update previous prices for the next iteration (store raw prices)
            previous_prices = current_prices.copy()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

        # Sleep for a while or until stop_flag is set
        stop_flag.wait(interval)


def display_prices(prices: dict[str, object], previous_prices: dict[str, object]) -> None:
    """Print one line per coin, coloured by the direction of the price since the last fetch."""
    colors = {'↑': Fore.GREEN, '↓': Fore.RED, '-': Fore.WHITE}
    # Calculate the maximum length of the coin names for alignment
    max_coin_length = max(len(coin.capitalize()) for coin in prices.keys())

    for coin, price in prices.items():
        direction = price_direction(price, previous_prices.get(coin))
        # Format the coin name to be of consistent width
        coin_name_formatted = f"{coin.capitalize():<{max_coin_length}}"
        # Print the coin name, price, and the arrow in the corresponding color
        print(f"{colors[direction]}| {time.strftime('%d/%m/%Y %H:%M:%S')} | {direction} | {coin_name_formatted} : ${format_price(price)}")

# =======================================================================================================================
#                                                                                             THREAD CREATION / EXECUTION
# =======================================================================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coins", default=DEFAULT_COINS,
                        help=f"comma separated CoinGecko coin IDs (default: {DEFAULT_COINS}). Find IDs with coin_list.py")
    parser.add_argument("--interval", type=float, default=15, help="seconds between updates (default: 15)")
    args = parser.parse_args()
    coins = [coin.strip() for coin in args.coins.split(",") if coin.strip()]

    # Initialize colorama for Windows compatibility
    init(autoreset=True)

    print(f"\n\nTo exit the program please press 'esc'\nCoins: {', '.join(coins)}\n")
    # Start fetching prices and listening for exit key in separate threads
    cash_thread  = threading.Thread(target=fetch_prices, args=(coins, args.interval))
    exit_thread  = threading.Thread(target=listen_for_exit, daemon=True)

    cash_thread.start()
    exit_thread.start()

    # Keep the main thread alive until the price thread finishes
    cash_thread.join()


if __name__ == "__main__":
    main()

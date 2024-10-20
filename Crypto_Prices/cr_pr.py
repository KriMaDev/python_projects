import time
import threading
import requests
import keyboard
from colorama import Fore, init

# Create a global stop flag
stop_flag = threading.Event()

# Initialize colorama for Windows compatibility
init(autoreset=True)

# =======================================================================================================================
#                                                                                                     FUNCTION DEFINITION
# =======================================================================================================================

# Function to format the price properly
def format_price(price):
    if isinstance(price, (float, int)):  # Handle both floats and integers
        return f"{price:.8f}" if price < 1 else f"{price:.2f}"
    return 'N/A'

# Function to listen for the exit key
def listen_for_exit():
    keyboard.wait('esc')  # Wait for the 'esc' key press
    print("Exiting program...")
    stop_flag.set()  # Signal the stop flag to stop the other thread

# Function to fetch cryptocurrency prices
def fetch_prices():
    ids             = "bitcoin,ethereum,cronos,pepe,pax-gold"
    previous_prices = {}

    while not stop_flag.is_set():
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd')
            response.raise_for_status()
            data     = response.json()

            #print("API response:", data)  # For debugging

            # Get the current prices (as raw numerical values)
            current_prices = {
                'bitcoin':  data.get('bitcoin', {}).get('usd', 'N/A'),
                'ethereum': data.get('ethereum', {}).get('usd', 'N/A'),
                'cronos':   data.get('cronos', {}).get('usd', 'N/A'),
                'pepe':     data.get('pepe', {}).get('usd', 'N/A'),
                'pax-gold': data.get('pax-gold', {}).get('usd', 'N/A'),
            }

            # Display the current prices and compare with the previous prices
            display_prices(current_prices, previous_prices)  # Call the display function

            # Update previous prices for the next iteration (store raw prices)
            previous_prices = current_prices.copy()

            # Sleep for a while or until stop_flag is set
            stop_flag.wait(15)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            stop_flag.wait(15)

# Function to display prices based on previous price
def display_prices(prices, previous_prices):
    # Calculate the maximum length of the coin names for alignment
    max_coin_length = max(len(coin.capitalize()) for coin in prices.keys())

    for coin, price in prices.items():
        if coin in previous_prices:
            prev_price = previous_prices[coin]
            if price > prev_price:
                color = Fore.GREEN  # Set color to green for price increase
                direction = '↑'
            elif price < prev_price:
                color = Fore.RED  # Set color to red for price decrease
                direction = '↓'
            else:
                color = Fore.WHITE  # No change, so white (or no color)
                direction = '-'
        else:
            color = Fore.WHITE
            direction = '-'

        # Format the coin name to be of consistent width
        coin_name_formatted = f"{coin.capitalize():<{max_coin_length}}"
        # Print the coin name, price, and the arrow in the corresponding color
        print(f"{color}| {time.strftime('%d/%m/%Y %H:%M:%S')} | {direction} | {coin_name_formatted} : ${format_price(price)}")


# =======================================================================================================================
#                                                                                             THREAD CREATION / EXECUTION
# =======================================================================================================================

print("\n\nTo exit the program please press 'esc'\nPredefined coins:\n")
# Start fetching prices and listening for exit key in separate threads
cash_thread  = threading.Thread(target=fetch_prices)
exit_thread  = threading.Thread(target=listen_for_exit)

cash_thread.start()
exit_thread.start()

# Keep the main thread alive until the price thread finishes
cash_thread.join()
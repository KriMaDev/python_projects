"""Print all coins known to CoinGecko with their ID, which cr_pr.py --coins expects."""
import argparse
from typing import Any

import requests

API_URL         = "https://api.coingecko.com/api/v3/coins/list"
REQUEST_TIMEOUT = 30


def get_coin_list() -> list[dict[str, Any]] | None:
    """Fetch the full CoinGecko coin list, or None if the request fails."""
    try:
        response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the coin list! {e}")
        return None
    if response.status_code == 200:
        return response.json()
    print(f"Failed to fetch the coin list! (HTTP {response.status_code})")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    # Limited at 9001 by default because thats default terminal buffer size
    parser.add_argument("--limit", type=int, default=9001, help="maximum number of coins to print (default: 9001)")
    parser.add_argument("--search", help="only show coins whose symbol, ID or name contains this text")
    args = parser.parse_args()

    print("Attempting to fetch coin list...")
    coins = get_coin_list()
    if not coins:
        return

    if args.search:
        term  = args.search.lower()
        coins = [c for c in coins if term in c['symbol'].lower() or term in c['id'].lower() or term in c['name'].lower()]

    # Print coins to check their IDs
    print("{:<20} {:<20} {:<60} {:<40}".format("Number", "Symbol", "ID", "Name"))
    print("="*140)
    for cc, coin in enumerate(coins[:args.limit], start=1):
        print("{:<20} {:<20} {:<60} {:<40}".format(cc, coin['symbol'], coin['id'], coin['name']))


if __name__ == "__main__":
    main()

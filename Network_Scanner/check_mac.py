# This script checks the MAC address using the maclookup API.
# It is a free API so note that it has a request limit of 1000 requests per month.
# The program simply checks a predefined MAC address or a user-inputted MAC address.
# It then prints out the details of the MAC address such as company, address, country, etc.
"""Look up the vendor of a MAC address with the maclookup.app API."""
import argparse
import re

import requests

EXAMPLE_MAC     = "AA:BB:CC:DD:EE:FF"
REQUEST_TIMEOUT = 10


def is_valid_mac(mac_address: str) -> bool:
    """Return True for a 6 byte MAC like AA:BB:CC:DD:EE:FF, aa-bb-cc-dd-ee-ff or AABBCCDDEEFF."""
    return bool(re.fullmatch(r"[0-9A-Fa-f]{2}([:-]?)(?:[0-9A-Fa-f]{2}\1){4}[0-9A-Fa-f]{2}", mac_address))


def ask_mac_address() -> str | None:
    """Ask whether to type a MAC address or use the example one."""
    # Check type of user input
    chk = input(f"'1 + Enter' to manually enter MAC Address \n'2 + Enter' to use predefined MAC Address: {EXAMPLE_MAC}\n: ")
    if chk == "1":
        return input("Enter MAC Address: ").strip()
    elif chk == "2":
        return EXAMPLE_MAC
    print("Invalid option. Exiting.")
    return None


def lookup_mac(mac_address: str) -> None:
    """Fetch and print the vendor details for a MAC address."""
    # API URL
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"

    try:
        # Send the GET request and parse the response
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        # Display relevant information
        fields = {
            "Exists & Found": f"{data.get('success', 'N/A')} & {data.get('found', 'N/A')}",
            "Random & Private": f"{data.get('isRand', 'N/A')} & {data.get('isPrivate', 'N/A')}",
            "Company": data.get("company", "N/A"),
            "Address": data.get("address", "N/A"),
            "Country": data.get("country", "N/A"),
            "Updated": data.get("updated", "N/A"),
            "MAC Prefix": data.get("macPrefix", "N/A"),
            "Block Start": data.get("blockStart", "N/A"),
            "Block End": data.get("blockEnd", "N/A"),
            "Block Size": data.get("blockSize", "N/A"),
            "Block Type": data.get("blockType", "N/A"),
        }
        print(f"For MAC Address {mac_address}")
        for key, value in fields.items():
            print(f"{key}: {value}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError:
        print("Unexpected response format. The API might have changed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mac", nargs="?", help="MAC address to look up (asked interactively if omitted)")
    args = parser.parse_args()

    mac_address = args.mac or ask_mac_address()
    if mac_address is None:
        return
    if not is_valid_mac(mac_address):
        print(f"'{mac_address}' is not a valid MAC address (expected e.g. {EXAMPLE_MAC}).")
        return
    lookup_mac(mac_address)


if __name__ == "__main__":
    main()

import requests

mac_address = "20:28:bc:25:27:8e"

# Correct API URL
url = f"https://api.maclookup.app/v2/macs/{mac_address}"

try:
    # Send the GET request
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

    # Parse the JSON response
    data = response.json()
    print(f"MAC Address: {data['mac']}")
    print(f"Company: {data['company']}")
    print(f"Address: {data['address']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except KeyError:
    print("Unexpected response format. The API might have changed.")

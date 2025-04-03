import requests

mac_address = "20:28:bc:25:27:8e"

# Correct API URL
url = f"https://api.maclookup.app/v2/macs/{mac_address}"

try:
    # Send the GET request
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTP Error for bad responses (4xx and 5xx)

    # Parse the JSON response
    data = response.json()
    # print(data)
    print(f"For MAC Address {mac_address}")
    print(f"Exists & Found: {data['success']} & {data['found']}")
    print(f"Random & Private: {data['isRand']} & {data['isPrivate']}")
    print(f"Company: {data['company']}")
    print(f"Address: {data['address']}")
    print(f"Country: {data['country']}")
    print(f"Updated: {data['updated']}")
    print(f"MAC Prefix: {data['macPrefix']}")
    print(f"Block Start: {data['blockStart']}")
    print(f"Block End: {data['blockEnd']}")
    print(f"Block Size: {data['blockSize']}")
    print(f"Block Type: {data['blockType']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except KeyError:
    print("Unexpected response format. The API might have changed.")


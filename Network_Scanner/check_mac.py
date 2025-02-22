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
    # print(data)
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

{'success': True, 'found': True, 'macPrefix': '2028BC', 'company': 'Visionscape Co,. Ltd.', 
'address': '503, 145, Gasan Digital 1-ro, Geumcheon-gu,, Seoul Korea 153-787, KR', 'country': 'KR',
 'blockStart': '2028BC000000', 'blockEnd': '2028BCFFFFFF', 'blockSize': 16777215, 'blockType': 'MA-L',
  'updated': '2015-11-17', 'isRand': False, 'isPrivate': False}

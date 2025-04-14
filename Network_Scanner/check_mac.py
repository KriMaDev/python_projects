# This script checks the MAC address using the maclookup API.
# It is a free API so note that it has a request limit of 1000 requests per month.
# The program simply checks a predefined MAC address or a user-inputted MAC address.
# It then prints out the details of the MAC address such as company, address, country, etc.
import requests

# Check type of user input
chk = input("'1 + Enter' to manually enter MAC Address \n'2 + Enter' to use predefined MAC Address: 20:28:bc:25:27:8e\n: ")
if chk == "1":
    mac_address = input("Enter MAC Address: ")
elif chk == "2":
    mac_address = "20:28:bc:25:27:8e"
else:
    print("Invalid option. Exiting.")
    exit()

# API URL
url = f"https://api.maclookup.app/v2/macs/{mac_address}"

try:
    # Send the GET request and parse the response
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # print(data)  # Uncomment to see the full response

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


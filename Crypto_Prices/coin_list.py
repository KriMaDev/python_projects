import requests

def get_coin_list():
    url       = "https://api.coingecko.com/api/v3/coins/list"
    response  = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        return coins
    else:
        print("Failed to fetch the coin list!")
        return None

print("Attempting to fetch coin list...")
coins = get_coin_list()

# Print coins to check their IDs
if coins:
    cc = 1
    print("{:<20} {:<20} {:<60} {:<40}".format("Number", "Symbol", "ID", "Name"))
    print("="*140)
    for coin in coins[:9001]:  # Limited at 9001 because thats default terminal buffer size
        print("{:<20} {:<20} {:<60} {:<40}".format(cc, coin['symbol'], coin['id'], coin['name']))
        cc += 1
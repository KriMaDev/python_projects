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

coins = get_coin_list()

# Print coins to check their IDs
if coins:
    cc = 1
    for coin in coins:  # for coin in coins[:100]:  For limited number of results
        print(f"Number: {cc} | ID: {coin['id']} | Symbol: {coin['symbol']} | Name: {coin['name']} ")
        cc += 1
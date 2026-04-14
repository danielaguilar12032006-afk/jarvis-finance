import requests

def get_price():
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSDT"
    response = requests.get(url)
    data = response.json()

    return float(data["result"]["XBTUSDT"]["c"][0])
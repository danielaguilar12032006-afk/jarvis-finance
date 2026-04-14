import ccxt
from config.settings import SYMBOLS

exchange = ccxt.kraken()

def get_prices():
    prices = {}

    for coin, symbol in SYMBOLS.items():
        try:
            ticker = exchange.fetch_ticker(symbol)
            prices[coin] = ticker["last"]
        except Exception as e:
            print("Error fetching {}: {}".format(coin, e))

    return prices

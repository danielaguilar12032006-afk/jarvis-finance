import ccxt
from config.settings import SYMBOL

exchange = ccxt.kraken()

def get_price():
    ticker = exchange.fetch_ticker(SYMBOL)
    return ticker["last"]

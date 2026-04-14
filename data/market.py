import ccxt

exchange = ccxt.kraken()

SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

def get_prices():
    prices = {}

    for symbol in SYMBOLS:
        try:
            ticker = exchange.fetch_ticker(symbol)
            coin = symbol.split("/")[0]
            prices[coin] = ticker["last"]
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return prices

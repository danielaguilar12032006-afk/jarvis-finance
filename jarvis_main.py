import ccxt
import os
import time

print("Jarvis corriendo...")

api_key = os.getenv("TU_API_KEY").strip()
api_secret = os.getenv("TU_API_SECRET").strip()

api_secret = api_secret.replace(" ", "").replace("\n", "")

exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

while True:
    try:
        ticker = exchange.fetch_ticker('BTC/USD')
        price = ticker['last']

        print("BTC price:", price)

        time.sleep(10)

    except Exception as e:
        print("Error general:", str(e))
        time.sleep(10)

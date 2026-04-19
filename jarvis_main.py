import ccxt
import os
import time

print("Jarvis trading iniciado...")

api_key = os.getenv("TU_API_KEY").strip()
api_secret = os.getenv("TU_API_SECRET").strip()

api_secret = api_secret.replace(" ", "").replace("\n", "")

exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

symbol = 'BTC/USD'
min_usd = 10  # mínimo Kraken aprox
trade_usd = 12  # lo que intentará usar

last_price = None
position = False

while True:
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']

        print("Precio:", price)

        if last_price is None:
            last_price = price
            time.sleep(10)
            continue

        change = (price - last_price) / last_price

        balance = exchange.fetch_balance()
        usd_balance = balance['free'].get('USD', 0)
        btc_balance = balance['free'].get('BTC', 0)

        # 📉 BAJA → COMPRA
        if change < -0.002 and not position:
            print("🔻 Bajó, intentando comprar...")

            usd_to_use = min(trade_usd, usd_balance)

            if usd_to_use >= min_usd:
                amount_btc = usd_to_use / price
                order = exchange.create_market_buy_order(symbol, amount_btc)
                print("✅ BUY ejecutado:", order)
                position = True
            else:
                print("⚠️ No hay suficiente USD para cumplir mínimo")

        # 📈 SUBE → VENDE
        elif change > 0.002 and position:
            print("🔺 Subió, intentando vender...")

            if btc_balance > 0:
                order = exchange.create_market_sell_order(symbol, btc_balance)
                print("✅ SELL ejecutado:", order)
                position = False
            else:
                print("⚠️ No hay BTC para vender")

        last_price = price
        time.sleep(10)

    except Exception as e:
        print("Error general:", str(e))
        time.sleep(10)

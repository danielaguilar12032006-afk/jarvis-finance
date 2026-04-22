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
min_usd = 10
trade_usd = 12

prices = []  # memoria de precios
position = False

while True:
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']

        print("Precio:", price)

        prices.append(price)

        # mantener últimos 5 precios
        if len(prices) > 5:
            prices.pop(0)

        # esperar a tener datos
        if len(prices) < 5:
            time.sleep(10)
            continue

        base_price = prices[0]
        change = (price - base_price) / base_price

        print("Cambio real:", change)

        balance = exchange.fetch_balance()
        usd_balance = balance['free'].get('USD', 0)
        btc_balance = balance['free'].get('BTC', 0)

        # 📉 BAJA → COMPRA
        if change < -0.0005 and not position:
            print("🔻 Bajó vs base, comprando...")

            usd_to_use = min(trade_usd, usd_balance)

            if usd_to_use >= min_usd:
                amount_btc = usd_to_use / price
                order = exchange.create_market_buy_order(symbol, amount_btc)
                print("✅ BUY ejecutado:", order)
                position = True

        # 📈 SUBE → VENDE
        elif change > 0.0005 and position:
            print("🔺 Subió vs base, vendiendo...")

            if btc_balance > 0:
                order = exchange.create_market_sell_order(symbol, btc_balance)
                print("✅ SELL ejecutado:", order)
                position = False

        time.sleep(10)

    except Exception as e:
        print("Error general:", str(e))
        time.sleep(10)

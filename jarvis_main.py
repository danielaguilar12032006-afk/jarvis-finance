import ccxt
import os
import time

print("Jarvis trading iniciado...")

api_key = os.getenv("TU_API_KEY").strip()
api_secret = os.getenv("TU_API_SECRET").strip()

exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

symbol = 'BTC/USD'
min_usd = 10
trade_usd = 10  # ajustado al mínimo real

prices = []
position = False

while True:
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']

        print("Precio:", price)

        prices.append(price)
        if len(prices) > 5:
            prices.pop(0)

        if len(prices) < 5:
            time.sleep(10)
            continue

        base_price = prices[0]
        change = (price - base_price) / base_price

        print("Cambio real:", change)

        balance = exchange.fetch_balance()

        usd_balance = (
            balance['free'].get('USD', 0) +
            balance['free'].get('ZUSD', 0) +
            balance['free'].get('USD.F', 0)
        )

        btc_balance = balance['free'].get('BTC', 0)

        print("USD disponible:", usd_balance)
        print("BTC disponible:", btc_balance)

        # 🔻 COMPRA
        if change < -0.0005 and not position:
            print("Intentando BUY...")

            usd_to_use = min(trade_usd, usd_balance)

            if usd_to_use < min_usd:
                print("❌ No hay suficiente USD")
            else:
                amount_btc = usd_to_use / price

                try:
                    order = exchange.create_market_buy_order(symbol, amount_btc)
                    print("✅ BUY REAL ejecutado:", order)
                    position = True
                except Exception as e:
                    print("❌ ERROR BUY:", str(e))

        # 🔺 VENTA
        elif change > 0.0005 and position:
            print("Intentando SELL...")

            if btc_balance <= 0:
                print("❌ No hay BTC para vender")
            else:
                try:
                    order = exchange.create_market_sell_order(symbol, btc_balance)
                    print("✅ SELL REAL ejecutado:", order)
                    position = False
                except Exception as e:
                    print("❌ ERROR SELL:", str(e))

        time.sleep(10)

    except Exception as e:
        print("Error general:", str(e))
        time.sleep(10)

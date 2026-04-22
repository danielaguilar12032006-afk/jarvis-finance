import ccxt
import time
import os

# ==============================
# CONFIG
# ==============================

SYMBOLS = [
    "ETH/CAD",
    "BTC/CAD",
    "SOL/CAD"
]

MIN_CAD = 5
TRADE_AMOUNT = 5
SLEEP_TIME = 10

# ==============================
# EXCHANGE (ENV VARIABLES)
# ==============================

exchange = ccxt.kraken({
    'apiKey': os.getenv("API_KEY"),
    'secret': os.getenv("API_SECRET"),
    'enableRateLimit': True
})

# ==============================
# BASE PRICES
# ==============================

base_prices = {}

print("Jarvis trading iniciado...")

# ==============================
# LOOP
# ==============================

while True:
    try:
        balance = exchange.fetch_balance()
        cad_balance = balance['total'].get('CAD', 0)

        print(f"\n💰 CAD disponible: {cad_balance}")

        for symbol in SYMBOLS:
            try:
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']

                print(f"{symbol} precio: {price}")

                # guardar primer precio
                if symbol not in base_prices:
                    base_prices[symbol] = price
                    continue

                change = (price - base_prices[symbol]) / base_prices[symbol]
                print(f"{symbol} cambio: {change}")

                # ==============================
                # BUY
                # ==============================
                if change < -0.001:
                    print(f"🔻 {symbol} bajó")

                    if cad_balance >= MIN_CAD:
                        amount = TRADE_AMOUNT / price

                        exchange.create_market_buy_order(symbol, amount)

                        print(f"🟢 BUY {symbol} | {amount}")
                        base_prices[symbol] = price

                    else:
                        print("❌ Sin CAD suficiente")

                # ==============================
                # SELL
                # ==============================
                elif change > 0.001:
                    print(f"🔺 {symbol} subió")

                    asset = symbol.split('/')[0]
                    asset_balance = balance['total'].get(asset, 0)

                    if asset_balance > 0:
                        exchange.create_market_sell_order(symbol, asset_balance)

                        print(f"🔴 SELL {symbol} | {asset_balance}")
                        base_prices[symbol] = price

            except Exception as e:
                print(f"Error con {symbol}: {e}")

        time.sleep(SLEEP_TIME)

    except Exception as e:
        print("Error general:", e)
        time.sleep(10)

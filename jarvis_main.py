import ccxt
import time

# ==============================
# CONFIG
# ==============================

API_KEY = "TU_API_KEY"
API_SECRET = "TU_API_SECRET"

SYMBOLS = [
    "ETH/CAD",
    "BTC/CAD",
    "SOL/CAD"
]

MIN_CAD = 5        # mínimo para comprar
TRADE_AMOUNT = 5   # cuánto usar por trade
SLEEP_TIME = 10    # segundos

# ==============================
# EXCHANGE
# ==============================

exchange = ccxt.kraken({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# ==============================
# BASE DE PRECIOS
# ==============================

base_prices = {}

# ==============================
# LOOP
# ==============================

print("Jarvis trading iniciado...")

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

                # guardar precio base
                if symbol not in base_prices:
                    base_prices[symbol] = price
                    continue

                change = (price - base_prices[symbol]) / base_prices[symbol]
                print(f"{symbol} cambio: {change}")

                # ==============================
                # COMPRA
                # ==============================
                if change < -0.001:  # bajó
                    print(f"🔻 {symbol} bajó, intentando comprar...")

                    if cad_balance >= MIN_CAD:
                        amount = TRADE_AMOUNT / price

                        order = exchange.create_market_buy_order(symbol, amount)

                        print(f"✅ COMPRA hecha en {symbol}: {amount}")
                        base_prices[symbol] = price

                    else:
                        print("❌ No hay suficiente CAD")

                # ==============================
                # VENTA
                # ==============================
                elif change > 0.001:  # subió
                    print(f"🔺 {symbol} subió, intentando vender...")

                    asset = symbol.split('/')[0]
                    asset_balance = balance['total'].get(asset, 0)

                    if asset_balance > 0:
                        order = exchange.create_market_sell_order(symbol, asset_balance)

                        print(f"💰 VENTA hecha en {symbol}: {asset_balance}")
                        base_prices[symbol] = price

            except Exception as e:
                print(f"Error con {symbol}: {str(e)}")

        time.sleep(SLEEP_TIME)

    except Exception as e:
        print("Error general:", str(e))
        time.sleep(10)

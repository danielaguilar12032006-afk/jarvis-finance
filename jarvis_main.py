import ccxt
import time
import os

# ==============================
# CONFIG
# ==============================

SYMBOLS = ["BTC/CAD", "ETH/CAD", "SOL/CAD"]
MONTO_COMPRA_CAD = 6
TIEMPO_ESPERA = 10

# ==============================
# EXCHANGE
# ==============================

exchange = ccxt.kraken({
    'apiKey': os.getenv("API_KEY"),
    'secret': os.getenv("API_SECRET"),
    'enableRateLimit': True
})

# ==============================
# BALANCE (CORREGIDO KRAKEN)
# ==============================

def obtener_balance(asset):
    try:
        balance = exchange.fetch_balance()

        mapping = {
            "CAD": ["CAD", "ZCAD"],
            "BTC": ["BTC", "XBT", "XXBT"],
            "ETH": ["ETH", "XETH"],
            "SOL": ["SOL"]
        }

        posibles = mapping.get(asset, [asset])

        for nombre in posibles:
            if nombre in balance['free']:
                return balance['free'][nombre]

        return 0

    except Exception as e:
        print(f"Error balance {asset}: {e}")
        return 0


# ==============================
# COMPRA
# ==============================

def comprar(symbol, monto_cad):
    try:
        ticker = exchange.fetch_ticker(symbol)
        precio = ticker['last']

        cantidad = monto_cad / precio

        print(f"🟢 BUY {symbol} | {cantidad}")

        order = exchange.create_market_buy_order(symbol, cantidad)
        print(f"✅ Compra ejecutada")

    except Exception as e:
        print(f"❌ Error compra {symbol}: {e}")


# ==============================
# VENTA
# ==============================

def vender(symbol):
    try:
        asset = symbol.split("/")[0]
        balance = obtener_balance(asset)

        if balance <= 0:
            print(f"❌ No hay {asset} para vender")
            return

        print(f"🔴 SELL {symbol} | {balance}")

        order = exchange.create_market_sell_order(symbol, balance)
        print(f"✅ Venta ejecutada")

    except Exception as e:
        print(f"❌ Error venta {symbol}: {e}")


# ==============================
# BASE DE PRECIOS
# ==============================

precios_base = {}

print("Jarvis PRO iniciado...")

# ==============================
# LOOP
# ==============================

while True:
    try:
        cad_balance = obtener_balance("CAD")
        print(f"\n💰 CAD disponible: {cad_balance}")

        for symbol in SYMBOLS:
            try:
                ticker = exchange.fetch_ticker(symbol)
                precio_actual = ticker['last']

                if symbol not in precios_base:
                    precios_base[symbol] = precio_actual
                    continue

                cambio = (precio_actual - precios_base[symbol]) / precios_base[symbol]

                print(f"{symbol} | Precio: {precio_actual} | Cambio: {cambio}")

                # 📉 COMPRA
                if cambio < -0.004:
                    if cad_balance >= MONTO_COMPRA_CAD:
                        print(f"📉 {symbol} bajó → COMPRAR")
                        comprar(symbol, MONTO_COMPRA_CAD)
                        precios_base[symbol] = precio_actual
                    else:
                        print("❌ Sin CAD suficiente")

                # 📈 VENTA
                elif cambio > 0.008:
                    print(f"📈 {symbol} subió → VENDER")
                    vender(symbol)
                    precios_base[symbol] = precio_actual

            except Exception as e:
                print(f"Error con {symbol}: {e}")

        time.sleep(TIEMPO_ESPERA)

    except Exception as e:
        print(f"⚠️ Error general: {e}")
        time.sleep(5)

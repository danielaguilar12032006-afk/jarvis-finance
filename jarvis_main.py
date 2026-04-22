import ccxt
import time

# 🔐 API CONFIG
exchange = ccxt.kraken({
    'apiKey': 'TU_API_KEY',
    'secret': 'TU_API_SECRET',
    'enableRateLimit': True
})

# ⚙️ CONFIG
SYMBOLS = ["BTC/CAD", "ETH/CAD", "SOL/CAD"]
MONTO_COMPRA_CAD = 6  # mínimo real
TIEMPO_ESPERA = 10  # segundos

# 📊 BASE DE PRECIOS
precios_base = {}


# =========================
# 🔍 BALANCES
# =========================
def obtener_balance(asset):
    try:
        balance = exchange.fetch_balance()
        return balance['free'].get(asset, 0)
    except Exception as e:
        print(f"Error balance {asset}: {e}")
        return 0


# =========================
# 💰 COMPRA
# =========================
def comprar(symbol, monto_cad):
    try:
        ticker = exchange.fetch_ticker(symbol)
        precio = ticker['last']

        cantidad = monto_cad / precio

        print(f"🟢 BUY {symbol} | {cantidad}")

        order = exchange.create_market_buy_order(symbol, cantidad)
        print(f"✅ Compra ejecutada: {order}")

    except Exception as e:
        print(f"❌ Error compra {symbol}: {e}")


# =========================
# 💸 VENTA
# =========================
def vender(symbol):
    try:
        asset = symbol.split("/")[0]
        balance = obtener_balance(asset)

        if balance <= 0:
            print(f"❌ No hay {asset} para vender")
            return

        print(f"🔴 SELL {symbol} | {balance}")

        order = exchange.create_market_sell_order(symbol, balance)
        print(f"✅ Venta ejecutada: {order}")

    except Exception as e:
        print(f"❌ Error venta {symbol}: {e}")


# =========================
# 🧠 LOOP PRINCIPAL
# =========================
while True:
    try:
        cad_balance = obtener_balance("CAD")
        print(f"\n💰 CAD disponible: {cad_balance}")

        for symbol in SYMBOLS:
            ticker = exchange.fetch_ticker(symbol)
            precio_actual = ticker['last']

            # Inicializar base
            if symbol not in precios_base:
                precios_base[symbol] = precio_actual
                continue

            cambio = (precio_actual - precios_base[symbol]) / precios_base[symbol]

            print(f"{symbol} | Precio: {precio_actual} | Cambio: {cambio}")

            # 📉 BAJÓ → COMPRAR
            if cambio < -0.001:
                if cad_balance >= MONTO_COMPRA_CAD:
                    print(f"📉 {symbol} bajó → comprando")
                    comprar(symbol, MONTO_COMPRA_CAD)
                    precios_base[symbol] = precio_actual
                else:
                    print("❌ Sin CAD suficiente")

            # 📈 SUBIÓ → VENDER
            elif cambio > 0.001:
                print(f"📈 {symbol} subió → vendiendo")
                vender(symbol)
                precios_base[symbol] = precio_actual

        time.sleep(TIEMPO_ESPERA)

    except Exception as e:
        print(f"⚠️ Error general: {e}")
        time.sleep(5)

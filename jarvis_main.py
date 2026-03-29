import time
import requests
from datetime import datetime

print("🚀 JARVIS SIMULADOR ESTABLE")

INTERVAL = 60
TRADE_AMOUNT = 100
COOLDOWN = 180  # 3 minutos

balance = 1000
btc = 0
buy_price = None
last_trade_time = 0

# =========================
# 📊 PRECIO BTC
# =========================
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data["price"])

# =========================
# 📈 ESTRATEGIA SIMPLE
# =========================
def get_signal(price, last_price):
    if last_price is None:
        return "HOLD"

    change = (price - last_price) / last_price

    if change > 0.002:   # sube 0.2%
        return "BUY"
    elif change < -0.002:  # baja 0.2%
        return "SELL"
    else:
        return "HOLD"

# =========================
# 🔁 LOOP
# =========================
last_price = None

while True:
    try:
        price = get_price()
        current_time = time.time()
        has_position = btc > 0

        print("\n==============================")
        print("⏱", datetime.now())
        print("💰 Balance:", round(balance, 2))
        print("📦 BTC:", round(btc, 6))
        print("📊 Precio:", price)

        action = get_signal(price, last_price)
        print("🧠 Señal:", action)

        # =========================
        # 🟢 BUY
        # =========================
        if action == "BUY":
            if has_position:
                print("⚠️ Ya tienes BTC")
            elif current_time - last_trade_time < COOLDOWN:
                print("⏳ Cooldown activo")
            elif balance >= TRADE_AMOUNT:
                btc = TRADE_AMOUNT / price
                balance -= TRADE_AMOUNT
                buy_price = price
                last_trade_time = current_time

                print("🟢 COMPRA:", btc)

        # =========================
        # 🔴 SELL
        # =========================
        elif action == "SELL":
            if not has_position:
                print("⚠️ No tienes BTC")
            else:
                balance += btc * price
                print("🔴 VENTA:", btc)

                btc = 0
                buy_price = None
                last_trade_time = current_time

        # =========================
        # 🛑 STOP LOSS / TAKE PROFIT
        # =========================
        if has_position and buy_price:
            change = (price - buy_price) / buy_price

            print("📉 Cambio:", round(change * 100, 2), "%")

            if change <= -0.01:
                print("🛑 STOP LOSS")
                balance += btc * price
                btc = 0
                buy_price = None
                last_trade_time = current_time

            elif change >= 0.01:
                print("💰 TAKE PROFIT")
                balance += btc * price
                btc = 0
                buy_price = None
                last_trade_time = current_time

        last_price = price

        print("🔁 Esperando...\n")
        time.sleep(INTERVAL)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(10)

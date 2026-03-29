import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 JARVIS DEBUG MODE ACTIVADO")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTERVALO = 60

balance = 1000

portfolio = {
    "BTC": 0
}

buy_price = None

# =========================
# 📊 PRECIO
# =========================
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data["price"])

# =========================
# 🧠 DECISIÓN IA (MUY ESTRICTA)
# =========================
def decide_action(price):
    prompt = f"""
    You are a professional crypto scalping bot.

    CURRENT STATE:
    Price: {price}
    Balance: {balance}
    BTC Holding: {portfolio["BTC"]}

    STRICT RULES:
    1. If you ALREADY HOLD BTC → you CANNOT BUY again
    2. If you HOLD BTC:
        - SELL if price is dropping or weak
        - HOLD if stable
    3. If you DO NOT HOLD BTC:
        - BUY only if price is clearly going up
        - HOLD if unclear
    4. Avoid unnecessary trades

    Answer ONLY: BUY, SELL or HOLD
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    decision = response.output_text.strip().upper()
    return decision

# =========================
# 🔁 LOOP PRINCIPAL
# =========================
while True:
    try:
        price = get_price()
        has_position = portfolio["BTC"] > 0

        print("\n==============================")
        print("⏱ Tiempo:", datetime.now())
        print("💰 Balance:", balance)
        print("📦 BTC:", portfolio["BTC"])
        print("📊 Precio:", price)
        print("📍 Tiene posición:", has_position)

        action = decide_action(price)
        print("🧠 IA dice:", action)

        # =========================
        # 🟢 BUY LOGIC
        # =========================
        if action == "BUY":
            if has_position:
                print("❌ ERROR IA: quiso comprar pero YA hay posición")
            elif balance < 100:
                print("❌ ERROR: no hay suficiente balance")
            else:
                amount = 100 / price
                portfolio["BTC"] += amount
                balance -= 100
                buy_price = price

                print("✅ COMPRA EJECUTADA")
                print("   BTC comprado:", amount)
                print("   Precio compra:", buy_price)

        # =========================
        # 🔴 SELL LOGIC
        # =========================
        elif action == "SELL":
            if not has_position:
                print("❌ ERROR IA: quiso vender sin tener BTC")
            else:
                sell_value = portfolio["BTC"] * price
                profit = sell_value - (portfolio["BTC"] * buy_price)

                balance += sell_value

                print("✅ VENTA EJECUTADA")
                print("   BTC vendido:", portfolio["BTC"])
                print("   Profit:", profit)

                portfolio["BTC"] = 0
                buy_price = None

        # =========================
        # 🧠 HOLD
        # =========================
        elif action == "HOLD":
            print("⏸ HOLD - No acción")

        else:
            print("❌ RESPUESTA INVALIDA DE IA")

        # =========================
        # 🛑 STOP LOSS / TAKE PROFIT
        # =========================
        if has_position and buy_price:
            change = (price - buy_price) / buy_price

            print("📉 Cambio desde compra:", round(change * 100, 2), "%")

            if change <= -0.01:
                print("🛑 STOP LOSS ACTIVADO")

                balance += portfolio["BTC"] * price
                portfolio["BTC"] = 0
                buy_price = None

            elif change >= 0.01:
                print("💰 TAKE PROFIT ACTIVADO")

                balance += portfolio["BTC"] * price
                portfolio["BTC"] = 0
                buy_price = None

        print("🔁 Esperando siguiente ciclo...\n")

        time.sleep(INTERVALO)

    except Exception as e:
        print("❌ ERROR GENERAL:", e)
        time.sleep(10)

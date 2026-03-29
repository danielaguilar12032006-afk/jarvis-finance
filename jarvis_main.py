import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 JARVIS SIMULADOR PRO")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTERVALO = 60

balance = 1000
portfolio = {
    "BTC": 0
}

buy_price = None

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data["price"])

def decide_action(price):
    prompt = f"""
    You are a crypto trading bot.

    Price: {price}
    Balance: {balance}
    Portfolio: {portfolio}

    Rules:
    - If price going up → BUY
    - If price weak → SELL
    - Otherwise HOLD

    Answer ONLY: BUY, SELL or HOLD
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text.strip().upper()


while True:
    try:
        price = get_price()

        print("\n⏱", datetime.now())
        print("💰 Balance:", balance)
        print("📦 Portfolio:", portfolio)
        print("📊 Price:", price)

        action = decide_action(price)
        print("🧠 Decision:", action)

        # =========================
        # 🔒 REGLA: SOLO UNA POSICIÓN
        # =========================
        has_position = portfolio["BTC"] > 0

        # =========================
        # 🟢 BUY
        # =========================
        if action == "BUY" and not has_position and balance > 100:
            amount = 100 / price
            portfolio["BTC"] += amount
            balance -= 100
            buy_price = price

            print("🟢 Compra BTC:", amount)

        # =========================
        # 🔴 SELL
        # =========================
        elif action == "SELL" and has_position:
            balance += portfolio["BTC"] * price
            print("🔴 Vendió BTC:", portfolio["BTC"])
            portfolio["BTC"] = 0
            buy_price = None

        # =========================
        # 🧠 STOP LOSS / TAKE PROFIT
        # =========================
        if has_position and buy_price:
            change = (price - buy_price) / buy_price

            if change <= -0.01:
                print("🛑 STOP LOSS")
                balance += portfolio["BTC"] * price
                portfolio["BTC"] = 0
                buy_price = None

            elif change >= 0.01:
                print("💰 TAKE PROFIT")
                balance += portfolio["BTC"] * price
                portfolio["BTC"] = 0
                buy_price = None

        print("--- Esperando siguiente revisión ---")

        time.sleep(INTERVALO)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)

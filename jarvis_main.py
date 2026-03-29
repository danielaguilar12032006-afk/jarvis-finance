import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 JARVIS SIMULADOR PROTEGIDO")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTERVALO = 60

# 💰 dinero inicial
balance = 1000

# 📦 portafolio
portfolio = {
    "BTC": 0,
    "ETH": 0
}

# 🧠 precio de compra
buy_price = 0

SYMBOLS = {
    "BTC": "XXBTZUSD",
    "ETH": "XETHZUSD"
}

# 📊 precios
def get_prices():
    try:
        pairs = ",".join(SYMBOLS.values())
        url = f"https://api.kraken.com/0/public/Ticker?pair={pairs}"
        response = requests.get(url, timeout=10).json()

        prices = {}
        for key, pair in SYMBOLS.items():
            for kraken_key in response["result"]:
                if pair in kraken_key:
                    prices[key] = float(response["result"][kraken_key]["c"][0])

        return prices

    except Exception as e:
        print("Error precios:", e)
        return {}

# 🤖 decisión
def decide_action(prices):
    prompt = f"""
    You are a professional crypto trader.

    Rules:
    - Buy only in strong uptrend
    - Sell in downtrend
    - Avoid overtrading
    - Be conservative

    Prices: {prices}
    Balance: {balance}
    Portfolio: {portfolio}

    Answer ONLY: BUY, SELL or HOLD
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip().upper()

    except Exception as e:
        print("Error IA:", e)
        return "HOLD"

# 🔁 loop
def run():
    global balance, buy_price

    print("===== JARVIS PRO =====")

    while True:
        now = datetime.now()
        print("\n🕒", now)

        print("💰 Balance:", round(balance, 2))
        print("📦 Portfolio:", portfolio)

        prices = get_prices()

        if prices:
            btc_price = prices["BTC"]
            print("📊 Prices:", prices)

            # 🔴 STOP LOSS / TAKE PROFIT
            if portfolio["BTC"] > 0:

                # Stop loss -2%
                if btc_price < buy_price * 0.99:
                    balance += portfolio["BTC"] * btc_price
                    portfolio["BTC"] = 0
                    print("🔴 STOP LOSS ACTIVADO")
                    continue

                # Take profit +3%
                if btc_price > buy_price * 1.01:
                    balance += portfolio["BTC"] * btc_price
                    portfolio["BTC"] = 0
                    print("🟢 TAKE PROFIT")
                    continue

            decision = decide_action(prices)
            print("🤖 Decision:", decision)

            # 🟢 COMPRA (solo si NO tienes BTC)
            if decision == "BUY" and balance >= 100 and portfolio["BTC"] == 0:
                amount = 100 / btc_price

                portfolio["BTC"] += amount
                balance -= 100
                buy_price = btc_price

                print("🟢 Compró BTC:", round(amount, 6))

            # 🔴 VENTA
            elif decision == "SELL" and portfolio["BTC"] > 0:
                balance += portfolio["BTC"] * btc_price
                portfolio["BTC"] = 0

                print("🔴 Vendió BTC")

            else:
                print("⏸️ HOLD")

        else:
            print("⚠️ Error obteniendo precios")

        print("\n--- Esperando siguiente revisión ---")
        time.sleep(INTERVALO)

# ▶️ start
if __name__ == "__main__":
    run()

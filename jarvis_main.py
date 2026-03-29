import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 JARVIS SIMULADOR ACTIVO")

# 🔐 API KEY desde Railway
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ⏱️ intervalo (segundos)
INTERVALO = 60

# 💰 dinero inicial
balance = 1000

# 📦 portafolio
portfolio = {
    "BTC": 0,
    "ETH": 0
}

# 📊 criptos
SYMBOLS = {
    "BTC": "XXBTZUSD",
    "ETH": "XETHZUSD"
}

# 📈 obtener precios
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
        print("Error obteniendo precios:", e)
        return {}

# 🤖 decisión con IA
def decide_action(prices):
    prompt = f"""
    You are a crypto trading bot.

    Prices: {prices}
    Balance: {balance}
    Portfolio: {portfolio}

    Decide: BUY, SELL or HOLD.
    Answer ONLY one word.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        decision = response.choices[0].message.content.strip().upper()
        return decision

    except Exception as e:
        print("Error IA:", e)
        return "HOLD"

# 🔁 loop principal
def run():
    global balance

    print("===== JARVIS SIMULADOR =====")

    while True:
        now = datetime.now()
        print("\n🕒", now)

        print("💰 Balance:", round(balance, 2))
        print("📦 Portfolio:", portfolio)

        prices = get_prices()

        if prices:
            print("📊 Prices:", prices)

            decision = decide_action(prices)
            print("🤖 Decision:", decision)

            # 🟢 COMPRAR
            if decision == "BUY" and balance >= 100:
                btc_price = prices["BTC"]
                amount = 100 / btc_price

                portfolio["BTC"] += amount
                balance -= 100

                print("🟢 Compró BTC:", round(amount, 6))

            # 🔴 VENDER
            elif decision == "SELL" and portfolio["BTC"] > 0:
                btc_price = prices["BTC"]

                balance += portfolio["BTC"] * btc_price
                print("🔴 Vendió BTC")

                portfolio["BTC"] = 0

            else:
                print("⏸️ HOLD")

        else:
            print("⚠️ No se obtuvieron precios")

        print("\n--- Esperando siguiente revisión ---")
        time.sleep(INTERVALO)

# ▶️ start
if __name__ == "__main__":
    run()

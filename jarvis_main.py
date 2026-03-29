import os
import time
import requests
from datetime import datetime

print("🚀 JARVIS SIMULADOR ACTIVO")

INTERVALO = 60

SYMBOLS = {
    "BTC": "XXBTZUSD",
    "ETH": "XETHZUSD",
    "SOL": "SOLUSD",
    "ADA": "ADAUSD",
    "DOGE": "XDGUSD"
}

# 💰 SIMULACIÓN
BALANCE = 1000
PORTFOLIO = {}
LAST_PRICES = {}

# 📊 OBTENER PRECIOS
def get_prices():
    try:
        pairs = ",".join(SYMBOLS.values())
        url = f"https://api.kraken.com/0/public/Ticker?pair={pairs}"
        response = requests.get(url, timeout=10).json()

        prices = {}

        for key, pair in SYMBOLS.items():
            for kraken_key in response["result"]:
                if pair in kraken_key:
                    price = float(response["result"][kraken_key]["c"][0])
                    prices[key] = price

        return prices

    except Exception as e:
        print("Error:", e)
        return {}

# 🧠 SIMULADOR
def simulate_trading(prices):
    global BALANCE, PORTFOLIO, LAST_PRICES

    for coin, price in prices.items():

        if coin not in LAST_PRICES:
            LAST_PRICES[coin] = price
            continue

        change = (price - LAST_PRICES[coin]) / LAST_PRICES[coin]

        # 📉 BAJÓ → COMPRAR
        if change < -0.01 and BALANCE > 50:
            amount = BALANCE * 0.1
            PORTFOLIO[coin] = PORTFOLIO.get(coin, 0) + amount / price
            BALANCE -= amount
            print(f"🟢 BUY {coin} ${amount}")

        # 📈 SUBIÓ → VENDER
        elif change > 0.01 and coin in PORTFOLIO:
            amount = PORTFOLIO[coin] * price
            BALANCE += amount
            print(f"🔴 SELL {coin} ${amount}")
            PORTFOLIO[coin] = 0

        LAST_PRICES[coin] = price

    print(f"💰 Balance: ${BALANCE:.2f}")
    print(f"📦 Portfolio: {PORTFOLIO}")

# 🔁 LOOP PRINCIPAL
def run():
    print("===== JARVIS TRADING SIMULATION =====")

    while True:
        now = datetime.now()
        print(f"\n🕒 {now}")

        prices = get_prices()

        if prices:
            for crypto, price in prices.items():
                print(f"{crypto} → ${price}")

            # 🔥 AQUÍ ESTÁ LO IMPORTANTE
            simulate_trading(prices)

        else:
            print("⚠️ Error obteniendo precios")

        print("\n--- Esperando siguiente revisión ---")
        time.sleep(INTERVALO)

# ▶️ START
if __name__ == "__main__":
    run()

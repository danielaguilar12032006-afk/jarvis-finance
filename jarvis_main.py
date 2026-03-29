import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 NUEVO JARVIS ACTIVO")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ⚙️ CONFIG
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
PORTFOLIO = {k: 0 for k in SYMBOLS}
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
        print("Error obteniendo precios:", e)
        return {}

# 🤖 SIMULACIÓN DE TRADING
def simulate_trading(prices):
    global BALANCE, PORTFOLIO, LAST_PRICES

    for crypto, price in prices.items():

        if crypto not in LAST_PRICES:
            LAST_PRICES[crypto] = price
            continue

        old_price = LAST_PRICES[crypto]
        change = (price - old_price) / old_price * 100

        # 🟢 COMPRAR
        if change < -1 and BALANCE > 50:
            amount = 50 / price
            PORTFOLIO[crypto] += amount
            BALANCE -= 50
            print(f"🟢 BUY {crypto} - $50")

        # 🔴 VENDER
        elif change > 1 and PORTFOLIO[crypto] > 0:
            amount = PORTFOLIO[crypto]
            value = amount * price
            BALANCE += value
            PORTFOLIO[crypto] = 0
            print(f"🔴 SELL {crypto} - ${value:.2f}")

        LAST_PRICES[crypto] = price

# 🔁 LOOP PRINCIPAL
def run():
    print("===== JARVIS FINANCIERO =====")
    print("🚀 Iniciando monitoreo...\n")

    while True:
        now = datetime.now()
        print(f"\n🕒 {now}")

        prices = get_prices()

        if prices:
            for crypto, price in prices.items():
                print(f"{crypto} → ${price}")

            simulate_trading(prices)

            print(f"\n💰 Balance: ${BALANCE:.2f}")
            print(f"📦 Portfolio: {PORTFOLIO}")

        else:
            print("⚠️ No se obtuvieron precios")

        print("\n--- Esperando siguiente revisión ---")
        time.sleep(INTERVALO)

# ▶️ START
if __name__ == "__main__":
    run()

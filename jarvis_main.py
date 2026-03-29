import os
import time
import requests
from datetime import datetime
from openai import OpenAI

print("🚀 NUEVO JARVIS ACTIVO")

# 🔐 API KEY (desde variables de entorno)
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

# 📊 OBTENER PRECIOS (KRAKEN)
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
        else:
            print("⚠️ No se obtuvieron precios")

        print("\n--- Esperando siguiente revisión ---")
        time.sleep(INTERVALO)

# ▶️ START
if __name__ == "__main__":
    run()

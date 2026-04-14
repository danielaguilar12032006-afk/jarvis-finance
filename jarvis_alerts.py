import time
import requests
from datetime import datetime
import os

# =========================
# CONFIG
# =========================
TELEGRAM_TOKEN = "8553012917:AAG-Wg0emSLS4lwDstgZuVwatGOEM5hkl-0"
CHAT_ID = "8781403850"

SYMBOLS = {
    "bitcoin": "XXBTZUSD",
    "ethereum": "XETHZUSD",
    "solana": "SOLUSD"
}

# =========================
# TELEGRAM
# =========================
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=data)
    except Exception as e:
        print("Error Telegram:", e)

# =========================
# KRAKEN PRICES
# =========================
def get_prices():
    try:
        pairs = ",".join(SYMBOLS.values())
        url = f"https://api.kraken.com/0/public/Ticker?pair={pairs}"

        response = requests.get(url, timeout=10)
        data = response.json()

        if data["error"]:
            print("Error Kraken:", data["error"])
            return {}

        result = data["result"]
        prices = {}

        for coin, pair in SYMBOLS.items():
            if pair in result:
                price = float(result[pair]["c"][0])
                prices[coin] = {"usd": price}

        print("Precios Kraken:", prices)
        return prices

    except Exception as e:
        print("Error Kraken:", e)
        return {}

# =========================
# LÓGICA
# =========================
last_prices = {}

def analyze_market():
    global last_prices

    prices = get_prices()

    if not prices:
        print("⚠️ No se obtuvieron precios")
        return

    for coin in SYMBOLS:

        if coin not in prices:
            continue

        current_price = prices[coin]["usd"]

        if coin in last_prices:
            old_price = last_prices[coin]

            if old_price == 0:
                continue

            change = ((current_price - old_price) / old_price) * 100

            print(f"{coin.upper()} cambio: {change:.2f}%")

            # SEÑALES
            if change >= 1:
                send_telegram(f"📈 COMPRA {coin.upper()} +{change:.2f}%")

            elif change <= -1:
                send_telegram(f"📉 VENTA {coin.upper()} {change:.2f}%")

        last_prices[coin] = current_price

# =========================
# MAIN LOOP
# =========================
def run_jarvis():
    print("JARVIS INICIADO 🚀")
    send_telegram("🚀 Jarvis activo (Kraken estable)")

    while True:
        try:
            print(f"Ciclo: {datetime.now()}")
            analyze_market()
            time.sleep(60)
        except Exception as e:
            print("Error ciclo:", e)
            time.sleep(10)

# =========================
# START
# =========================
if __name__ == "__main__":
    run_jarvis()

import time
from collections import defaultdict
from data.market import get_prices
from config.settings import SYMBOLS

# =========================
# CONFIG
# =========================
TARGET_PROFIT = 0.005  # 0.5%
MAX_POSITIONS = 3
SLEEP_TIME = 10

# =========================
# ESTADO
# =========================
positions = defaultdict(list)  # guarda compras por símbolo
avg_price = {}

# =========================
# FUNCIONES
# =========================

def calculate_avg(symbol):
    if not positions[symbol]:
        return None
    return sum(positions[symbol]) / len(positions[symbol])


def should_buy(price, symbol):
    # evita comprar si ya tienes muchas posiciones
    if len(positions[symbol]) >= MAX_POSITIONS:
        return False

    # primera compra siempre permitida
    if not positions[symbol]:
        return True

    # compra si baja un poco (mejora promedio)
    last_price = positions[symbol][-1]
    return price < last_price * 0.998


def should_sell(price, symbol):
    if not positions[symbol]:
        return False

    avg = calculate_avg(symbol)
    target = avg * (1 + TARGET_PROFIT)

    return price >= target


def buy(symbol, price):
    positions[symbol].append(price)
    avg_price[symbol] = calculate_avg(symbol)

    print(f"{symbol} BUY at {price} | avg: {avg_price[symbol]} | positions: {len(positions[symbol])}")


def sell(symbol, price):
    avg = avg_price[symbol]

    print(f"{symbol} SELL at {price} | avg: {avg} | profit: {price - avg}")

    positions[symbol].clear()
    avg_price[symbol] = None


# =========================
# LOOP PRINCIPAL
# =========================

def run():
    print("Jarvis iniciado...\n")

    while True:
        try:
            prices = get_prices()

            for symbol in SYMBOLS:
                price = prices[symbol]

                print(f"{symbol} Price: {price}")

                # DECISIONES
                if should_buy(price, symbol):
                    buy(symbol, price)

                elif should_sell(price, symbol):
                    sell(symbol, price)

                else:
                    print(f"{symbol} HOLD")

            print("-" * 40)
            time.sleep(SLEEP_TIME)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run()

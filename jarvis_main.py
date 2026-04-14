import time
from data.market import get_price
from config.settings import (
    SYMBOL,
    BUY_THRESHOLD,
    PROFIT_TARGET,
    STOP_LOSS,
    FEE,
    SLEEP_TIME
)

position = []  # guarda precios de compra


def average_price():
    if not position:
        return None
    return sum(position) / len(position)


def should_buy(price):
    if not position:
        return True

    last_buy = position[-1]
    return price < last_buy * (1 - BUY_THRESHOLD)


def should_sell(price):
    if not position:
        return False

    avg = average_price()
    target = avg * (1 + PROFIT_TARGET + FEE)

    return price >= target


def buy(price):
    position.append(price)
    avg = average_price()

    print(f"BUY {SYMBOL} at {price} | avg: {avg} | buys: {len(position)}")


def sell(price):
    avg = average_price()
    profit = price - avg

    print(f"SELL {SYMBOL} at {price} | avg: {avg} | profit: {profit}")

    position.clear()


def run():
    print("Jarvis activo...\n")

    while True:
        try:
            price = get_price()

            print(f"{SYMBOL} price: {price}")

            if should_buy(price):
                buy(price)

            elif should_sell(price):
                sell(price)

            else:
                print("HOLD")

            print("-" * 30)
            time.sleep(SLEEP_TIME)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run()
def buy(symbol, price):
    positions[symbol].append(price)
    avg_price[symbol] = calculate_avg(symbol)

    print(f"{symbol} BUY at {price} | avg: {avg_price[symbol]} | positions: {len(positions[symbol])}")


def sell(symbol, price):
    avg = avg_price[symbol]

    print(f"{symbol} SELL at {price} | avg: {avg} | profit: {price - avg}")

    positions[symbol].clear()
    avg_price[symbol] = None


def run():
    print("Jarvis activo...\n")

    while True:
        try:
            prices = get_prices()

            for symbol in SYMBOLS:
                price = prices.get(symbol)

                if not price:
                    continue

                print(f"{symbol} price: {price}")

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

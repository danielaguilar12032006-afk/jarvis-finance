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

last_price = None
in_position = False
buy_price = 0


def run():
    global last_price, in_position, buy_price

    print("Jarvis activo...\n")

    while True:
        try:
            price = get_price()

            # PRINT ARREGLADO (solo esto cambiamos)
            print(f"{SYMBOL} price: {price}")

            # SI NO TIENE POSICIÓN → BUSCA COMPRA
            if not in_position and last_price:
                change = (price - last_price) / last_price

                if change <= -BUY_THRESHOLD:
                    in_position = True
                    buy_price = price

                    print(f"BUY {SYMBOL} at {price}")

            # SI YA COMPRÓ → BUSCA VENTA
            elif in_position:
                change = (price - buy_price) / buy_price

                # PROFIT
                if change >= PROFIT_TARGET + FEE:
                    print(f"SELL {SYMBOL} at {price} | profit: {price - buy_price}")
                    in_position = False

                # STOP LOSS
                elif change <= -STOP_LOSS:
                    print(f"STOP LOSS {SYMBOL} at {price}")
                    in_position = False

                else:
                    print("HOLD")

            last_price = price
            print("-" * 30)

            time.sleep(SLEEP_TIME)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run()

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

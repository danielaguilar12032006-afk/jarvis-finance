import time
from data.market import get_prices
from config.settings import (
    SYMBOLS,
    BUY_THRESHOLD,
    PROFIT_TARGET,
    STOP_LOSS,
    FEE,
    SLEEP_TIME
)

state = {}

for coin in SYMBOLS:
    state[coin] = {
        "last_price": None,
        "in_position": False,
        "buy_price": 0
    }


def run():
    print("Jarvis multi-coin activo...\n")

    while True:
        try:
            prices = get_prices()

            for coin in SYMBOLS:
                price = prices.get(coin)
                if not price:
                    continue

                s = state[coin]

                print(f"{coin} price: {price}")

                # BUY
                if not s["in_position"] and s["last_price"]:
                    change = (price - s["last_price"]) / s["last_price"]

                    if change <= -BUY_THRESHOLD:
                        s["in_position"] = True
                        s["buy_price"] = price

                        print(f"BUY {coin} at {price}")

                # SELL
                elif s["in_position"]:
                    change = (price - s["buy_price"]) / s["buy_price"]

                    if change >= PROFIT_TARGET + FEE:
                        print(f"SELL {coin} at {price} | profit: {price - s['buy_price']}")
                        s["in_position"] = False

                    elif change <= -STOP_LOSS:
                        print(f"STOP LOSS {coin} at {price}")
                        s["in_position"] = False

                    else:
                        print(f"{coin} HOLD")

                s["last_price"] = price
                print("-" * 30)

            time.sleep(SLEEP_TIME)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    run()                    print(f"BUY {SYMBOL} at {price}")

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

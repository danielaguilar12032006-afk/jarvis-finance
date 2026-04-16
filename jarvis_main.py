import time
import os
import ccxt
from data.market import get_prices
from config.settings import (
    SYMBOLS,
    BUY_THRESHOLD,
    PROFIT_TARGET,
    STOP_LOSS,
    FEE,
    SLEEP_TIME
)

# 🔒 CONFIG REAL (seguro)
TRADE_AMOUNT_USD = 2

exchange = ccxt.kraken({
    "apiKey": os.getenv("API_KEY"),
    "secret": os.getenv("API_SECRET")
})

state = {}

for coin in SYMBOLS:
    state[coin] = {
        "last_price": None,
        "in_position": False,
        "buy_price": 0
    }


def run():
    print("Jarvis REAL activo...\n")

    while True:
        try:
            prices = get_prices()

            for coin, symbol in SYMBOLS.items():
                price = prices.get(coin)
                if not price:
                    continue

                s = state[coin]

                print("{} price: {}".format(coin, price))

                # ================= BUY =================
                if not s["in_position"] and s["last_price"] is not None:
                    change = (price - s["last_price"]) / s["last_price"]

                    if change <= -BUY_THRESHOLD:
                        amount = TRADE_AMOUNT_USD / price

                        exchange.create_market_buy_order(symbol, amount)

                        s["in_position"] = True
                        s["buy_price"] = price

                        print("BUY {} at {}".format(coin, price))

                # ================= SELL =================
                elif s["in_position"]:
                    change = (price - s["buy_price"]) / s["buy_price"]

                    if change >= (PROFIT_TARGET + FEE):
                        amount = TRADE_AMOUNT_USD / s["buy_price"]

                        exchange.create_market_sell_order(symbol, amount)

                        print("SELL {} at {} | profit: {}".format(
                            coin,
                            price,
                            price - s["buy_price"]
                        ))

                        s["in_position"] = False

                    elif change <= -STOP_LOSS:
                        amount = TRADE_AMOUNT_USD / s["buy_price"]

                        exchange.create_market_sell_order(symbol, amount)

                        print("STOP LOSS {} at {}".format(coin, price))

                        s["in_position"] = False

                    else:
                        print("{} HOLD".format(coin))

                # actualizar último precio
                s["last_price"] = price

                print("-" * 30)

            time.sleep(SLEEP_TIME)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    run()
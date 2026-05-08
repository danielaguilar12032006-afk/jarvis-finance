import ccxt
import time
import os

# ==============================
# API
# ==============================

exchange = ccxt.kraken({
    'apiKey': os.getenv("KRAKEN_API_KEY"),
    'secret': os.getenv("KRAKEN_SECRET"),
})

# ==============================
# CONFIG
# ==============================

SYMBOLS = [
    "BTC/CAD",
    "ETH/CAD",
    "SOL/CAD",
    "XRP/CAD"
]

TRADE_MIN = 6
FEE = 0.004
SLEEP = 15

STRATEGY_SPLIT = {
    "DCA": 0.35,
    "TREND": 0.50,
    "MEAN": 0.15
}

base_prices = {}
last_dca = {}

print("Jarvis FINANCE iniciado...")

# ==============================
# FUNCIONES
# ==============================

def get_price(symbol):
    return exchange.fetch_ticker(symbol)['last']


def get_balance():
    balance = exchange.fetch_balance()
    return balance['CAD']['free']


def buy(symbol, cad_amount):
    try:
        price = get_price(symbol)

        amount = (cad_amount / price) * (1 - FEE)

        exchange.create_market_buy_order(symbol, amount)

        print(f"🟢 BUY {symbol} | {cad_amount:.2f} CAD")

    except Exception as e:
        print("BUY ERROR:", e)


def sell(symbol):
    try:
        balance = exchange.fetch_balance()

        coin = symbol.split('/')[0]

        amount = balance[coin]['free']

        if amount <= 0:
            return

        exchange.create_market_sell_order(symbol, amount)

        print(f"🔴 SELL {symbol}")

    except Exception as e:
        print("SELL ERROR:", e)


# ==============================
# ESTRATEGIAS
# ==============================

def dca(symbol):
    now = time.time()

    if symbol not in last_dca:
        last_dca[symbol] = 0

    # cada 6 horas
    if now - last_dca[symbol] > 21600:

        cad_balance = get_balance()

        amount = cad_balance * STRATEGY_SPLIT["DCA"]

        if amount >= TRADE_MIN:
            buy(symbol, min(amount, 15))

        last_dca[symbol] = now


def trend(symbol, price):
    if symbol not in base_prices:
        base_prices[symbol] = price
        return

    change = (price - base_prices[symbol]) / base_prices[symbol]

    cad_balance = get_balance()

    if change > 0.01:

        amount = cad_balance * STRATEGY_SPLIT["TREND"]

        if amount >= TRADE_MIN:
            buy(symbol, min(amount, 20))

    elif change < -0.007:
        sell(symbol)

    base_prices[symbol] = price


def mean(symbol, price):
    if symbol not in base_prices:
        base_prices[symbol] = price
        return

    change = (price - base_prices[symbol]) / base_prices[symbol]

    cad_balance = get_balance()

    if change < -0.005:

        amount = cad_balance * STRATEGY_SPLIT["MEAN"]

        if amount >= TRADE_MIN:
            buy(symbol, min(amount, 10))

    elif change > 0.01:
        sell(symbol)

    base_prices[symbol] = price


# ==============================
# LOOP
# ==============================

while True:
    try:
        cad_balance = get_balance()

        print(f"\n💵 CAD Disponible: {cad_balance:.2f}")

        for symbol in SYMBOLS:

            price = get_price(symbol)

            dca(symbol)
            trend(symbol, price)
            mean(symbol, price)

            print(f"{symbol} | {price:.2f}")

        print("------ ciclo terminado ------\n")

        time.sleep(SLEEP)

    except Exception as e:
        print("MAIN ERROR:", e)
        time.sleep(5)

import time
import ccxt

from config.settings import (
    SYMBOLS,
    BUY_THRESHOLD,
    PROFIT_TARGET,
    STOP_LOSS,
    SLEEP_TIME,
    TRADE_AMOUNT
)

from jarvis_alerts import log_trade

# 🔐 CONFIGURACIÓN CORREGIDA
exchange = ccxt.kraken({
    'apiKey': 'TU_API_KEY',
    'secret': 'TU_API_SECRET',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot'
    }
})

print("Jarvis corriendo...")

last_prices = {}
positions = {}

while True:
    try:
        # 🔍 TEST DE CONEXIÓN (CLAVE)
        balance = exchange.fetch_balance()

        for coin, symbol in SYMBOLS.items():
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']

            print(f"{coin} price: {price}")

            if coin not in last_prices:
                last_prices[coin] = price
                continue

            change = (price - last_prices[coin]) / last_prices[coin]

            # 🟢 BUY
            if coin not in positions and change <= -BUY_THRESHOLD:
                amount = TRADE_AMOUNT / price

                try:
                    exchange.create_market_buy_order(symbol, amount)

                    positions[coin] = price
                    msg = f"🟢 BUY {coin} at {price}"
                    print(msg)
                    log_trade(msg)

                except Exception as e:
                    print(f"Error BUY {coin}: {e}")

            # 🔴 SELL / STOP
            if coin in positions:
                entry_price = positions[coin]
                profit = (price - entry_price) / entry_price
                amount = TRADE_AMOUNT / entry_price

                # TAKE PROFIT
                if profit >= PROFIT_TARGET:
                    try:
                        exchange.create_market_sell_order(symbol, amount)

                        msg = f"🔴 SELL {coin} at {price} | profit: {profit:.4f}"
                        print(msg)
                        log_trade(msg)

                        del positions[coin]

                    except Exception as e:
                        print(f"Error SELL {coin}: {e}")

                # STOP LOSS
                elif profit <= -STOP_LOSS:
                    try:
                        exchange.create_market_sell_order(symbol, amount)

                        msg = f"⚠️ STOP LOSS {coin} at {price} | loss: {profit:.4f}"
                        print(msg)
                        log_trade(msg)

                        del positions[coin]

                    except Exception as e:
                        print(f"Error STOP {coin}: {e}")

            last_prices[coin] = price

        print("----- ciclo terminado -----")
        time.sleep(SLEEP_TIME)

    except Exception as e:
        print(f"Error general: {e}")
        time.sleep(10)

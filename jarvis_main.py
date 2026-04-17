import ccxt
import os
import time

print("Jarvis corriendo...")

# 🔑 Obtener keys desde Railway
api_key = os.getenv("TU_API_KEY").strip()
api_secret = os.getenv("TU_API_SECRET").strip()

# 🔥 FIX IMPORTANTE (quita errores de padding)
api_secret = api_secret.replace(" ", "").replace("\n", "")

# 🔗 Conexión a Kraken
exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

while True:
    try:
        # 📊 Obtener precios
        btc = exchange.fetch_ticker('BTC/USD')['last']
        eth = exchange.fetch_ticker('ETH/USD')['last']
        sol = exchange.fetch_ticker('SOL/USD')['last']

        print(f"BTC price: {btc}")
        print(f"ETH price: {eth}")
        print(f"SOL price: {sol}")

        print("----- ciclo terminado -----")

    except Exception as e:
        print("Error general:", str(e))

    time.sleep(10)            price = ticker['last']

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

from datetime import datetime

def log_trade(message):
    with open("logs/trades.log", "a") as f:
        f.write(f"{datetime.now()} | {message}\n")

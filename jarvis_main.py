import time
from data.market import get_price
from core.strategy import check_buy_signal
from core.trader import calculate_targets
import json
import os

SLEEP_TIME = 10
STATE_FILE = "data/state.json"

# ======================
# STATE FUNCTIONS
# ======================

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "in_position": False,
        "buy_price": None,
        "target": None,
        "stop": None
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# ======================
# INIT
# ======================

state = load_state()

in_position = state["in_position"]
buy_price = state["buy_price"]
target = state["target"]
stop = state["stop"]

last_prices = []

# ======================
# MAIN LOOP
# ======================

while True:
    try:
        price = get_price()
        print(f"Price: {price}")

        last_prices.append(price)
        if len(last_prices) > 50:
            last_prices.pop(0)

        # ======================
        # BUY LOGIC
        # ======================
        if not in_position:
            if check_buy_signal(last_prices):
                print(f"BUY at {price}")

                buy_price = price
                target, stop = calculate_targets(price)

                in_position = True

                # SAVE STATE
                state = {
                    "in_position": True,
                    "buy_price": buy_price,
                    "target": target,
                    "stop": stop
                }
                save_state(state)

        # ======================
        # SELL LOGIC
        # ======================
        else:
            print(f"Target: {target}")
            print(f"Stop: {stop}")

            if price >= target:
                print(f"SELL at {price} (target reached)")
                in_position = False

            elif price <= stop:
                print(f"SELL at {price} (stop loss)")
                in_position = False

            if not in_position:
                # RESET STATE
                state = {
                    "in_position": False,
                    "buy_price": None,
                    "target": None,
                    "stop": None
                }
                save_state(state)

        time.sleep(SLEEP_TIME)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(SLEEP_TIME)

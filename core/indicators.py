def calculate_ma(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period
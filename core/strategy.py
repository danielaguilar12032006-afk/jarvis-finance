def check_buy_signal(prices):
    if len(prices) < 10:
        return False

    # lógica simple de subida continua
    if prices[-1] > prices[-2] > prices[-3]:
        return True

    return False

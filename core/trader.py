def calculate_targets(price):
    target = price * 1.007  # 0.7% ganancia
    stop = price * 0.97     # 3% pérdida
    return target, stop

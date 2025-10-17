class Broker:
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float):
        side = side.lower()
        if side not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")

        if qty <= 0:
            raise ValueError("qty must be positive")

        if side == "buy":
            cost = qty * price
            if cost > self.cash:
                raise ValueError("Insufficient cash for buy order.")
            self.cash -= cost
            self.position += qty

        else:  # sell
            if qty > self.position:
                raise ValueError("Insufficient position for sell order.")
            self.cash += qty * price
            self.position -= qty
class Broker:
    """
    Deterministic broker: executes market orders,
    tracks cash and position (no slippage or fees).
    """
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float):
        side = side.lower()
        if side == "buy":
            cost = qty*price
            if cost > self.cash:
                raise ValueError("Insufficient funds")
            self.cash -= cost
            self.postion += qty

        elif side == "sell":
            if qty > self.position:
                raise ValueError("Insufficient position")
            self.cash += qty*price
            self.position -= qty

        else:
            raise ValueError("Side must be 'buy' or 'sell'")
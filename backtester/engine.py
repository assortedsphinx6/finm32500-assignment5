import pandas as pd

class Backtester:
    """
    End-of-day backtester: use signal(t−1), trade at close(t),
    track cash, position, and equity.
    """
    def __init__(self, strategy, broker):
        self.strategy = strategy
        self.broker = broker

    def run(self, prices: pd.Series):
        if prices.empty:
            return pd.DataFrame(columns=["cash", "position", "equity"])

        signals = self.strategy.signals(prices)

        for t in range(1, len(prices)):
            prev_signal = signals.iloc[t - 1]
            price = prices.iloc[t]

            # Buy if +1, sell if −1, flat if 0
            if prev_signal == 1 and self.broker.cash >= price:
                self.broker.market_order("buy", 1, price)
            elif prev_signal == -1 and self.broker.position > 0:
                self.broker.market_order("sell", self.broker.position, price)

        equity = self.broker.cash + self.broker.position * prices.iloc[-1]
        return pd.DataFrame(
            {
                "cash": [self.broker.cash],
                "position": [self.broker.position],
                "equity": [equity],
            }
        )
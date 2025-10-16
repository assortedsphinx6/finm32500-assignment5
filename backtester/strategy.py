import pandas as pd
import numpy as np


class VolatilityBreakoutStrategy:
    """
    Generates {-1, 0, +1} trading signals:
    +1 when current return > rolling x-day std of returns
    -1 when current return < -rolling x-day std of returns
     0 otherwise.
    """

    
    def __init__(self, window: int = 20):
        self.window = window
    
    def signals(self, prices: pd.Series) -> pd.Series:
        # integrity
        if prices.empty or len(prices) < 2:
            return pd.Series(dtype = int)

        # daily returns
        # the first day would have 0 instead of NaN since it does not have a prev day
        returns = prices.pct_change().fillna(0)

        # rolling x-day standard deviation of returns
        rolling_std = returns.rolling(window=self.window, min_periods=1).std().fillna(0)

        # generate signals
        signals = np.where(
            returns > rolling_std, 1,
            np.where(returns < -rolling_std, -1, 0)
        )

        return pd.Series(signals, index=prices.index)

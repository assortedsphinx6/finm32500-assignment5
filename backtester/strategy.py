import pandas as pd
import numpy as np

class VolatilityBreakoutStrategy:
    def __init__(self, window: int = 20):
        self.window = window

    def signals(self, prices: pd.Series) -> pd.Series:
        if prices.empty or len(prices) < 2:
            return pd.Series(dtype=int)

        returns = prices.pct_change().fillna(0)
        rolling_std = returns.rolling(window=self.window, min_periods=1).std().fillna(0)

        # {-1,0,+1} per handout
        sig = np.where(returns >  rolling_std,  1,
              np.where(returns < -rolling_std, -1, 0))
        return pd.Series(sig, index=prices.index)
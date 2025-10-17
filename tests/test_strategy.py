import numpy as np
import pandas as pd
import pytest

from backtester.strategy import VolatilityBreakoutStrategy

def test_import_and_simple_call():
    strategy = VolatilityBreakoutStrategy(window=2)
    prices = pd.Series([100.0, 101.0, 102.0])
    #just checking if the strategy runs or errors out
    signals = strategy.signals(prices)
    #checking if the length of the two match or not
    assert len(signals) == len(prices)

def test_constant_prices():
    strategy = VolatilityBreakoutStrategy(window=3)
    prices = pd.Series([100.0,100.0,100.0,100.0,100.0])
    signals = strategy.signals(prices)
    assert (signals==0).all()

def test_for_single_price():
    strategy = VolatilityBreakoutStrategy(window=3)
    prices = pd.Series([100.0])
    signals = strategy.signals(prices)
    #check for series class
    assert isinstance(signals, pd.Series)
    #we have a check, if the len of prices < 2 or empty, we create an empty series
    assert len(signals)==0

def test_if_nan_handled():
    strategy = VolatilityBreakoutStrategy(window=3)
    prices = pd.Series([np.nan, 100.0, 101.0])
    signals = strategy.signals(prices)
    assert len(signals) == len(prices)
    #check if the first signal is handled well
    assert int(signals.iloc[0]) == 0

def test_one_window_nonzero_prices():
    strategy = VolatilityBreakoutStrategy(window=1)
    prices = pd.Series([100.0, 102.0, 100.0, 101.0])
    signals = strategy.signals(prices)
    #since window is 1, standard deviations are 0
    expected = pd.Series([0,1,-1,1])
    pd.testing.assert_series_equal(signals.astype(int), expected.astype(int))

def test_deterministic():
    strategy = VolatilityBreakoutStrategy(window=2)
    prices = pd.Series([100.0, 120.0, 60.0, 61.0])
    signals = strategy.signals(prices)
    returns = prices.pct_change().fillna(0)
    rolling_std = returns.rolling(window=2, min_periods=1).std().fillna(0)

    expected = []
    for rets, sstd in zip(returns, rolling_std):
        if rets>sstd:
            expected.append(1)
        elif rets<-sstd:
            expected.append(-1)
        else:
            expected.append(0)
    expected = pd.Series(expected, index=prices.index)

    pd.testing.assert_series_equal(signals.astype(int), expected.astype(int))


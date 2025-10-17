import pytest
import pandas as pd
from types import SimpleNamespace
from backtester.engine import Backtester


@pytest.fixture
def mock_broker():
    broker = SimpleNamespace()
    broker.cash = 100
    broker.position = 0

    def market_order(side, qty, price):
        if side == "buy":
            broker.cash -= qty * price
            broker.position += qty
        elif side == "sell":
            broker.cash += qty * price
            broker.position -= qty
        else:
            raise ValueError("Invalid order side")

    broker.market_order = market_order
    return broker


@pytest.fixture
def mock_strategy():
    class Strategy:
        def __init__(self, signals):
            self._signals = signals

        def signals(self, prices):
            return self._signals

    return Strategy


def test_empty_prices_returns_empty_df(mock_strategy, mock_broker):
    prices = pd.Series(dtype=float)
    strategy = mock_strategy(pd.Series(dtype=float))
    bt = Backtester(strategy, mock_broker)

    result = bt.run(prices)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["cash", "position", "equity"]
    assert result.empty


def test_buy_signal_increases_position(mock_strategy, mock_broker):
    prices = pd.Series([10, 12, 15])
    signals = pd.Series([1, 0, 0]) 
    strategy = mock_strategy(signals)
    bt = Backtester(strategy, mock_broker)

    result = bt.run(prices)

    assert mock_broker.position == 1
    assert mock_broker.cash == pytest.approx(100 - 12)
    expected_equity = mock_broker.cash + mock_broker.position * 15
    assert result["equity"].iloc[0] == pytest.approx(expected_equity)


def test_sell_signal_reduces_position(mock_strategy, mock_broker):
    mock_broker.position = 1
    mock_broker.cash = 50

    prices = pd.Series([10, 11, 9])
    signals = pd.Series([0, -1, 0])
    strategy = mock_strategy(signals)
    bt = Backtester(strategy, mock_broker)

    result = bt.run(prices)

    assert mock_broker.position == 0
    # Sell occurs at t=2 using signal(t-1) => price 9
    assert mock_broker.cash == pytest.approx(50 + 9)
    expected_equity = mock_broker.cash
    assert result["equity"].iloc[0] == pytest.approx(expected_equity)


def test_no_action_when_flat_signal(mock_strategy, mock_broker):
    prices = pd.Series([10, 11, 12])
    signals = pd.Series([0, 0, 0])
    strategy = mock_strategy(signals)
    bt = Backtester(strategy, mock_broker)

    result = bt.run(prices)

    assert mock_broker.position == 0
    assert mock_broker.cash == 100
    expected_equity = 100
    assert result["equity"].iloc[0] == expected_equity


def test_cannot_buy_if_not_enough_cash(mock_strategy, mock_broker):
    mock_broker.cash = 5 
    prices = pd.Series([10, 20])
    signals = pd.Series([1, 0])
    strategy = mock_strategy(signals)
    bt = Backtester(strategy, mock_broker)

    result = bt.run(prices)

    assert mock_broker.position == 0
    assert mock_broker.cash == 5
    assert result["equity"].iloc[0] == 5


def test_engine_propagates_broker_failure(monkeypatch, mock_broker, mock_strategy):
    prices = pd.Series([10, 11, 12])
    signals = pd.Series([1, 1, 1])           # ensures a buy attempt
    strategy = mock_strategy(signals)

    def boom(*args, **kwargs):
        raise ValueError("trade failed")
    monkeypatch.setattr(mock_broker, "market_order", boom)

    with pytest.raises(ValueError, match="trade failed"):
        Backtester(strategy, mock_broker).run(prices)
import pytest
from backtester.broker import Broker

def test_buy_and_sell_updates_cash_and_position():
    b = Broker(cash=100.0)
    b.market_order("buy", 2, 10.0)   # spend 20
    assert (b.position, b.cash) == (2, 80.0)
    b.market_order("sell", 1, 12.0)  # receive 12
    assert (b.position, b.cash) == (1, 92.0)

def test_rejects_invalid_side():
    b = Broker(cash=100.0)
    with pytest.raises(ValueError):
        b.market_order("hold", 1, 10.0)

def test_rejects_non_positive_qty():
    b = Broker(cash=100.0)
    with pytest.raises(ValueError):
        b.market_order("buy", 0, 10.0)
    with pytest.raises(ValueError):
        b.market_order("sell", -3, 10.0)

def test_raises_on_insufficient_cash():
    b = Broker(cash=5.0)
    with pytest.raises(ValueError):
        b.market_order("buy", 1, 10.0)

def test_raises_on_insufficient_shares():
    b = Broker(cash=100.0)
    with pytest.raises(ValueError):
        b.market_order("sell", 1, 10.0)
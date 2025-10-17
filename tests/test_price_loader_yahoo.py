# tests/test_price_loader_yahoo.py
import sys
import types
import pandas as pd
import pytest
from backtester.price_loader import PriceLoader

def test_price_loader_yahoo_happy():
    # Fake yfinance module with a download() that returns data
    fake_yf = types.SimpleNamespace(
        download=lambda symbol, start=None, end=None, progress=False, auto_adjust=False, threads=False: pd.DataFrame(
            {"Adj Close": [100.0, 101.0, 102.0]},
            index=pd.date_range("2020-01-01", periods=3, freq="D"),
        )
    )
    sys.modules["yfinance"] = fake_yf  # inject stub

    s = PriceLoader().load_prices()
    assert s.name == "AAPL"
    assert list(s.index) == list(pd.date_range("2020-01-01", periods=3, freq="D"))
    assert list(s.astype(float).values) == [100.0, 101.0, 102.0]

def test_price_loader_yahoo_empty():
    fake_yf = types.SimpleNamespace(
        download=lambda *a, **k: pd.DataFrame()
    )
    sys.modules["yfinance"] = fake_yf

    with pytest.raises(ValueError):
        PriceLoader().load_prices()

def test_price_loader_yahoo_missing_field():
    fake_yf = types.SimpleNamespace(
        download=lambda *a, **k: pd.DataFrame(
            {"Close": [100.0, 101.0, 102.0]},
            index=pd.date_range("2020-01-01", periods=3, freq="D"),
        )
    )
    sys.modules["yfinance"] = fake_yf

    with pytest.raises(ValueError):
        PriceLoader().load_prices()

def test_price_loader_raises_when_yfinance_missing(monkeypatch):
    # Ensure import inside load_prices() fails
    sys.modules.pop("yfinance", None)
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yfinance":
            raise ImportError("No module named yfinance")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="yfinance is not installed"):
        PriceLoader().load_prices()
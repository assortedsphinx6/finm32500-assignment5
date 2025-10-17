import pandas as pd
import pytest
from backtester.price_loader import PriceLoader
import builtins
import sys

def test_price_loader_yahoo_happy(monkeypatch):
    def fake_download(symbol, start=None, end=None, progress=False, auto_adjust=False, threads=False):
        idx = pd.date_range("2020-01-01", periods=3, freq="D")
        return pd.DataFrame({"Adj Close": [100.0, 101.0, 102.0]}, index=idx)

    import yfinance as yf
    monkeypatch.setattr(yf, "download", fake_download)

    s = PriceLoader().load_prices()   # loads AAPL; uses yfinance.download under the hood
    assert s.name == "AAPL"
    assert list(s.index) == list(pd.date_range("2020-01-01", periods=3, freq="D"))
    assert list(s.astype(float).values) == [100.0, 101.0, 102.0]

def test_price_loader_yahoo_empty(monkeypatch):
    import yfinance as yf
    monkeypatch.setattr(yf, "download", lambda *a, **kw: pd.DataFrame())

    with pytest.raises(ValueError):
        PriceLoader().load_prices()

def test_price_loader_raises_when_yfinance_missing(monkeypatch):
    # Ensure yfinance isn't already loaded
    sys.modules.pop("yfinance", None)

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yfinance":
            raise ImportError("No module named yfinance")
        return real_import(name, *args, **kwargs)

    # Make importing yfinance fail inside load_prices()
    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="yfinance is not installed"):
        PriceLoader().load_prices()
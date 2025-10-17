import pandas as pd

class PriceLoader:
    """
    Minimal Yahoo Finance PriceLoader.
    Always loads prices for AAPL (Apple Inc.) for demonstration / testing.
    """

    def __init__(self, price_field: str = "Adj Close"):
        self.price_field = price_field

    def load_prices(self) -> pd.Series:
        """Fetches AAPL prices from Yahoo Finance."""
        try:
            import yfinance as yf
        except Exception as e:
            raise RuntimeError(
                "yfinance is not installed. Please install it with `pip install yfinance`."
            ) from e

        df = yf.download(
            "AAPL",
            start="2020-01-01",
            end="2020-12-31",
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df.empty or self.price_field not in df.columns:
            raise ValueError("No valid AAPL data returned from Yahoo Finance.")

        s = df[self.price_field].astype(float).dropna()
        s.name = "AAPL"
        s = s[~s.index.duplicated()].sort_index()
        return s
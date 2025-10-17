import numpy as np, pandas as pd, pytest
from backtester.strategy import VolatilityBreakoutStrategy
from backtester.broker import Broker

@pytest.fixture
def prices():
    # deterministic rising series
    return pd.Series(np.linspace(100, 120, 200))

@pytest.fixture
def strategy():
    return VolatilityBreakoutStrategy()

@pytest.fixture
def broker():
    return Broker(cash=1_000)

# blocks all outbound sockets during tests
import socket, pytest
@pytest.fixture(autouse=True, scope="session")
def _no_network():
    real_socket = socket.socket
    def blocked(*args, **kwargs):
        raise RuntimeError("Network access disabled during tests")
    socket.socket = blocked
    try:
        yield
    finally:
        socket.socket = real_socket
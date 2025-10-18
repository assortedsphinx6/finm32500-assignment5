# FINM 32500 – Assignment 5: Testing & CI in Financial Engineering

![coverage](coverage.svg)

## Overview
This project implements a **minimal daily-bar backtester** to demonstrate good engineering practices in testing and continuous integration.  
The goal is not PnL generation but **unit test quality, CI coverage, and determinism**.

## Components

### PriceLoader
- Loads daily prices for a single symbol (AAPL) using Yahoo Finance.
- Deterministic and fully mocked in tests (no network access).
- Returns a clean `pandas.Series` of prices.

### Strategy
- **VolatilityBreakoutStrategy**: generates signals in {-1, 0, +1}.
- Buys when current return > rolling x-day volatility, sells when < -volatility, stays flat otherwise.
- Uses daily returns and a configurable rolling window.

### Broker
- Executes deterministic market orders with no slippage or fees.
- Tracks `cash` and `position`.
- Validates all inputs and raises on invalid side, zero/negative quantity, or insufficient cash/position.

### Backtester
- Runs an end-of-day simulation:
  - Uses **signal(t−1)**.
  - Trades at **close(t)**.
  - Tracks `cash`, `position`, and `equity` through time.
- Deterministic and reproducible for CI testing.

## Testing, Fixtures, and Mocks
- Tests written with **pytest**.
- Synthetic or mocked data only; **no live API calls**.
- Fixtures and monkeypatching isolate components and simulate errors deterministically.
- Test suite completes in < 60 seconds on GitHub Actions.

## Coverage & CI
- 100% line coverage across all modules.
- CI workflow (.github/workflows/ci.yml) runs:
  ```bash
  pip install -r requirements.txt
  coverage run -m pytest -q
  coverage report --fail-under=90
  ```
- Workflow fails if coverage < 90%.
- Coverage badge generated locally with `coverage-badge` and committed as `coverage.svg`.

## How to Run Locally
```bash
# install dependencies
pip install -r requirements.txt

# run tests
coverage run -m pytest -q

# view coverage
coverage report -m
```

## Repository Structure
```
backtester/
  broker.py
  engine.py
  price_loader.py
  strategy.py
tests/
  test_broker.py
  test_engine.py
  test_price_loader_yahoo.py
  test_strategy.py
  conftest.py
.github/workflows/ci.yml
requirements.txt
pyproject.toml
README.md
coverage.svg
```

## Results
- ✅ All tests passing on GitHub Actions.
- ✅ 100% coverage.
- ✅ Suite runtime under 60s.
- ✅ No network calls (fully mocked).

---
© University of Chicago – FINM 32500: Computing for Finance in Python (Fall 2025)

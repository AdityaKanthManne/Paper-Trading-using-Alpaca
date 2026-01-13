import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


def trading_client() -> TradingClient:
    api_key = os.environ["ALPACA_API_KEY"]
    api_secret = os.environ["ALPACA_API_SECRET"]
    return TradingClient(api_key, api_secret, paper=True)


def get_account_snapshot(tc: TradingClient):
    acct = tc.get_account()
    equity = float(acct.equity)
    cash = float(acct.cash)
    positions = {p.symbol: float(p.qty) for p in tc.get_all_positions()}
    return equity, cash, positions


def submit_market_order(tc: TradingClient, symbol: str, qty: int, side: str):
    req = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side.upper() == "BUY" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    return tc.submit_order(req)

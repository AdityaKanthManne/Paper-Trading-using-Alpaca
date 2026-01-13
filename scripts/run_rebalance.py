import os
from dotenv import load_dotenv
from src.utils.logger import log_run


from src.broker.alpaca_paper import trading_client, get_account_snapshot, submit_market_order
from src.model.weights import target_weights, validate_weights
from src.utils.prices import latest_prices
from src.rebalance.rebalance import compute_target_shares, compute_deltas, orders_from_deltas
from src.risk.checks import max_order_shares


def main():
    load_dotenv()  # loads .env locally (not committed)

    w = target_weights()
    validate_weights(w)

    tc = trading_client()
    equity, cash, current = get_account_snapshot(tc)

    symbols = list(w.keys())
    prices = latest_prices(symbols)

    target = compute_target_shares(equity=equity, weights=w, prices=prices)
    deltas = compute_deltas(current=current, target=target)

    print("\n=== SNAPSHOT ===")
    print(f"Equity: {equity:.2f} | Cash: {cash:.2f}")
    print("Current:", current)
    print("Prices:", prices)
    print("Target shares:", target)
    print("Deltas:", deltas)

    log_path = log_run({
        "equity": equity,
        "cash": cash,
        "weights": w,
        "prices": prices,
        "target_shares": target,
        "deltas": deltas,
    })
    print(f"\nSaved log: {log_path}")

    max_order_shares(deltas, max_shares_per_order=200)

    orders = orders_from_deltas(deltas)
    if not orders:
        print("\nNo trades needed.")
        return

    print("\n=== DRY RUN (paper) ===")
    for sym, (side, qty) in orders.items():
        print(f"{side} {qty} {sym}")

    # Paper-only safety: must explicitly enable
    if os.environ.get("TRADING_ENABLED", "FALSE").upper() != "TRUE":
        print("\nTrading disabled (TRADING_ENABLED!=TRUE). No orders were sent.")
        return

    print("\n=== SENDING PAPER ORDERS ===")
    for sym, (side, qty) in orders.items():
        resp = submit_market_order(tc, sym, qty, side)
        print(f"Submitted {side} {qty} {sym} | id={resp.id}")


if __name__ == "__main__":
    main()

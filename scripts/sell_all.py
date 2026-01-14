import os
from dotenv import load_dotenv

from src.broker.alpaca_paper import trading_client, submit_market_order


def main():
    load_dotenv()

    tc = trading_client()

    positions = tc.get_all_positions()
    if not positions:
        print("No positions to sell.")
        return

    sells = []
    for p in positions:
        sym = p.symbol
        qty = int(float(p.qty))  # whole shares only
        if qty > 0:
            sells.append((sym, qty))

    if not sells:
        print("No long positions found to sell.")
        return

    print("\n=== DRY RUN: SELL ALL POSITIONS ===")
    for sym, qty in sells:
        print(f"SELL {qty} {sym}")

    if os.environ.get("TRADING_ENABLED", "FALSE").upper() != "TRUE":
        print("\nTrading disabled (TRADING_ENABLED!=TRUE). No orders were sent.")
        return

    print("\n=== SENDING SELL ORDERS (PAPER) ===")
    for sym, qty in sells:
        resp = submit_market_order(tc, sym, qty, "SELL")
        print(f"Submitted SELL {qty} {sym} | id={resp.id}")


if __name__ == "__main__":
    main()

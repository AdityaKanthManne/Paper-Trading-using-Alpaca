from dotenv import load_dotenv
import pandas as pd

from src.broker.alpaca_paper import trading_client, get_account_snapshot
from src.utils.prices import latest_prices


def main():
    load_dotenv()

    tc = trading_client()
    equity, cash, positions = get_account_snapshot(tc)

    print("\n=== ACCOUNT ===")
    print(f"Equity: {equity:,.2f}")
    print(f"Cash:   {cash:,.2f}")

    if not positions:
        print("\nNo positions found.")
        return

    symbols = sorted(positions.keys())
    prices = latest_prices(symbols)

    rows = []
    for sym in symbols:
        qty = float(positions[sym])
        px = float(prices[sym])
        mkt_value = qty * px
        rows.append(
            {
                "Symbol": sym,
                "Shares": qty,
                "LastPrice": round(px, 4),
                "MarketValue": round(mkt_value, 2),
            }
        )

    df = pd.DataFrame(rows).sort_values("MarketValue", ascending=False)
    total_value = df["MarketValue"].sum()

    df["Weight"] = (df["MarketValue"] / total_value).round(4)

    print("\n=== PORTFOLIO POSITIONS (estimated using yfinance last close) ===")
    print(df.to_string(index=False))

    # Save a CSV snapshot
    df.to_csv("portfolio_snapshot.csv", index=False)
    print("\nSaved: portfolio_snapshot.csv")

    print(f"\nPositions Value: {total_value:,.2f}")
    print(f"Cash:           {cash:,.2f}")
    print(f"Approx Total:   {(total_value + cash):,.2f}")


if __name__ == "__main__":
    main()

from typing import Dict


def max_order_shares(delta_shares: Dict[str, int], max_shares_per_order: int = 50):
    for sym, d in delta_shares.items():
        if abs(d) > max_shares_per_order:
            raise RuntimeError(f"Order too large for {sym}: {d} shares (limit {max_shares_per_order})")

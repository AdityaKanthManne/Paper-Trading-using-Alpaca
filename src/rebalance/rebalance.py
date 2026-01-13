from math import floor
from typing import Dict, Tuple


def compute_target_shares(equity: float, weights: Dict[str, float], prices: Dict[str, float]) -> Dict[str, int]:
    targets = {}
    for sym, w in weights.items():
        dollars = equity * float(w)
        targets[sym] = floor(dollars / prices[sym])  # whole shares only
    return targets


def compute_deltas(current: Dict[str, float], target: Dict[str, int]) -> Dict[str, int]:
    deltas = {}
    for sym, tgt in target.items():
        cur = int(float(current.get(sym, 0.0)))
        deltas[sym] = int(tgt - cur)
    return deltas


def orders_from_deltas(deltas: Dict[str, int]) -> Dict[str, Tuple[str, int]]:
    orders = {}
    for sym, d in deltas.items():
        if d == 0:
            continue
        side = "BUY" if d > 0 else "SELL"
        orders[sym] = (side, abs(int(d)))
    return orders

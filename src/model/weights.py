from typing import Dict

# Only allow trades in these symbols (edit as you like)
WHITELIST = {"AAPL", "MSFT", "SPY"}


def target_weights() -> Dict[str, float]:
    # Replace with your model output
    return {
        "AAPL": 0.25,
        "MSFT": 0.25,
        "SPY": 0.50,
    }


def validate_weights(w: Dict[str, float], tol: float = 1e-6) -> None:
    if not w:
        raise ValueError("Weights dict is empty")

    # ticker safety
    bad = set(w.keys()) - WHITELIST
    if bad:
        raise ValueError(f"Symbols not in whitelist: {sorted(bad)}")

    s = sum(float(x) for x in w.values())
    if abs(s - 1.0) > tol:
        raise ValueError(f"Weights must sum to 1.0. Got {s}")

    if any(v < 0 for v in w.values()):
        raise ValueError("Weights must be non-negative")

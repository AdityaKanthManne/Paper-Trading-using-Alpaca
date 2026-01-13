import json
import os
from datetime import datetime
from typing import Any, Dict


def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)


def log_run(payload: Dict[str, Any]) -> str:
    ensure_logs_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("logs", f"rebalance_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path

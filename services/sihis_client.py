import json
import os
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parents[1]

def get_kemenkes_intelligence(mode="demo", period="14 Hari"):
    if mode == "api":
        base_url = os.getenv("SIHIS_API_BASE_URL", "").rstrip("/")
        if not base_url:
            raise RuntimeError("SIHIS_API_BASE_URL belum dikonfigurasi.")
        r = requests.get(
            f"{base_url}/api/intelligence/kemenkes",
            params={"period": period},
            timeout=20,
        )
        r.raise_for_status()
        return r.json()

    path = BASE_DIR / "data" / "demo" / "intelligence_kemenkes.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)

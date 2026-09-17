import json
import os
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
DEMO_FILE = ROOT / "data" / "demo" / "intelligence_kemenkes.json"

def get_kemenkes_intelligence(mode="demo", period="14 Hari"):
    if mode == "api":
        base = os.getenv("SIHIS_API_BASE_URL", "").strip()
        if not base:
            raise RuntimeError("SIHIS_API_BASE_URL belum dikonfigurasi.")
        r = requests.get(base.rstrip("/") + "/api/intelligence/kemenkes", timeout=15)
        r.raise_for_status()
        return r.json()
    with DEMO_FILE.open(encoding="utf-8") as f:
        payload = json.load(f)
    payload["metadata"]["period"] = period
    return payload

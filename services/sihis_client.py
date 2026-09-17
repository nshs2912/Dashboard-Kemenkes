import json
import os
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parents[1]


def get_kemenkes_intelligence(mode="api", period="14 Hari"):
    base_url = os.getenv("SIHIS_API_BASE_URL", "").rstrip("/")

    if not base_url:
        raise RuntimeError(
            "SIHIS_API_BASE_URL belum dikonfigurasi di Streamlit Secrets."
        )

    # "14 Hari" -> 14
    if isinstance(period, str):
        period_days = int(period.split()[0])
    else:
        period_days = int(period)

    response = requests.get(
        f"{base_url}/api/intelligence/kemenkes",
        params={"period": period_days},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()

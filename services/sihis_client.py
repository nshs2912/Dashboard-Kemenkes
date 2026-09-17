import requests
import streamlit as st


def get_api_base_url():
    """
    Ambil URL SI-HIS dari Streamlit Secrets.
    Environment variable tetap didukung sebagai fallback untuk local development.
    """

    # Streamlit Cloud / Streamlit
    try:
        value = st.secrets.get("SIHIS_API_BASE_URL")
        if value:
            return str(value).rstrip("/")
    except Exception:
        pass

    # Local development fallback
    import os

    value = os.getenv("SIHIS_API_BASE_URL", "")
    if value:
        return value.rstrip("/")

    raise RuntimeError(
        "SIHIS_API_BASE_URL belum ditemukan. "
        "Tambahkan ke Streamlit Secrets."
    )


def period_to_days(period):
    """
    '7 Hari'  -> 7
    '14 Hari' -> 14
    '30 Hari' -> 30
    """
    if isinstance(period, int):
        return period

    try:
        return int(str(period).split()[0])
    except (ValueError, IndexError):
        return 14


def get_kemenkes_intelligence(mode="api", period="14 Hari"):

    # Dashboard Kemenkes sekarang API-only.
    if mode != "api":
        raise RuntimeError(
            "Dashboard-Kemenkes hanya menggunakan SI-HIS Intelligence API."
        )

    base_url = get_api_base_url()
    period_days = period_to_days(period)

    endpoint = f"{base_url}/api/intelligence/kemenkes"

    try:
        response = requests.get(
            endpoint,
            params={"period": period_days},
            timeout=30,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Tidak dapat terhubung ke SI-HIS API: {exc}"
        ) from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"SI-HIS API mengembalikan HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "SI-HIS API tidak mengembalikan JSON yang valid."
        ) from exc

    if not isinstance(payload, dict):
        raise RuntimeError(
            "Format respons SI-HIS tidak sesuai: JSON harus berupa object."
        )

    return payload

import os

SIHIS_API_BASE_URL = os.getenv("SIHIS_API_BASE_URL", "").rstrip("/")
SIHIS_API_TIMEOUT = int(os.getenv("SIHIS_API_TIMEOUT", "20"))

import os

def check_api_config():
    return {
        "SIHIS_API_BASE_URL": bool(os.getenv("SIHIS_API_BASE_URL")),
        "SATUSEHAT_ENVIRONMENT": bool(os.getenv("SATUSEHAT_ENVIRONMENT")),
    }

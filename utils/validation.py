def validate_payload(payload):
    required = ["total_cases", "active_alerts"]
    return all(key in payload for key in required)

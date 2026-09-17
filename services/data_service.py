def normalize_intelligence(payload):
    payload = payload or {}
    ml = payload.get("ml", {})

    if not isinstance(ml, dict):
        ml = {}

    return {
        "area": payload.get("area", "Indonesia"),
        "period": payload.get("period", ""),
        "total_cases": payload.get("total_cases", 0),
        "cases_7d": payload.get("cases_7d", 0),
        "active_alerts": payload.get("active_alerts", 0),
        "high_risk_areas": payload.get("high_risk_areas", 0),
        "klb_signal": ml.get("klb_signal", 0),
        "top_disease": payload.get("top_disease", []),
        "early_warning": payload.get("early_warning", []),
        "province_risk": payload.get("province_risk", []),
        "forecast": payload.get("forecast", []),
        "vulnerable_population": payload.get("vulnerable_population", {}),
        "recommendations": payload.get("recommendations", []),

        # Mempertahankan provenance dari SI-HIS API
        "data_provenance": payload.get("data_provenance", {}),

        # Mempertahankan seluruh ML signals
        "ml": ml,
    }

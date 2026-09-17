from typing import TypedDict, Any

class IntelligenceResponse(TypedDict, total=False):
    area: str
    period: str
    total_cases: int
    cases_7d: int
    active_alerts: int
    high_risk_areas: int
    top_disease: list[dict[str, Any]]
    early_warning: list[dict[str, Any]]
    province_risk: list[dict[str, Any]]
    ml: dict[str, float]
    recommendations: list[str]

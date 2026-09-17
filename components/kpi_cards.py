import streamlit as st

def show_kpis(data):
    cols = st.columns(6)
    items = [
        ("Total Kasus", data.get("total_cases", 0)),
        ("Kasus 7 Hari", data.get("cases_7d", 0)),
        ("Active Alerts", data.get("active_alerts", 0)),
        ("Area Risiko Tinggi", data.get("high_risk_areas", 0)),
        ("KLB Signal", f'{float(data.get("klb_signal",0))*100:.0f}%'),
        ("Periode", data.get("period", "-")),
    ]
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)

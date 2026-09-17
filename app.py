import streamlit as st
import pandas as pd
import plotly.express as px
from services.sihis_client import get_kemenkes_intelligence

st.set_page_config(page_title="SI-HIS | Dashboard Kemenkes", page_icon="🏥", layout="wide")
st.title("🇮🇩 SI-HIS — Kemenkes National Health Intelligence")
st.caption("National overview • Epidemiology • Early Warning • Spatial Intelligence • Prediction • Decision Support")

with st.sidebar:
    st.header("Filter Nasional")
    period = st.selectbox("Periode", ["7 Hari", "14 Hari", "30 Hari"], index=1)
    st.selectbox("Provinsi", ["Semua Provinsi"])
    st.divider()
    st.info("Mode: DEMO / simulated intelligence. Adapter API SI-HIS tersedia untuk tahap integrasi.")

payload = get_kemenkes_intelligence(mode="demo", period=period)
s = payload["summary"]
prov = pd.DataFrame(payload["province_metrics"])
disease = pd.DataFrame(payload["disease_metrics"])
alerts = pd.DataFrame(payload["early_warning"])

st.subheader("National Overview")
a,b,c,d,e = st.columns(5)
a.metric("Total Kasus", f"{s['total_cases']:,}")
b.metric("Kasus 7 Hari", f"{s['cases_7d']:,}")
c.metric("Active Early Warning", s["active_alerts"])
d.metric("Provinsi High Risk", s["high_risk_provinces"])
e.metric("KLB Signal", f"{s['klb_signal']:.0%}")

c1,c2 = st.columns(2)
with c1:
    st.markdown("### Beban Kasus per Provinsi")
    fig = px.bar(prov.sort_values("cases").tail(15), x="cases", y="province", orientation="h")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("### Distribusi Penyakit")
    fig = px.pie(disease, names="disease", values="cases", hole=.45)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🚨 Early Warning & Spatial Intelligence")
c3,c4 = st.columns([1.15,1])
with c3:
    view = alerts[["province","signal","risk_level","reason","klb_probability"]].copy()
    view["klb_probability"] = view["klb_probability"].map(lambda x: f"{x:.0%}")
    st.dataframe(view, use_container_width=True, hide_index=True)
with c4:
    fig = px.scatter_geo(prov, lat="lat", lon="lon", size="cases", color="risk_score",
                         hover_name="province", hover_data={"cases":True,"risk_score":":.2f","lat":False,"lon":False},
                         scope="asia")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=500, margin={"l":0,"r":0,"t":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🔮 Prediction & Decision Support")
p1,p2,p3 = st.columns(3)
p1.metric("Prediksi Kasus 7 Hari", f"{s['forecast_7d']:,}", f"{s['forecast_change_pct']:+.1f}%")
p2.metric("Spatial Risk Signal", f"{s['spatial_risk']:.0%}")
p3.metric("Vulnerable Population Signal", f"{s['vulnerable_signal']:.0%}")

st.markdown("### Prioritas Tindak Lanjut")
for x in payload["recommendations"]:
    st.markdown(f"- **{x['priority']}** — {x['action']} — *{x['basis']}*")

with st.expander("🔗 SI-HIS Integration Contract"):
    st.code(payload["integration_contract"], language="text")

st.caption("Demo sintetis. EWS/ML bukan diagnosis atau deklarasi KLB dan tidak boleh menjadi satu-satunya dasar keputusan kesehatan masyarakat.")

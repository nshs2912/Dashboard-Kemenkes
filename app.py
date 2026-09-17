import streamlit as st

from config.dashboard_config import APP_TITLE, PERIOD_OPTIONS, DATA_SOURCE_OPTIONS
from services.sihis_client import get_kemenkes_intelligence
from services.data_service import normalize_intelligence
from services.intelligence_service import get_decision_signals
from components.filters import sidebar_filters
from components.kpi_cards import show_kpis
from components.charts import disease_chart, province_risk_chart
from components.maps import province_map
from components.tables import show_early_warning
from components.alerts import show_alerts

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("Dashboard keputusan nasional; intelligence dihitung oleh SI-HIS Intelligence.")

source, period, province = sidebar_filters(PERIOD_OPTIONS, DATA_SOURCE_OPTIONS)
mode = "api" if source == "SI-HIS API" else "demo"

try:
    payload = get_kemenkes_intelligence(mode=mode, period=period)
    data = normalize_intelligence(payload)
except Exception as exc:
    st.error(f"Gagal mengambil intelligence: {exc}")
    st.stop()

show_kpis(data)

st.divider()
st.header("1. Epidemiological Intelligence")
c1, c2 = st.columns(2)
with c1:
    disease_chart(data["top_disease"])
with c2:
    province_risk_chart(data["province_risk"])

st.header("2. Spatial Intelligence")
province_map(data["province_risk"])

st.header("3. Early Warning")
show_alerts(data)
show_early_warning(data["early_warning"])

st.header("4. Prediction & Vulnerable Population")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Forecast")
    st.dataframe(data["forecast"], use_container_width=True, hide_index=True)
with c2:
    st.subheader("Populasi Rentan")
    st.json(data["vulnerable_population"])

st.header("5. Decision Support")
signals = get_decision_signals(data)
st.metric("Status Prioritas", signals["priority"])
for item in data["recommendations"]:
    st.write("•", item)

with st.expander("Data provenance, interoperability & governance"):
    st.markdown("""
**Arsitektur data:** Multi-source → SI-HIS Data Hub → Data Quality →
Standardisasi → HL7 FHIR/Terminologi → SI-HIS Intelligence → Dashboard.

**Sumber data:** individu/NutriMed MyLab, mitra digital, dokter/klinik,
Puskesmas/SIMPUS, rumah sakit, laboratorium, farmasi, Dinkes, Kemenkes,
serta data pembiayaan/claims sesuai kewenangan dan integrasi.

**Interoperabilitas:** dashboard tidak mengolah ulang mesin intelligence;
dashboard mengonsumsi kontrak API SI-HIS.

**Governance:** sinyal ML merupakan decision support. Sinyal KLB bukan
penetapan KLB/outbreak; keputusan kesehatan masyarakat memerlukan
verifikasi surveilans dan proses otoritatif.
""")

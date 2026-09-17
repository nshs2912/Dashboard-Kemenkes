import streamlit as st
import pandas as pd

from config.dashboard_config import APP_TITLE, PERIOD_OPTIONS
from services.sihis_client import get_kemenkes_intelligence
from services.data_service import normalize_intelligence
from services.intelligence_service import get_decision_signals
from components.kpi_cards import show_kpis
from components.charts import disease_chart, province_risk_chart
from components.maps import province_map
from components.tables import show_early_warning
from components.alerts import show_alerts

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

def period_to_days(period: str) -> int:
    try:
        return int(str(period).split()[0])
    except (ValueError, IndexError):
        return 14

def records(value):
    if value is None:
        return []
    if isinstance(value, pd.DataFrame):
        return value.to_dict("records")
    return value if isinstance(value, list) else []

def show_provenance(data):
    p = data.get("data_provenance", {})
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Engine", p.get("engine", "Tidak tersedia"))
    with c2:
        st.metric("Dataset", p.get("dataset_type", "Tidak tersedia"))
    with c3:
        st.metric("Source", p.get("source", "Tidak tersedia"))
    st.caption(
        "Dashboard-Kemenkes tidak menghitung ulang intelligence epidemiologi; "
        "seluruh intelligence dikonsumsi dari SI-HIS Intelligence API."
    )

st.title(APP_TITLE)
st.caption(
    "National Health Intelligence Dashboard — SI-HIS sebagai intelligence "
    "engine, Dashboard-Kemenkes sebagai presentation dan decision-support layer."
)

# Dashboard hanya menggunakan SI-HIS API; tidak ada sumber demo lokal.
st.sidebar.header("⚙️ Dashboard Control")
period = st.sidebar.selectbox(
    "Periode Intelligence",
    PERIOD_OPTIONS,
    index=PERIOD_OPTIONS.index("14 Hari") if "14 Hari" in PERIOD_OPTIONS else 0,
)
province = st.sidebar.selectbox("Provinsi", ["Semua Provinsi"])
period_days = period_to_days(period)

st.sidebar.divider()
st.sidebar.info(
    "Sumber intelligence: **SI-HIS Intelligence API**. "
    "Dashboard tidak menggunakan dataset epidemiologi lokal."
)

try:
    with st.spinner("Mengambil intelligence dari SI-HIS..."):
        payload = get_kemenkes_intelligence(mode="api", period=period)

    if not isinstance(payload, dict):
        raise ValueError("Respons SI-HIS API bukan object JSON.")

    data = normalize_intelligence(payload)

except Exception as exc:
    st.error("❌ Gagal mengambil intelligence dari SI-HIS.")
    st.code(str(exc))
    st.markdown(
        """
**Periksa Streamlit Secrets:**
```toml
SIHIS_API_BASE_URL = "https://URL-SI-HIS-PORT-8000"
```

URL harus berupa root API, misalnya:
```text
https://xxxxx-8000.app.github.dev
```

Dashboard kemudian memanggil:
```text
/api/intelligence/kemenkes?period=14
```
"""
    )
    st.stop()

p = data.get("data_provenance", {})
if p.get("engine") == "SI-HIS Intelligence":
    st.success("🟢 Terhubung ke SI-HIS Intelligence API")
else:
    st.warning("🟡 Respons diterima, tetapi provenance belum mengidentifikasi SI-HIS.")

st.caption(f"Periode: **{period_days} hari** · Provinsi: **{province}**")

st.divider()
st.header("📌 National Intelligence Overview")
show_kpis(data)

st.divider()
st.header("1. 🦠 Epidemiological Intelligence")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Top Disease")
    items = records(data.get("top_disease"))
    disease_chart(items) if items else st.info("Belum ada data penyakit dari SI-HIS.")
with c2:
    st.subheader("Province Risk")
    items = records(data.get("province_risk"))
    province_risk_chart(items) if items else st.info("Belum ada data risiko provinsi dari SI-HIS.")

st.divider()
st.header("2. 🗺️ Spatial Intelligence")
items = records(data.get("province_risk"))
province_map(items) if items else st.info("Belum ada data spasial dari SI-HIS.")

st.divider()
st.header("3. 🚨 Early Warning System")
show_alerts(data)
items = records(data.get("early_warning"))
show_early_warning(items) if items else st.info(
    "Tidak ada sinyal early warning yang dikirim SI-HIS pada periode ini."
)

st.divider()
st.header("4. 🔮 Prediction & Vulnerable Population")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Forecast")
    forecast = records(data.get("forecast"))
    if forecast:
        fdf = pd.DataFrame(forecast)
        if {"date", "cases"}.issubset(fdf.columns):
            st.line_chart(fdf.set_index("date")["cases"])
        st.dataframe(fdf, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada forecast dari SI-HIS.")
with c2:
    st.subheader("Populasi Rentan")
    vulnerable = data.get("vulnerable_population", {})
    if isinstance(vulnerable, dict):
        signal = vulnerable.get("signal", 0.0)
        try:
            signal_text = f"{float(signal):.3f}"
        except (ValueError, TypeError):
            signal_text = str(signal)
        st.metric("Vulnerability Signal", signal_text)
        st.write(f"**Kelompok:** {vulnerable.get('group', 'Tidak tersedia')}")
    else:
        st.json(vulnerable)

st.divider()
st.header("5. 🧠 SI-HIS ML Intelligence Signals")
ml = data.get("ml", {})
if isinstance(ml, dict):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("KLB Signal", f"{float(ml.get('klb_signal', 0.0)):.3f}")
    with c2:
        st.metric("Spatial Risk", f"{float(ml.get('spatial_risk', 0.0)):.3f}")
    with c3:
        st.metric(
            "Vulnerable Population",
            f"{float(ml.get('vulnerable_population', 0.0)):.3f}",
        )
    st.caption(
        "Sinyal ML adalah decision support. Sinyal KLB bukan penetapan "
        "KLB/outbreak dan harus diverifikasi melalui surveilans epidemiologi."
    )
else:
    st.info("ML signal belum tersedia pada respons SI-HIS.")

st.divider()
st.header("6. 🎯 Decision Support")
signals = get_decision_signals(data)
st.metric("Status Prioritas", signals.get("priority", "Tidak tersedia"))
recommendations = data.get("recommendations", [])
if recommendations:
    for item in recommendations:
        st.write("•", item)
else:
    st.info("Belum ada rekomendasi yang dikirim SI-HIS.")

st.divider()
st.header("7. 📍 Province Intelligence")
if items:
    pdf = pd.DataFrame(items)
    if province != "Semua Provinsi" and "province" in pdf.columns:
        pdf = pdf[pdf["province"].astype(str) == province]
    if not pdf.empty:
        st.dataframe(pdf, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk provinsi yang dipilih.")
else:
    st.info("Data provinsi belum tersedia.")

st.divider()
with st.expander("🔐 Data Provenance, Interoperability & Governance"):
    show_provenance(data)
    st.markdown(
        """
### Arsitektur
```text
Multi-source Health Data
        ↓
SI-HIS Data Hub
        ↓
Data Quality & Standardization
        ↓
HL7 FHIR / Terminology
        ↓
SI-HIS Intelligence Engine
        ↓
FastAPI Intelligence API
        ↓
Dashboard-Kemenkes
```

### Governance
- Dashboard bukan intelligence engine.
- Sinyal ML adalah decision support, bukan keputusan otomatis.
- Sinyal KLB bukan penetapan KLB/outbreak.
- Cluster spasial tidak otomatis membuktikan sumber atau kausalitas penularan.
- Forecast adalah estimasi statistik, bukan kepastian.
- Produksi memerlukan validasi populasi/periode, monitoring drift, keamanan,
  governance, dan kontrol akses sesuai kewenangan.
"""
    )
    st.json(data.get("data_provenance", {}))

st.divider()
st.caption(
    "SI-HIS — Smart Integrated Health Intelligence System | "
    "Kemenkes National Health Intelligence Dashboard"
)

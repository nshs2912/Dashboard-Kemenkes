import streamlit as st

def show_alerts(data):
    signal = float(data.get("klb_signal", 0) or 0)
    if signal >= 0.80:
        st.error("KLB signal tinggi — perlu verifikasi surveilans dan investigasi epidemiologi.")
    elif signal >= 0.60:
        st.warning("KLB signal meningkat — perlu pemantauan dan verifikasi data.")
    else:
        st.success("Tidak ada sinyal KLB tinggi pada data demo.")

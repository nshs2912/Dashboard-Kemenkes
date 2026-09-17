import pandas as pd
import plotly.express as px
import streamlit as st

def disease_chart(items):
    if not items:
        st.info("Belum ada data penyakit.")
        return
    df = pd.DataFrame(items)
    st.plotly_chart(px.bar(df, x="disease", y="cases", title="Beban Penyakit Utama"), use_container_width=True)

def province_risk_chart(items):
    if not items:
        st.info("Belum ada data risiko provinsi.")
        return
    df = pd.DataFrame(items)
    st.plotly_chart(px.bar(df, x="province", y="risk", title="Profil Risiko Provinsi"), use_container_width=True)

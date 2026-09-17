import streamlit as st

def sidebar_filters(period_options, source_options):
    source = st.sidebar.selectbox("Data Source", source_options)
    period = st.sidebar.selectbox("Periode", period_options, index=1)
    province = st.sidebar.selectbox("Provinsi", ["Semua Provinsi"])
    return source, period, province

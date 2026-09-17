import pandas as pd
import plotly.express as px
import streamlit as st

def province_map(items):
    if not items:
        st.info("Data spasial belum tersedia.")
        return
    df = pd.DataFrame(items)
    required = {"latitude", "longitude", "province", "risk"}
    if not required.issubset(df.columns):
        st.info("Koordinat provinsi belum tersedia pada kontrak data.")
        return
    fig = px.scatter_geo(
        df, lat="latitude", lon="longitude",
        size="risk", color="risk",
        hover_name="province",
        projection="natural earth",
        title="Peta Risiko Provinsi"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

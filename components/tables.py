import pandas as pd
import streamlit as st

def show_early_warning(items):
    if not items:
        st.info("Tidak ada early warning.")
        return
    st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)

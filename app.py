from pathlib import Path

import pandas as pd
import streamlit as st


# Enable wide mode
st.set_page_config(layout="wide")


st.title("Forex Factory Calendar Dashboard")
st.markdown("_Prototype v0.0.1_")


def load_data() -> pd.DataFrame:
    filepath = Path(__file__).parent / "output" / "calendar.csv"

    if filepath.exists():
        return pd.read_csv(filepath)


# Load data into session state
if "dataframe" not in st.session_state:
    st.session_state.dataframe = load_data()

# Refresh button to manually update the DataFrame
if st.button("Refresh Data"):
    st.session_state.dataframe = load_data()

# Display the DataFrame
if st.session_state.dataframe is not None:
    st.dataframe(st.session_state.dataframe, use_container_width=True, height=600)
else:
    st.info("Please ensure the CSV file is available to visualize the data.")

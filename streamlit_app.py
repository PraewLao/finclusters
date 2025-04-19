import streamlit as st

st.set_page_config(page_title="Stock Return Predictor", layout="wide")

st.title("📊 Stock Return & Peers App")
st.markdown("""
Welcome! Use the sidebar to navigate:
- Page 2: Predict expected stock return using CAPM, FF3, or Carhart models.
""")

# === SIDEBAR ===
st.sidebar.title("🔍 Stock Selection")
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL)", value="AAPL")

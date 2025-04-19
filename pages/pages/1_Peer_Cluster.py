import streamlit as st

# Sidebar: Shared ticker input
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

st.title(f"🔎 Peer Analysis for {ticker.upper()}")

st.markdown("""
This page will display **peer companies** for the selected stock using clustering analysis.

📌 _Cluster model file will be integrated soon._
""")

# Placeholder for peer output
st.info("Cluster analysis results for peers will appear here.")

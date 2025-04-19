import streamlit as st

# Sidebar: Shared ticker input
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

st.title(f"💰 Price Forecast for {ticker.upper()}")

st.markdown("""
This page will calculate a **predicted price** based on expected return.

More inputs and logic will be added here.
""")

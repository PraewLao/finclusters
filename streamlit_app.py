import streamlit as st

# Sidebar input: Ticker (only typed once here!)
st.sidebar.title("📌 Global Settings")
ticker_input = st.sidebar.text_input("Enter stock ticker (e.g. AAPL)", value=st.session_state.get("ticker", ""))
st.session_state["ticker"] = ticker_input

st.title("Welcome to [Placeholder] App")
st.markdown("👈 Use the sidebar to enter a stock ticker. Then explore Pages 1–3 to analyze clusters, returns, and forecasts.")

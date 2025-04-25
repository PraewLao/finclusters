import streamlit as st

# === TICKER INPUT (PERSISTENT ACROSS ALL PAGES) ===
with st.sidebar:
    st.markdown("### 📌 Global Settings")
    ticker = st.text_input("Enter stock ticker (e.g. AAPL)", value=st.session_state.get("ticker", "")).upper().strip()
    st.session_state["ticker"] = ticker

st.title("Welcome to [Placeholder] App")
st.markdown("👈 Use the sidebar to enter a stock ticker. Then explore Pages 1–3 to analyze clusters, returns, and forecasts.")

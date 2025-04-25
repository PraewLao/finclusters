import streamlit as st
import yfinance as yf
import numpy as np

# === SIDEBAR (Live Global Ticker Input) ===
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "")).upper().strip()
st.session_state["ticker"] = ticker

if not ticker:
    st.warning("Please enter a stock ticker in the sidebar.")
    st.stop()

# === MAIN PAGE ===
try:
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    company_name = stock_info.get("longName", ticker.upper())
    forward_eps = stock_info.get("forwardEps", None)
    forward_pe = stock_info.get("forwardPE", None)

    st.title(f"💰 Price Forecast for {company_name}")

    # === Collect model-based return from Page 2 toggle ===
    model_return = st.session_state.get("expected_return", None)
    terminal_growth = 0.03
    model_price = None

    # Only compute if return is valid and forwardEPS is available
    if forward_eps and model_return is not None and model_return > terminal_growth:
        model_price = forward_eps / (model_return - terminal_growth)

    # Analyst forecast
    analyst_price = None
    if forward_pe and forward_eps:
        analyst_price = forward_pe * forward_eps

    # Peer forecast (real one)
    peer_min_return = st.session_state.get("peer_min_return", None)
    peer_max_return = st.session_state.get("peer_max_return", None)

    peer_price_min = None
    peer_price_max = None

    if forward_eps and peer_min_return is not None and peer_max_return is not None:
        if peer_max_return > terminal_growth:
            peer_price_min = forward_eps / (peer_max_return - terminal_growth)
        if peer_min_return > terminal_growth:
            peer_price_max = forward_eps / (peer_min_return - terminal_growth)

    # === Forecasted Price Summary ===
    st.markdown("---")
    st.subheader("📌 Forecasted Prices")
    if model_price:
        st.markdown(f"🧠 Model-Based Price Estimate: **${model_price:.2f}**")
    if peer_price_min and peer_price_max:
        st.markdown(f"📊 Peer-Based Price Range Estimate: **${peer_price_min:.2f}  ${peer_price_max:.2f}**")
    if analyst_price:
        st.markdown(f"📣 Analyst Price Estimate: **${analyst_price:.2f}**")

    # === 1-Year Chart ===
    hist = stock.history(period="1y")
    if not hist.empty:
        st.markdown("---")
        st.subheader("📉 One-Year Share Price")
        st.line_chart(hist["Close"], use_container_width=True)
    else:
        st.info("1Y price data not available.")

except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")

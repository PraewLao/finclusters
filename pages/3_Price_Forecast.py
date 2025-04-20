# === 📁 pages/page3.py ===
import streamlit as st
import yfinance as yf
import numpy as np

# === SIDEBAR ===
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

# === MAIN PAGE ===
if ticker:
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        company_name = stock_info.get("longName", ticker.upper())
        forward_eps = stock_info.get("forwardEps", None)
        forward_pe = stock_info.get("forwardPE", None)

        st.title(f"💰 Price Forecast for {company_name}")

        # === Collect model-based return ===
        model_return = st.session_state.get("expected_return", None)
        terminal_growth = 0.03
        model_price = None
        if forward_eps and model_return and model_return > terminal_growth:
            model_price = forward_eps / (model_return - terminal_growth)

        # Analyst forecast
        analyst_price = None
        if forward_pe and forward_eps:
            analyst_price = forward_pe * forward_eps

        # Peer forecast (placeholder)
        peer_price = None
        if model_price and analyst_price:
            peer_price = (model_price + analyst_price) / 2

        # === Forecasted Price Summary ===
        st.markdown("---")
        st.subheader("📌 Forecasted Prices")
        if model_price:
            st.markdown(f"🐮 Model-Based Price Estimate: **${model_price:.2f}**")
        if peer_price:
            st.markdown(f"🧠 Peer Price Estimate (Placeholder): **${peer_price:.2f}**")
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

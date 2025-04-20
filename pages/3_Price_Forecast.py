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

        st.title(f"💰 Price Forecast for {company_name}")
        st.markdown(f"**Forward EPS:** `{forward_eps}`")

        # === Model-based Price Forecast ===
        model_expected_return = st.number_input("", min_value=0.0, max_value=100.0, value=8.0, step=0.01, label_visibility="collapsed")
        model_return = model_expected_return / 100  # full precision
        terminal_growth = 0.03

        if forward_eps and model_return > terminal_growth:
            model_price = forward_eps / (model_return - terminal_growth)
            st.success(f"💸 Estimated Share Price (Model-Based): **${model_price:.2f}**")
        else:
            st.info("Cannot calculate model price: Missing forward EPS or invalid expected return.")

        # === Peer Price Placeholder ===
        st.markdown("---")
        st.subheader("🧠 Peer Price Range")
        st.info("Price range of peers will appear here based on clustering.")

        # === Analyst-Based Price Estimate ===
        st.markdown("---")
        st.subheader("📣 Analyst Price Forecast")
        forward_pe = stock_info.get("forwardPE", None)

        if forward_pe and forward_eps:
            analyst_price = forward_pe * forward_eps
            st.success(f"📈 Analyst Price Estimate: **${analyst_price:.2f}**")
        else:
            st.info("Forward P/E or EPS not available. Analyst price forecast cannot be calculated.")

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")

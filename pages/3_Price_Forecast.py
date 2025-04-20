# === 📁 pages/page3.py ===
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# === SIDEBAR ===
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

st.title(f"💰 Price Forecast for {ticker.upper()}")

# === MAIN PAGE ===
if ticker:
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        company_name = stock_info.get("longName", ticker.upper())
        sector = stock_info.get("sector", "Unknown")
        forward_eps = stock_info.get("forwardEps", None)

        st.markdown(f"**Company:** `{company_name}`")
        st.markdown(f"**Sector:** `{sector}`")
        st.markdown(f"**Forward EPS:** `{forward_eps}`")

        # Load model-based expected return from Page 2 (if saved or re-calculated here)
        # For demo purposes, we use a placeholder value
        model_expected_return = st.number_input("Enter Expected Return from Model (%)", min_value=0.0, max_value=100.0, value=8.0)
        model_return = model_expected_return / 100

        # Terminal growth assumption
        terminal_growth = 0.03

        # === Model-based Price Forecast ===
        if forward_eps and model_return > terminal_growth:
            fair_price = forward_eps / (model_return - terminal_growth)
            st.success(f"💸 Estimated Share Price from Model: **${round(fair_price, 2)}**")
        else:
            st.info("Cannot calculate price: Missing forward EPS or invalid expected return.")

        # === Peers Price Range Placeholder ===
        st.markdown("---")
        st.subheader("🧠 Peer Price Range")
        st.info("Price range of peers will appear here based on clustering.")

        # === Analyst-Based Forward P/E ===
        st.markdown("---")
        st.subheader("📣 Analyst Forward P/E")
        forward_pe = stock_info.get("forwardPE", None)
        if forward_pe:
            st.success(f"📊 Analyst Forward P/E: **{round(forward_pe, 2)}x**")
        else:
            st.info("Forward P/E not available.")

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")

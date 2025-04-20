# === 📁 pages/page3.py ===
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

        # === Pull YTD price data ===
        hist = stock.history(period="ytd")
        if not hist.empty:
            fig, ax = plt.subplots()
            hist["Close"].plot(ax=ax, label="YTD Price", color="gray")

            # Model-based price estimate
            model_return = st.session_state.get("expected_return", None)
            terminal_growth = 0.03
            model_price = None
            if forward_eps and model_return and model_return > terminal_growth:
                model_price = forward_eps / (model_return - terminal_growth)
                ax.axhline(model_price, color="green", linestyle="--", label="Model Estimate")

            # Analyst-based price estimate
            analyst_price = None
            if forward_pe and forward_eps:
                analyst_price = forward_pe * forward_eps
                ax.axhline(analyst_price, color="blue", linestyle=":", label="Analyst Estimate")

            # Placeholder peer estimate
            peer_price = (model_price + analyst_price) / 2 if model_price and analyst_price else None
            if peer_price:
                ax.axhline(peer_price, color="orange", linestyle="-.", label="Peer Estimate")

            ax.set_title(f"YTD Price and Forecasts for {ticker.upper()}")
            ax.set_ylabel("Price ($)")
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("YTD price data not available.")

        # === Forward EPS ===
        st.markdown(f"**Forward EPS:** `{forward_eps}`")

        # === Model-based Price Forecast ===
        if model_price:
            st.success(f"💸 Estimated Share Price (Model-Based): **${model_price:.2f}**")
        else:
            st.info("Cannot calculate model price: Missing forward EPS or expected return.")

        # === Peer Price Placeholder ===
        st.markdown("---")
        st.subheader("🧠 Peer Price Range")
        st.info("Price range of peers will appear here based on clustering.")

        # === Analyst-Based Price Estimate ===
        st.markdown("---")
        st.subheader("📣 Analyst Price Forecast")
        if analyst_price:
            st.success(f"📈 Analyst Price Estimate: **${analyst_price:.2f}**")
        else:
            st.info("Forward P/E or EPS not available. Analyst price forecast cannot be calculated.")

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")

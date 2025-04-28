import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# === Get ticker from global session state ===
ticker = st.session_state.get("ticker", "")

if not ticker:
    st.warning("⚠️ Please enter a stock ticker in the sidebar.")
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

    # Peer forecast
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
    st.subheader("📌 Forecasted Prices")
    
    # Prepare data for display
    forecast_data = []
    
    if model_price:
        forecast_data.append(("🧠 Model-Based", f"{model_price:.2f}"))
    
    if peer_price_min and peer_price_max:
        peer_range = f"{peer_price_min:.2f} - {peer_price_max:.2f}"
        forecast_data.append(("📊 Peer-Based Range", peer_range))
    
    if analyst_price:
        forecast_data.append(("📣 Analyst-Based", f"{analyst_price:.2f}"))
    
    # Display as table without index
    if forecast_data:
        forecast_df = pd.DataFrame(forecast_data, columns=["Estimate Type", "Price"])
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    # === Price Chart ===
    st.markdown("---")
    st.subheader(f"📉 {ticker} Share Price")
    
    # Get current live price
    current_price = stock_info.get("currentPrice", None)
    
    # Show current live price
    if current_price:
        st.markdown(f"💵 **Current Price:** ${current_price:.2f}")
    
    # Let user select time frame
    timeframe = st.radio(
        "Select Time Frame",
        options=["1M", "3M", "6M", "1Y", "2Y", "5Y", "Max"],
        index=3,
        horizontal=True
    )
        
    # Map selection to yfinance period
    def map_timeframe(duration):
        mapping = {
            "1M": "1mo",
            "3M": "3mo",
            "6M": "6mo",
            "1Y": "1y",
            "2Y": "2y",
            "5Y": "5y",
            "Max": "max"
        }
        return mapping.get(duration, "1y")
    
    period = map_timeframe(timeframe)
    hist = stock.history(period=period)
    
    if not hist.empty:
        st.line_chart(hist["Close"], use_container_width=True)
    else:
        st.info(f"{timeframe} price data not available.")


except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")

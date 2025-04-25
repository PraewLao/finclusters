import streamlit as st
import yfinance as yf

# === SIDEBAR ===
st.sidebar.title("📊 Price Forecast")
ticker = st.sidebar.text_input("Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

# === MAIN PAGE ===
if ticker:
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        company_name = stock_info.get("longName", ticker.upper())
        current_price = stock_info.get("regularMarketPrice", None)

        st.title(f"📈 Price Forecast for {company_name} ({ticker.upper()})")

        if current_price is None:
            st.error("❌ Current price data not available.")
            st.stop()

        st.markdown(f"**Current Price:** ${current_price:.2f}")

        # === Analyst-Based Price Estimate ===
        st.markdown("---")
        st.subheader("📣 Analyst-Based Price Estimate")
        forward_pe = stock_info.get("forwardPE", None)
        if forward_pe and forward_pe > 0:
            analyst_return = (1 / forward_pe) + 0.03
            analyst_price = current_price * (1 + analyst_return)
            st.success(f"📣 Analyst-Based Price Estimate: **${analyst_price:.2f}**")
        else:
            st.info("Forward P/E not available. Analyst price estimate could not be calculated.")

        # === Model-Based Price Estimate ===
        st.markdown("---")
        st.subheader("🧠 Model-Based Price Estimate")

        if "expected_return" in st.session_state:
            expected_return = st.session_state["expected_return"]
            model_price = current_price * (1 + expected_return)
            st.success(f"🧠 Model-Based Price Estimate: **${model_price:.2f}**")
        else:
            st.info("Expected return not available. Please run the Expected Return page first.")

    except Exception as e:
        st.error(f"Error: {e}")

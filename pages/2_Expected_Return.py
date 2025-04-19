import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Load model coefficients
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/sector_model_coefficients_by_ticker_UPDATED.csv"
    return pd.read_csv(url)

# Get default 10-year treasury yield
@st.cache_data
def get_default_rf():
    try:
        rf_yield = yf.Ticker("^TNX").info["regularMarketPrice"] / 100
        return round(rf_yield * 100, 2)  # return as percent
    except:
        return 4.0  # fallback

coeff_df = load_coefficients()
default_rf = get_default_rf()

# === SIDEBAR ===
st.sidebar.title("🔍 Stock Selection")
ticker = st.sidebar.text_input("Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

# === MAIN PAGE ===
if ticker:
    try:
        stock_info = yf.Ticker(ticker).info
        company_name = stock_info.get("longName", ticker.upper())
        sector = stock_info.get("sector", "Unknown")

        st.title(f"📈 Expected Return on {company_name} ({ticker.upper()})")
        st.markdown(f"**Sector:** `{sector}`")

        row = coeff_df[coeff_df["ticker"].str.upper() == ticker.upper()]
        if row.empty:
            st.error("❌ Ticker not found in model data.")
            st.stop()

        model_type = row["model"].values[0]
        intercept = row["intercept"].values[0]
        st.markdown(f"**Model used**: `{model_type}`")

        # Extract coefficients
        coefs = []
        for i in range(1, 5):
            col = f"coef_{i}"
            if col in row.columns and not pd.isna(row[col].values[0]):
                coefs.append(row[col].values[0])

        # Use static inputs for model factors
        factor_inputs = {
            "CAPM": [0.01],
            "FF3": [0.01, 0.02, -0.01],
            "Carhart": [0.01, 0.02, -0.01, 0.015]
        }
        x = np.array(factor_inputs[model_type])

        # Risk-Free Rate input
        rf_percent = st.number_input("Enter Risk-Free Rate (%)", min_value=0.0, max_value=100.0, value=default_rf)
        rf = rf_percent / 100

        # Prediction
        monthly_return = intercept + np.dot(coefs, x) + rf
        st.success(f"📊 Expected Monthly Return on {ticker.upper()}: **{round(monthly_return * 100, 2)}%**")

    # === PEER RETURN RANGE (placeholder) ===
st.markdown("---")
st.subheader("🧠 Expected Return Range of Peers")
st.info("Peer returns based on cluster analysis will be displayed here.")

# === ANALYST RETURN ESTIMATE (placeholder) ===
st.markdown("---")
st.subheader("📣 Expected Return by Analyst Forecasts")
st.info("Analyst-derived return estimates will appear here.")


    except Exception as e:
        st.error(f"Error: {e}")

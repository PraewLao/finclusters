import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Load model coefficients
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/sector_model_coefficients_by_ticker_REPLACEMENT.csv"
    return pd.read_csv(url)

# Get default 10-year treasury yield
@st.cache_data
def get_default_rf():
    try:
        rf_yield = yf.Ticker("^TNX").info["regularMarketPrice"] / 100
        return round(rf_yield * 100, 2)
    except:
        return 4.0

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

        # Coefficient list
        coefs = []
        for i in range(1, 5):
            col = f"coef_{i}"
            if col in row.columns and not pd.isna(row[col].values[0]):
                coefs.append(row[col].values[0])

        # Identify GICS sector
        gics_sector = str(row["gics"].values[0]) if "gics" in row.columns else "Unknown"

        # Default factor values
        factor_inputs = {
            "CAPM": [0.01],
            "FF3": [0.01, 0.02, -0.01],
            "Carhart": [0.01, 0.02, -0.01, 0.015]
        }

        # Forward-looking toggle for CAPM in GICS 35 or 45
        if model_type == "CAPM" and gics_sector in ["35", "45"]:
            use_forward = st.toggle("Use forward-looking market premium (4.42%)?", value=False)
            factor_inputs["CAPM"] = [0.0442] if use_forward else [0.01]

        x = np.array(factor_inputs[model_type])

        rf_percent = st.number_input("Enter Risk-Free Rate (%)", min_value=0.0, max_value=100.0, value=default_rf)
        rf = rf_percent / 100

        monthly_return = intercept + np.dot(coefs, x) + rf

        # Save for Page 3
        st.session_state["expected_return"] = monthly_return

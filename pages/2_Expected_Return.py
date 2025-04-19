import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Load updated model coefficients
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/sector_model_coefficients_by_ticker_UPDATED.csv"
    return pd.read_csv(url)

coeff_df = load_coefficients()

# === SIDEBAR ===
st.sidebar.title("🔍 Stock Selection")
ticker = st.sidebar.text_input("Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker  # share across pages

# === MAIN PAGE ===
if ticker:
    try:
        stock_info = yf.Ticker(ticker).info
        sector = stock_info.get("sector", "Unknown")

        st.title(f"📈 Expected Return on {ticker.upper()}")
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

        # Factor labels and default inputs
        factor_labels = {
            "CAPM": "Enter MKT-RF",
            "FF3": "Enter MKT-RF, SMB, HML",
            "Carhart": "Enter MKT-RF, SMB, HML, MOM"
        }
        defaults = {
            "CAPM": "0.01",
            "FF3": "0.01, 0.02, -0.01",
            "Carhart": "0.01, 0.02, -0.01, 0.015"
        }

        factor_input = st.text_input(factor_labels[model_type], value=defaults[model_type])

        # Risk-Free Rate input (as percentage)
        rf_percent = st.number_input("Enter Risk-Free Rate (%)", min_value=0.0, max_value=100.0, value=0.4)
        rf = rf_percent / 100

        # Prediction logic
        try:
            x = np.array([float(i.strip()) for i in factor_input.split(",")])
            monthly_return = intercept + np.dot(coefs, x) + rf
            st.success(f"📊 Expected Return on {ticker.upper()}: **{round(monthly_return * 100, 2)}%**")
        except:
            st.error("⚠️ Please check that your factor inputs match the model type.")

    except Exception as e:
        st.error(f"Error: {e}")

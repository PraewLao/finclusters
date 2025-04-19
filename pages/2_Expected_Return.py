import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Load model coefficients
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/refs/heads/main/sector_model_coefficients_by_ticker.csv"
    return pd.read_csv(url)

coeff_df = load_coefficients()

st.title("📈 Expected Return Predictor (by Ticker)")

# --- Ticker input ---
ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="AAPL")

if ticker:
    try:
        stock_info = yf.Ticker(ticker).info
        sector = stock_info.get("sector", "Unknown")
        st.markdown(f"**Sector:** `{sector}`")

        # --- Match ticker to model and coefficients ---
        row = coeff_df[coeff_df["ticker"].str.upper() == ticker.upper()]

        if row.empty:
            st.error("❌ Ticker not found in trained model data.")
            st.stop()

        model_type = row["model"].values[0]
        intercept = row["intercept"].values[0]
        sector_model = row["sector"].values[0]

        # Get relevant coefficients
        coefs = []
        for i in range(1, 5):
            col = f"coef_{i}"
            if col in row.columns and not pd.isna(row[col].values[0]):
                coefs.append(row[col].values[0])

        st.markdown(f"**Model used**: `{model_type}`")

        # --- Factor input ---
        factor_labels = {
            "CAPM": "Enter MKT-RF (e.g. 0.01)",
            "FF3": "Enter MKT-RF, SMB, HML",
            "Carhart": "Enter MKT-RF, SMB, HML, MOM"
        }

        default_inputs = {
            "CAPM": "0.01",
            "FF3": "0.01, 0.02, -0.01",
            "Carhart": "0.01, 0.02, -0.01, 0.015"
        }

        factor_input = st.text_input(factor_labels[model_type], value=default_inputs[model_type])
        rf = st.number_input("Enter Risk-Free Rate (e.g. 0.004)", value=0.004, step=0.001)

        try:
            x = np.array([float(i.strip()) for i in factor_input.split(",")])
            predicted_excess = intercept + np.dot(coefs, x)
            predicted_total = predicted_excess + rf

            annual_return = (1 + predicted_total) ** 12 - 1
st.success(f"📈 Predicted **Annual Return**: **{round(annual_return * 100, 2)}%**")

        except:
            st.error("⚠️ Please check that your factor inputs match the model type.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

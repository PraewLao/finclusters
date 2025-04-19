import streamlit as st
import yfinance as yf
import numpy as np

st.title("📈 Expected Return Prediction")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL)", value="AAPL")

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        sector = info.get("sector", "Unknown")

        st.markdown(f"**Sector:** `{sector}`")

        # === Choose model based on sector ===
        if "Health" in sector:
            model_name = "CAPM"
            intercept = 0.0021
            coef = [1.12]
            input_label = "Enter MKT-RF (e.g. 0.01)"
            default_input = "0.01"

        elif "Consumer" in sector:
            model_name = "FF3"
            intercept = 0.0018
            coef = [1.10, 0.22, -0.15]
            input_label = "Enter MKT-RF, SMB, HML (comma-separated)"
            default_input = "0.01, 0.02, -0.01"

        elif "Information" in sector:
            model_name = "Carhart"
            intercept = 0.0023
            coef = [1.05, 0.20, -0.10, 0.08]
            input_label = "Enter MKT-RF, SMB, HML, MOM (comma-separated)"
            default_input = "0.01, 0.02, -0.01, 0.015"

        else:
            st.warning("⚠️ This sector is not supported yet.")
            st.stop()

        # === Factor Inputs ===
        factor_input = st.text_input(input_label, value=default_input)
        rf = st.number_input("Enter current Risk-Free Rate (e.g. 0.004)", value=0.004, step=0.001)

        # === Prediction ===
        try:
            x = np.array([float(i.strip()) for i in factor_input.split(",")])
            excess_return = intercept + np.dot(coef, x)
            predicted_return = excess_return + rf

            st.success(f"📊 Predicted Monthly Return: **{round(predicted_return*100, 2)}%**")
        except:
            st.error("⚠️ Please check that your factor inputs are formatted correctly.")

    except Exception as e:
        st.error(f"Could not fetch data for {ticker}: {e}")

import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Load the expected return model
@st.cache_resource
def load_model():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/expected_return_model.pkl"
    response = requests.get(url)
    model_bytes = io.BytesIO(response.content)
    return pickle.load(model_bytes)


data = load_model()
models = data["models"]
ticker_to_sector = data["ticker_to_sector"]

# Streamlit UI
st.title("📈 Expected Return Prediction")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL, TSLA)")

if ticker:
    ticker = ticker.upper()
    sector = ticker_to_sector.get(ticker)

    if sector is None:
        st.error("Ticker not found in the training set.")
    else:
        model_data = models.get(sector, {})
        result = model_data.get(ticker)

        if result is None:
            st.warning("No model available for this ticker.")
        else:
            y_pred = result["y_pred"]
            predicted_return = y_pred.mean()

            st.markdown(f"### 🧠 Best Model for Sector {sector}")
            st.success(f"Predicted Average Monthly Return: **{predicted_return:.2%}**")

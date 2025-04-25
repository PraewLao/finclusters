import streamlit as st
import pandas as pd
import requests

# Load coefficients from GitHub
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/expected_return_coefficients.csv"
    return pd.read_csv(url)

df = load_coefficients()

st.title("📈 Expected Return Prediction")

# User input
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, JNJ)").upper()

# Monthly average values from 2000–2024 training set
default_factors = {
    'MKT_RF': 0.0062,
    'SMB': 0.0027,
    'HML': 0.0024,
    'MOM': 0.0037
}

if ticker:
    row = df[df['Ticker'] == ticker]

    if row.empty:
        st.error("Ticker not found.")
    else:
        gics = row.iloc[0]['GICS']
        model = row.iloc[0]['Model']
        alpha = row.iloc[0]['Alpha']
        beta_mkt = row.iloc[0]['Beta_MKT_RF']
        beta_smb = row.iloc[0].get('Beta_SMB', 0) or 0
        beta_hml = row.iloc[0].get('Beta_HML', 0) or 0
        beta_mom = row.iloc[0].get('Beta_MOM', 0) or 0

        # Use forward-looking premium toggle for Healthcare (GICS 35 with CAPM)
        if str(gics) == '35' and model == 'CAPM':
            use_forward = st.toggle("Use forward-looking market premium (4.42%)?", value=False)
            mkt_rf = 0.0442 if use_forward else default_factors['MKT_RF']
        else:
            mkt_rf = default_factors['MKT_RF']

        # Calculate expected return
        expected_return = alpha + beta_mkt * mkt_rf
        if model in ['FF3', 'Carhart']:
            expected_return += beta_smb * default_factors['SMB'] + beta_hml * default_factors['HML']
        if model == 'Carhart':
            expected_return += beta_mom * default_factors['MOM']

        st.markdown(f"### 🧠 Model Used: {model}  |  GICS Sector: {gics}")
        st.success(f"Predicted Monthly Return: **{expected_return:.2%}**")

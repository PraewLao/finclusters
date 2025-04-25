import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Load model coefficients from CSV
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/sector_model_coefficients_by_ticker_REPLACEMENT.csv"
    return pd.read_csv(url)

# Load Active Companies CSV for Peer Filtering
ACTIVE_COMPANIES_URL = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/Active_Companies.csv"
active_companies_df = pd.read_csv(ACTIVE_COMPANIES_URL)
active_tickers = set(active_companies_df['Ticker'].str.upper())

# Get default 10-year treasury yield from Yahoo Finance
@st.cache_data
def get_default_rf():
    try:
        rf_yield = yf.Ticker("^TNX").info["regularMarketPrice"] / 100
        return round(rf_yield * 100, 2)
    except:
        return 4.0

# Load model data and treasury yield
coeff_df = load_coefficients()
default_rf = get_default_rf()

# === SIDEBAR (Live Global Ticker Input) ===
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "")).upper().strip()
st.session_state["ticker"] = ticker

if not ticker:
    st.warning("Please enter a stock ticker in the sidebar.")
    st.stop()

# === MAIN PAGE ===
try:
    stock_info = yf.Ticker(ticker).info
    company_name = stock_info.get("longName", ticker.upper())
    sector_name = stock_info.get("sector", "Unknown")

    st.title(f"📈 Expected Return on {company_name} ({ticker.upper()})")
    st.markdown(f"**Sector:** `{sector_name}`")

    # Match ticker with model coefficients
    row = coeff_df[coeff_df["ticker"].str.upper() == ticker.upper()]
    if row.empty:
        st.error("❌ Ticker not found in model data.")
        st.stop()

    model_type = row["model"].values[0]
    intercept = row["intercept"].values[0]
    st.markdown(f"**Model used**: `{model_type}`")

    # Extract sector code from CSV (e.g. GICS_35, GICS_45)
    sector_code = row["sector"].values[0] if "sector" in row.columns else "Unknown"

    # Extract coefficients
    coefs = []
    for i in range(1, 5):
        col = f"coef_{i}"
        if col in row.columns and not pd.isna(row[col].values[0]):
            coefs.append(row[col].values[0])

    # Default factor inputs
    factor_inputs = {
        "CAPM": [0.01],
        "FF3": [0.01, 0.02, -0.01],
        "Carhart": [0.01, 0.02, -0.01, 0.015]
    }

    # Show toggle if CAPM and GICS_35 or GICS_45
    if model_type == "CAPM" and sector_code in ["GICS_35", "GICS_45"]:
        use_forward = st.toggle("Use forward-looking market premium?", value=False)
        factor_inputs["CAPM"] = [0.0442] if use_forward else [0.01]

    # Calculate expected return
    x = np.array(factor_inputs[model_type])
    rf_percent = st.number_input("Enter Risk-Free Rate (%)", min_value=0.0, max_value=100.0, value=default_rf)
    rf = rf_percent / 100
    monthly_return = intercept + np.dot(coefs, x) + rf

    # Save to session state for Page 3
    st.session_state["expected_return"] = monthly_return

    st.success(f"🧠 Expected Return on {ticker.upper()}: **{round(monthly_return * 100, 2)}%**")

    # === Find Peers from Same Cluster ===
    # Filter peers from same cluster
    peers = coef_df[(coef_df['sector'] == sector) & (coef_df['cluster'] == cluster_id)]
    
    # Only keep peers that are still active
    peers = peers[peers['ticker'].isin(active_tickers)]
    
    # Calculate expected return for each peer
    peer_expected_returns = []
    
    for _, peer in peers.iterrows():
        if sector in ['GICS_35', 'GICS_45']:  # CAPM sectors
            expected_return_peer = rf + (peer['mkt_excess'] * mkt_premium)
        elif sector == 'GICS_25':  # FF3 sector
            expected_return_peer = (
                rf + (peer['mkt_excess'] * mkt_premium) +
                (peer['smb'] * smb_premium) +
                (peer['hml'] * hml_premium)
            )
        else:
            expected_return_peer = None
    
        if expected_return_peer is not None:
            peer_expected_returns.append(expected_return_peer)
    
    # Show min and max expected returns
    if peer_expected_returns:
        min_peer_return = min(peer_expected_returns)
        max_peer_return = max(peer_expected_returns)
    
        st.subheader("📈 Peer Companies' Expected Return Range:")
        st.write(f"Lowest Expected Return: **{min_peer_return:.2%}**")
        st.write(f"Highest Expected Return: **{max_peer_return:.2%}**")
    else:
        st.warning("⚠️ No active peers found to calculate expected return range.")

    # === Analyst Forecast Section ===
    st.markdown("---")
    st.subheader("📣 Expected Return by Analyst Forecasts")
    forward_pe = stock_info.get("forwardPE", None)
    if forward_pe and forward_pe > 0:
        analyst_return = (1 / forward_pe) + 0.03
        st.success(f"📣 Analyst-Based Expected Return: **{round(analyst_return * 100, 2)}%**")
    else:
        st.info("Forward P/E not available. Analyst return estimate could not be calculated.")

except Exception as e:
    st.error(f"Error: {e}")

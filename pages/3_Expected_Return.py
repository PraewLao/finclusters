import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# === Get ticker from global session state ===
ticker = st.session_state.get("ticker", "")

if not ticker:
    st.warning("⚠️ Please enter a stock ticker in the sidebar.")
    st.stop()

# Load model coefficients from CSV
@st.cache_data
def load_coefficients():
    url = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/main/sector_model_coefficients_by_ticker_REPLACEMENT.csv"
    return pd.read_csv(url)

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

# === MAIN PAGE ===
try:
    stock_info = yf.Ticker(ticker).info
    company_name = stock_info.get("longName", ticker.upper())
    sector_name = stock_info.get("sector", "Unknown")

    # Adjust sector display name 
    if sector_name == "Consumer Cyclical":
        sector_name = "Consumer Discretionary"
    elif sector_name == "Technology":
        sector_name = "Information Technology"


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

    # === Peer Range Calculation ===
    st.markdown("---")
    st.subheader("📊 Expected Return Range of Peers")

    try:
        peer_returns = []

        if "peer_tickers" not in st.session_state or not st.session_state["peer_tickers"]:
            st.info("No peer tickers found from Page 1.")
        else:
            for peer_ticker in st.session_state["peer_tickers"]:
                peer_row = coeff_df[coeff_df["ticker"].str.upper() == peer_ticker]
                if peer_row.empty:
                    continue

                peer_row = peer_row.iloc[0]
                model = peer_row["model"]
                intercept_peer = peer_row["intercept"]

                # Get coefficients
                coefs_peer = []
                for i in range(1, 5):
                    col = f"coef_{i}"
                    if col in peer_row and not pd.isna(peer_row[col]):
                        coefs_peer.append(peer_row[col])

                # Get factor vector
                if model == "CAPM":
                    x_peer = [0.0442]
                elif model == "FF3":
                    x_peer = [0.01, 0.02, -0.01]
                elif model == "Carhart":
                    x_peer = [0.01, 0.02, -0.01, 0.015]
                else:
                    continue  # Skip unknown models

                if len(coefs_peer) == len(x_peer):
                    expected_return_peer = intercept_peer + np.dot(coefs_peer, x_peer) + rf
                    peer_returns.append(expected_return_peer)

            if peer_returns:
                st.success(f"📉 Lowest Peer Return: **{min(peer_returns):.2%}**")
                st.success(f"📈 Highest Peer Return: **{max(peer_returns):.2%}**")
            
                # Save to session state for Page 3
                st.session_state["peer_min_return"] = min(peer_returns)
                st.session_state["peer_max_return"] = max(peer_returns)
            
            else:
                st.info("No valid expected return could be calculated for peers.")

    except Exception as e:
        st.error(f"Error calculating peer return range: {e}")

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

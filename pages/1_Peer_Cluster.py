import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

st.title("📊 Financial Ratio Cluster Finder")

# === Load Ticker & Sector Reference CSV ===
TICKER_SECTOR_FILE = 'sector_model_coefficients_by_ticker_REPLACEMENT.csv'
ticker_sector_df = pd.read_csv(TICKER_SECTOR_FILE)

# === Sector-Specific Model and Feature Config ===
MODEL_CONFIG = {
    'GICS_35': {
        'scaler': 'scaler_hc.pkl',
        'kmeans': 'kmeans_model_hc.pkl',
        'pca': 'pca_transformer_hc.pkl',
        'data': 'clustered_data_hc.csv',
        'features': ['ROA', 'ROE', 'ROA_vol', 'ROE_vol', 'RD_Sales', 'Debt_Assets', 'Market_Book', 'WC_TA', 'RE_TA']
    },
    'GICS_25': {
        'scaler': 'scaler_cd.pkl',
        'kmeans': 'kmeans_model_cd.pkl',
        'pca': 'pca_transformer_cd.pkl',
        'data': 'clustered_data_cd.csv',
        'features': ['ROA', 'ROE', 'RD_Sales', 'Debt_Assets', 'Market_Book', 'WC_TA', 'RE_TA', 'ROA_vol', 'ROE_vol']
    },
    'GICS_45': {
        'scaler': 'scaler_IT.pkl',
        'kmeans': 'kmeans_model_IT.pkl',
        'pca': 'pca_transformer_IT.pkl',
        'data': 'clustered_data_cd_IT.csv',
        'features': ['ROA', 'ROE', 'ROA_vol', 'ROE_vol', 'RD_Sales', 'SGA_Sales', 'CapEx_Sales', 'Debt_Assets', 'Market_Book', 'WC_TA']
    }
}

# === Model Loader ===
@st.cache_resource
def load_models_and_data(sector_key):
    cfg = MODEL_CONFIG[sector_key]
    scaler = joblib.load(cfg['scaler'])
    kmeans = joblib.load(cfg['kmeans'])
    pca = joblib.load(cfg['pca'])
    df = pd.read_csv(cfg['data'])
    features = cfg['features']
    return scaler, kmeans, pca, df, features

# === Ticker Input ===
ticker = st.text_input("Enter ticker symbol:").upper().strip()

if ticker:
    if ticker in ticker_sector_df['ticker'].values:
        sector_key = ticker_sector_df[ticker_sector_df['ticker'] == ticker]['sector'].iloc[0]

        st.info(f"🔍 {ticker} belongs to **{sector_key}** sector.")

        if sector_key in MODEL_CONFIG:
            scaler, kmeans, pca, df, features = load_models_and_data(sector_key)

            if ticker in df['tic'].values:
                company = df[df['tic'] == ticker].iloc[0]
                cluster_id = int(company['cluster'])

                st.success(f"✅ {ticker} is in **Cluster {cluster_id}**")

                # === Similar Companies ===
                st.subheader("🏢 Similar Companies:")
                peers = df[df['cluster'] == cluster_id][['tic', 'fyear']].sort_values(by='fyear', ascending=False).head(10)
                st.dataframe(peers)

                # === PCA Visualization ===
                if 'pca_1' in df.columns and 'pca_2' in df.columns:
                    st.subheader("🧭 PCA Cluster Visualization")
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.scatter(df['pca_1'], df['pca_2'], c=df['cluster'], cmap='viridis', alpha=0.3)
                    ax.scatter(company['pca_1'], company['pca_2'], color='red', s=100, label=ticker, edgecolor='black')
                    ax.set_title('Cluster View with PCA')
                    ax.set_xlabel('PCA 1')
                    ax.set_ylabel('PCA 2')
                    ax.legend()
                    st.pyplot(fig)
            else:
                st.error("❌ Ticker not found in sector-specific data.")
        else:
            st.error("❌ No model defined for this GICS sector.")
    else:
        st.error("❌ Ticker not found in sector reference CSV.")
else:
    st.info("ℹ️ Please enter a ticker symbol to begin.")

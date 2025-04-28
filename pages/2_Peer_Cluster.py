import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.title("📊 Peer Cluster Finder")

# === Get ticker from global session state ===
ticker = st.session_state.get("ticker", "")

if not ticker:
    st.warning("⚠️ Please enter a stock ticker in the sidebar.")
    st.stop()

# === Load Ticker & Sector Reference CSV ===
TICKER_SECTOR_FILE = 'sector_model_coefficients_by_ticker_REPLACEMENT.csv'
ticker_sector_df = pd.read_csv(TICKER_SECTOR_FILE)

# === Load Active Companies CSV ===
ACTIVE_COMPANIES_URL = "https://raw.githubusercontent.com/PraewLao/price-and-peers-app/refs/heads/main/Active_Companies.csv"
active_companies_df = pd.read_csv(ACTIVE_COMPANIES_URL)
active_tickers = set(active_companies_df['Ticker'].str.upper())

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

# === Main Logic ===
if ticker in ticker_sector_df['ticker'].values:
    sector_key = ticker_sector_df[ticker_sector_df['ticker'] == ticker]['sector'].iloc[0]

    st.info(f"🔍 {ticker} belongs to **{sector_key}** sector.")

    if sector_key in MODEL_CONFIG:
        scaler, kmeans, pca, df, features = load_models_and_data(sector_key)

        if ticker in df['tic'].values:
            company = df[df['tic'] == ticker].iloc[0]
            cluster_id = int(company['cluster'])

            st.success(f"✅ {ticker} is in **Cluster {cluster_id}**")

            # === Peer Companies ===
            # Get most recent data per ticker
            peers_recent = (
                df[df['cluster'] == cluster_id]
                .sort_values(by=['tic', 'fyear'], ascending=[True, False])
                .drop_duplicates(subset='tic')  # Keep latest year per ticker
            )

            
            # Filter peers that are in active companies list
            active_peers = peers_recent[peers_recent['tic'].isin(active_tickers)]
            
            # Save to session state for use on Page 2
            st.session_state["peer_tickers"] = active_peers["tic"].str.upper().tolist()

            
            # Show only active peer tickers
            if not active_peers.empty:
                st.subheader("🏢 Active Peer Companies")
                sorted_peers = active_peers[['tic']].rename(columns={'tic': 'Ticker'}).sort_values(by='Ticker').reset_index(drop=True)
                st.dataframe(sorted_peers, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ No active peers found for this cluster.")



            # === Cluster Visualization ===
            if 'pca_1' in df.columns and 'pca_2' in df.columns:
                st.subheader("🧭 PCA Cluster Visualization")
            
                # Add hover text combining ticker and fiscal year
                df['hover_text'] = df['tic'] + " | Year: " + df['fyear'].astype(str)
            
                fig = px.scatter(
                    df, x='pca_1', y='pca_2', color='cluster',
                    hover_name='hover_text',
                    hover_data={'fyear': False, 'pca_1': False, 'pca_2': False},
                    color_continuous_scale='Viridis',
                    opacity=0.6,
                    title='PCA Cluster View '
                )
            
                # Highlight selected company
                fig.add_scatter(
                    x=[company['pca_1']], y=[company['pca_2']],
                    mode='markers+text',
                    marker=dict(color='red', size=14, line=dict(color='black', width=2)),
                    text=[ticker],
                    textposition='top center',
                    name='Selected Company'
                )
            
                fig.update_layout(height=600, width=900)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Ticker not found in sector-specific data.")
    else:
        st.error("❌ No model defined for this GICS sector.")
else:
    st.error("❌ Ticker not found in sector reference CSV.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

st.title("📊 Financial Ratio Cluster Finder")

# === 1. Load model & data safely ===

# If TIC's GICS is 35 (need revision)
@st.cache_resource
def load_models_and_data():
    try:
        scaler = joblib.load('scaler_hc.pkl')
        kmeans = joblib.load('kmeans_model_hc.pkl')
        pca = joblib.load('pca_transformer_hc.pkl')
        df = pd.read_csv('clustered_data_hc.csv')
        return scaler, kmeans, pca, df
    except FileNotFoundError as e:
        st.error(f"❌ File not found: {e.filename}")
        return None, None, None, None

scaler, kmeans, pca, df = load_models_and_data()

# If TIC's GICS is 25 (need revision)
# need to define scaler, kmeans, pca, df with correct files

# If TIC's GICS is 35 (need revision)
# need to define scaler, kmeans, pca, df with correct files

# === 2. Define features used in clustering ===
features = ['ROA', 'ROE', 'RD_Sales', 'Debt_Assets', 'Market_Book', 'ROA_vol', 'ROE_vol']

# === 3. Ticker Input ===
ticker = st.text_input("Enter ticker symbol:").upper().strip()

if ticker:
    if ticker in df['tic'].values:
        company = df[df['tic'] == ticker].iloc[0]
        cluster_id = int(company['cluster'])

        st.success(f"✅ {ticker} is in **Cluster {cluster_id}**")

        # === 4. Show Similar Companies in Cluster ===
        st.subheader("🏢 Similar Companies in the Same Cluster:")
        cluster_peers = df[df['cluster'] == cluster_id][['tic', 'fyear']].sort_values(by='fyear', ascending=False).head(10)
        st.dataframe(cluster_peers)

        # === 5. PCA Scatter Plot with Highlight ===
        if 'pca_1' in df.columns and 'pca_2' in df.columns:
            st.subheader("🧭 PCA Visualization of Clusters")
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(df['pca_1'], df['pca_2'], c=df['cluster'], cmap='viridis', alpha=0.3, label='Companies')
            ax.scatter(company['pca_1'], company['pca_2'], color='red', s=100, label=ticker, edgecolor='black')
            ax.set_title('Cluster View with PCA')
            ax.set_xlabel('PCA 1')
            ax.set_ylabel('PCA 2')
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("⚠️ PCA columns not found in the data.")
    else:
        st.error("❌ Ticker not found in dataset.")
else:
    st.info("ℹ️ Please enter a ticker symbol to begin.")

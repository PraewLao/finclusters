import streamlit as st

# Sidebar: Shared ticker input
ticker = st.sidebar.text_input("🔍 Enter stock ticker", value=st.session_state.get("ticker", "AAPL"))
st.session_state["ticker"] = ticker

st.title(f"🔎 Peer Analysis for {ticker.upper()}")

st.markdown("""
This page will display **peer companies** for the selected stock using clustering analysis.

📌 _Cluster model file will be integrated soon._
""")

# Placeholder for peer output
st.info("Cluster analysis results for peers will appear here.")
import streamlit as st
import pandas as pd
import joblib

# Load model & data
scaler = joblib.load('scaler.pkl')
kmeans = joblib.load('kmeans_model.pkl')
pca = joblib.load('pca_transformer.pkl')
df = pd.read_csv('clustered_data.csv')

features = ['ROA', 'ROE', 'RD_Sales', 'Debt_Assets', 'Market_Book', 'ROA_vol', 'ROE_vol']

st.title("Financial Ratio Cluster Finder")

ticker = st.text_input("Enter ticker symbol:")

if ticker in df['tic'].values:
    company = df[df['tic'] == ticker].iloc[0]
    cluster_id = company['cluster']
    
    st.success(f"✅ {ticker} is in Cluster {int(cluster_id)}")

    # Show similar companies
    st.subheader("Similar Companies in Cluster:")
    cluster_peers = df[df['cluster'] == cluster_id][['tic', 'fyear']]
    st.dataframe(cluster_peers)

    # Show PCA plot
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['pca_1'], df['pca_2'], c=df['cluster'], cmap='viridis', alpha=0.4)
    ax.scatter(company['pca_1'], company['pca_2'], color='red', s=100, label=ticker)
    ax.set_title('PCA Clustering Visualization')
    ax.set_xlabel('PCA 1')
    ax.set_ylabel('PCA 2')
    ax.legend()
    st.pyplot(fig)
else:
    if ticker != "":
        st.error("❌ Ticker not found in dataset.")

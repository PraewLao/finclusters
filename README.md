# FinClusters: Multi-Industry Financial Clustering App

A multi-page Streamlit app for clustering companies by financial ratios across Health Care (GICS 35), Consumer Discretionary (GICS 25), and Information Technology (GICS 45) sectors. The app helps identify peer companies and visualize cluster positions interactively.

---

## Description

This GitHub repository contains a working prototype for an interactive multi-industry clustering Streamlit Dashboard. It allows users to input stock tickers and:
- Identify which cluster the company belongs to based on financial ratios.
- View peer companies in the same cluster.
- Visualize clusters using PCA.
- Analyze expected return ranges from CAPM/FF3/Carhart models.
- Estimate future prices based on analyst forecasts and model returns.

The app uses pre-trained models per GICS sector with sector-specific financial ratios and supports session state across pages.

There are 5 Python scripts that create the 4 interactive and connected pages in the app:

- **`streamlit_app.py`** – The homepage of the app (explains purpose and instructions)
- **`page0.py`** – Welcome page
- **`page1.py`** – Methodology
- **`page2.py`** – Peer Clustering analysis and visualization
- **`page3.py`** – Expected Return analysis from models and forecasts
- **`page4.py`** – Price Forecasting based on expected returns

---

## Getting Started

### Dependencies 

- The **`requirements.txt`** file contains all necessary Python libraries (e.g., Streamlit, Pandas, Scikit-learn, Joblib, Plotly).
- Pre-trained models and datasets for each sector:
  - **scaler_hc.pkl**, **kmeans_model_hc.pkl**, **clustered_data_hc.csv**, **sector_model_coefficients_by_ticker_REPLACEMENT.csv**, etc.
- A CSV reference file: **Active_Companies.csv** containing currently active companies.

---

### Features

- 📈 Clustering based on sector-specific financial ratios.
- 🏢 Displays peer companies dynamically.
- 🧭 Interactive PCA cluster plots using Plotly.
- 💡 Expected return calculations via CAPM, FF3, and Carhart models.
- 🔮 Price forecasting based on returns and analyst forecasts.
- 🔄 Ready to scale with additional GICS sectors in the future.

---

### Note

This prototype currently supports **three sectors (GICS 25, 35, 45)** with tailored models. Future versions will expand to more industries.

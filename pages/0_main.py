import streamlit as st

st.title("Welcome to FinClusters App")

# Introduction Text
st.markdown("""
Welcome to the **Financial Ratio Cluster Finder** and **Return Forecasting** platform!

### 🎯 **Goals of FinClusters**
- Help investors and analysts **identify peer companies** using **financial ratio clustering**.
- Provide **expected return predictions** using:
  - Models that offer the highest predictive accuracy for each industry (CAPM, Fama-French 3-Factor, and Carhart 4-Factor).
  - Peer-based return analysis from financial cluster analysis.
  - Analyst forecast data from Yahoo Finance.
- **Forecast stock prices** based on different expected return assumptions.

---

### 🌟 **What FinClusters Can Do**
**1. Industry-Specific Peer Clustering**
   - Analyze a company's financial position relative to peers.
   - Uses pre-trained clustering models per industry.
   - Visualizes the company's **position in the financial space**.

**2. Expected Return Forecasting**
   - Provides model-based returns (CAPM, FF3, Carhart).
   - Compares to peer-based return ranges.
   - Integrates analyst projections from Yahoo Finance.

**3. Price Forecasting**
   - Projects future stock prices based on:
     - Model-based expected returns
     - Peer-based range
     - Analyst-based forecast

---

### 🔍 **Current Industries Available**
This prototype supports the following **GICS Sectors**:
- 🏥 **Healthcare** (GICS 35)
- 🛍️ **Consumer Discretionary** (GICS 25)
- 💻 **Information Technology** (GICS 45)

> 🚧 **More sectors will be added soon!** We're expanding to provide support for all GICS industries.

---

### 💡 **How to Use FinClusters**
1. Enter a **ticker symbol** in the sidebar.
2. The app detects the sector and applies the relevant **clustering model**.
3. Explore peer clusters, return forecasts, and price projections.

---

Feel free to explore and let us know your feedback!
""")

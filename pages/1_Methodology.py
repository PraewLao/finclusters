import streamlit as st

st.title("📚 Methodology")  
st.markdown("All data and training models in Colab notebooks used in this project can be accessed in [this shared folder](https://drive.google.com/drive/folders/1dxeOSDAX77fi-8cc2utdIVGbQpLE4pBj?usp=share_link).")

# --- Clustering Methodology ---
st.markdown("### Financial Ratio Clustering")
st.markdown("#### Overview")

st.markdown("""
We use **K-Means Clustering** to group companies based on similar **financial profiles**.  
The clustering models are **industry-specific**, with separate models trained for:
- Healthcare (GICS 35): The training model was developed in [this Colab notebook](https://drive.google.com/drive/folders/1uGNFtpK5DD30P3GPYlD-GmGnO6TvwGBd?usp=share_link).
- Consumer Discretionary (GICS 25): The training model was developed in [this Colab notebook](https://drive.google.com/drive/folders/1PWsaECx9pbb4ruzWR5-gOj2IYSFUcOJW?usp=share_link).
- Information Technology (GICS 45): The training model was developed in [this Colab notebook](https://drive.google.com/drive/folders/15NKTZJ-nmJHGjEi9op1NyURigUFiRsND?usp=share_link).

The goal is to identify companies with **comparable financial fundamentals** to aid in peer analysis, investment screening, and forecasting.
""")

# --- Financial Ratios Used ---
st.markdown("#### Financial Ratios Used")

st.markdown("""
**Healthcare (GICS 35):**
- ROA (Return on Assets)
- ROE (Return on Equity)
- ROA Volatility (3-Year Rolling Std Dev)
- ROE Volatility (3-Year Rolling Std Dev)
- R&D Expense / Sales
- Debt / Assets
- Market / Book Value
- Working Capital / Total Assets
- Retained Earnings / Total Assets

**Consumer Discretionary (GICS 25):**
- ROA (Return on Assets)
- ROE (Return on Equity)
- R&D Expense / Sales
- Debt / Assets
- Market / Book Value
- Working Capital / Total Assets
- Retained Earnings / Total Assets
- ROA Volatility
- ROE Volatility

**Information Technology (GICS 45):**
- ROA (Return on Assets)
- ROE (Return on Equity)
- ROA Volatility
- ROE Volatility
- R&D Expense / Sales
- SG&A Expense / Sales
- CapEx / Sales
- Debt / Assets
- Market / Book Value
- Working Capital / Total Assets
""")

# --- Equations ---
st.markdown("#### Key Financial Ratio Formulas")

st.latex(r"\text{ROA} = \frac{\text{Net Income}}{\text{Total Assets}}")
st.latex(r"\text{ROE} = \frac{\text{Net Income}}{\text{Common Equity}}")
st.latex(r"\text{Debt/Assets} = \frac{\text{Total Liabilities}}{\text{Total Assets}}")
st.latex(r"\text{Market/Book} = \frac{\text{Market Cap}}{\text{Common Equity}}")
st.latex(r"\text{R\&D/Sales} = \frac{\text{R\&D Expenses}}{\text{Sales}}")
st.latex(r"\text{SGA/Sales} = \frac{\text{SG\&A Expenses}}{\text{Sales}}")
st.latex(r"\text{CapEx/Sales} = \frac{\text{Capital Expenditures}}{\text{Sales}}")
st.latex(r"\text{Working Capital/Assets} = \frac{\text{Working Capital}}{\text{Total Assets}}")
st.latex(r"\text{Retained Earnings/Assets} = \frac{\text{Retained Earnings}}{\text{Total Assets}}")

st.markdown("""
Volatilities (ROA Volatility and ROE Volatility) are calculated as **3-year rolling standard deviations** of ROA and ROE, respectively.
""")

# --- Preprocessing ---
st.markdown("#### Data Preparation")

st.markdown("""
- Source: WRDS Compustat (Annual Fundamentals)
- Active companies between 2000 to 2023.
- Sectors filtered by GICS codes (25, 35, 45).
- Winsorization applied at 1st and 99th percentiles to reduce the impact of outliers.
- Financial ratios normalized using **StandardScaler** prior to clustering.
""")

# --- Clustering Algorithm ---
st.markdown("#### K-Means Clustering")

st.markdown("""
The **K-Means Algorithm** partitions companies into **k clusters** by minimizing the sum of squared distances between points and their assigned cluster centroids.

We determined the optimal number of clusters **(k)** per sector using the **Elbow Method**, which analyzes where additional clusters provide diminishing improvements in inertia (sum of squared distances).

Typical values:
- Healthcare: 6 clusters
- Consumer Discretionary: 7 clusters
- Information Technology: 5 clusters
""")

st.latex(r"\text{Inertia} = \sum_{i=1}^{n} || x_i - \mu_{c(i)} ||^2")

st.markdown("""
Where:
- \( x_i \) = Data point
- \( \mu_{c(i)} \) = Centroid of the assigned cluster
""")

# --- PCA for Visualization ---
st.markdown("#### PCA (Principal Component Analysis) for 2D Visualization")

st.markdown("""
After clustering, we reduce the dimensionality of the financial ratio space to **2 Principal Components** for visualization using **PCA**.
""")

st.latex(r"Z = XW")

st.markdown("""
Where:
- \( X \) = Original standardized features
- \( W \) = PCA loading matrix
- \( Z \) = Projected 2D representation

The scatter plot shows companies colored by their cluster label, and highlights the selected company's position among peers.
""")

st.markdown("---")

# --- Model-Based Expected Return Prediction ---
st.markdown("### Expected Return Prediction")

# --- Data Used to Train the Model ---
st.markdown("#### Data Used to Train the Model")

st.markdown("""
We use historical stock return and factor data covering **January 2000 to December 2024**.  
- **Stock returns** were gathered from CRSP.  
- **Fama-French 3 factors** and the **momentum factor** were sourced from WRDS, representing market, size, value, and momentum factors.

The dataset is split into training and testing sets based on a fixed date:
- **Training set**: January 2000 – December 2018 (~76% of the data)
- **Testing set**: January 2019 – December 2024 (~24% of the data)

This split ensures that the model is trained on historical periods and evaluated on more recent, unseen data.
""")

st.markdown("#### Regression Model")

st.markdown("""
We train and test predictive models using historical stock return data from 2000 to 2024.  
The models incorporate market, size, value, and momentum factors, evaluated using:
""")

# Equations
st.markdown("**CAPM:**")
st.latex(r"R_i - R_f = \alpha + \beta_{MKT}(R_{MKT} - R_f) + \epsilon")

st.markdown("**Fama-French 3-Factor:**")
st.latex(r"R_i - R_f = \alpha + \beta_{MKT}(R_{MKT} - R_f) + \beta_{SMB}SMB + \beta_{HML}HML + \epsilon")

st.markdown("**Carhart 4-Factor:**")
st.latex(r"R_i - R_f = \alpha + \beta_{MKT}(R_{MKT} - R_f) + \beta_{SMB}SMB + \beta_{HML}HML + \beta_{MOM}MOM + \epsilon")

# Explanation of Variables
st.markdown("""
Where:
- Ri = Return of the individual stock
- Rf = Risk-free rate
- RMKT = Return of the overall market
- βMKT = Sensitivity of stock return to the market return
- βSMB = Sensitivity to the size factor (Small minus Big)
- βHML = Sensitivity to the value factor (High minus Low book-to-market)
- βMOM = Sensitivity to the momentum factor
- ε = Idiosyncratic risk (firm-specific return variation unexplained by the factors)
""")

st.markdown("""
We evaluate model performance using RMSE and MAE, and select the best predictive model for each GICS sector:
- CAPM for Healthcare
- Fama-French 3-Factor for Consumer Discretionary
- CAPM for Information Technology

The full model training and testing workflow was developed in a Colab notebook, which can be accessed [here](https://drive.google.com/drive/folders/1phTcLUvwUc_gxbt229_L2Eqaoti3g4Qj?usp=sharing).
""")

st.markdown("""
To calculate and showcase the predicted expected return for a selected stock, the app selects the most precise model for each industry, retrieves the beta coefficients from the regression results, and pulls the default risk-free rate from Yahoo Finance in real-time, specifically using the 10-Year Treasury Yield, ticker symbol **`^TNX`**. If live data is unavailable, a fallback default rate of **4.0%** is applied to ensure continuity.

Users have the flexibility to manually adjust the risk-free rate if they believe an alternative assumption is more appropriate for their analysis.  
Upon changing the input, the app dynamically recalculates expected returns across all predictive models to reflect the updated assumptions.

Moreover, users can toggle between using historical market excess returns and forward-looking risk premium estimates sourced from [NYU Stern](https://pages.stern.nyu.edu/~adamodar/), providing additional flexibility in modeling expected returns.
""")

# --- Peer Estimation of Expected Return ---
st.markdown("#### Peer Expected Return Range")
st.markdown("""
The app calculates minimum and maximum expected returns among a company's peers using the sector's best-fit model.
""")

# --- Analyst Estimation of Expected Return ---
st.markdown("#### Analyst Estimation of Expected Return")
st.markdown("""
Using real-time forward P/E data from Yahoo Finance and assuming a 3% GDP growth rate, implied expected returns are computed using:
""")
st.latex(r"P/E = \frac{1}{r-g}")

st.markdown("""
Where:
- \( P/E \) = Forward Price-to-Earnings ratio from Yahoo Finance
- \( r \) = Implied expected return
- \( g \) = Assumed growth rate (set at 3%, proxied by long-term GDP growth)

Rearranging the equation to solve for \( r \):
""")
st.latex(r"r = \frac{1}{P/E} + g")

st.markdown("""
Thus, given the forward P/E and assuming a growth rate of 3%, we estimate the implied analyst expected return for the stock.
""")

st.markdown("---")

# --- Price Forecast Methodology ---
st.markdown("### Price Forecast")
st.markdown("""
The app projects potential future stock prices based on three forecasting methods.  
Each method leverages the expected returns estimated earlier and combines them with forward-looking earnings data retrieved from Yahoo Finance.  
This multi-approach framework provides users with a more comprehensive view of price potential under different assumptions.
""")

st.markdown("#### Model-Based Forecast")
st.markdown("""
Using the expected return derived from the best-fit capital pricing model (CAPM, Fama-French 3-Factor, or Carhart 4-Factor), we estimate the intrinsic value of the stock based on a simplified Gordon Growth framework.  
Specifically, if the company's forward EPS (Earnings Per Share) is available, and the model-implied expected return exceeds a 3% assumed terminal growth rate, the stock price is estimated as:
""")
st.latex(r"\text{Model-Based Price} = \frac{\text{Forward EPS}}{\text{Expected Return} - \text{Terminal Growth}}")
st.markdown("""
This approach anchors the valuation on fundamental earnings expectations adjusted for sector-specific risk-return profiles.
""")

st.markdown("#### Peer-Based Forecast Range")
st.markdown("""
Building on the financial peer cluster analysis, we also forecast a range of possible stock prices based on the minimum and maximum expected returns observed among a company's peers.  
If both the peer minimum and maximum expected returns exceed the 3% terminal growth assumption, peer-based price forecasts are calculated as:
""")
st.latex(r"\text{Peer Price Range} = \left[ \frac{\text{Forward EPS}}{\text{Peer Max Return} - \text{Terminal Growth}},\quad \frac{\text{Forward EPS}}{\text{Peer Min Return} - \text{Terminal Growth}} \right]")
st.markdown("""
This range offers a benchmark comparison, showing how a company's valuation may vary relative to similar companies' risk-return expectations.
""")

st.markdown("#### Analyst-Based Forecast")
st.markdown("""
Lastly, we incorporate market consensus by estimating a stock price based on forward P/E ratios provided by analysts on Yahoo Finance.  
The analyst forecast price is computed by simply multiplying the forward P/E by the forward EPS:
""")
st.latex(r"\text{Analyst Forecast Price} = \text{Forward P/E} \times \text{Forward EPS}")
st.markdown("""
This provides an additional external reference point, reflecting prevailing market expectations about the company’s valuation.
""")

import streamlit as st

st.title("📚 Methodology")  

# --- Cluster Analysis ---
st.markdown("### Cluster Analysis")
st.markdown("""
The app applies cluster analysis to group companies based on their financial characteristics.  
Each cluster represents companies with similar financial risk profiles.
""")

st.markdown("---")

# --- Model-Based Expected Return Prediction ---
st.markdown("### Expected Return Prediction")
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

""")

st.markdown("""
The app retrieves the default risk-free rate from Yahoo Finance in real-time, specifically using the 10-Year Treasury Yield, ticker symbol **`^TNX`**.  
If live data is unavailable, a fallback default rate of **4.0%** is applied to ensure continuity.

Users have the flexibility to manually adjust the risk-free rate if they believe an alternative assumption is more appropriate for their analysis.  
Upon changing the input, the app dynamically recalculates expected returns across all predictive models to reflect the updated assumptions.

Moreover, users can toggle between using **historical market excess returns** and **forward-looking risk premium estimates** sourced from [NYU Stern](https://pages.stern.nyu.edu/~adamodar/), providing additional flexibility in modeling expected returns.
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

# P/E Equation
st.latex(r"P/E = \frac{1}{r-g}")

# Where: section (LaTeX style line-by-line)
st.markdown("Where:")
st.latex(r"P/E \quad \text{= Forward Price-to-Earnings ratio from Yahoo Finance}")
st.latex(r"r \quad \text{= Implied expected return}")
st.latex(r"g \quad \text{= Assumed growth rate (set at 3%, proxied by long-term GDP growth)}")

st.markdown("""
Rearranging the equation to solve for \( r \):
""")

# Rearranged Equation
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

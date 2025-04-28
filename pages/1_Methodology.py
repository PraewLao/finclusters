import streamlit as st

st.title("📚 Methodology")  

# --- Cluster Analysis ---
st.markdown("### Cluster Analysis")
st.markdown("""
The app applies cluster analysis to group companies based on their financial characteristics.  
Each cluster represents companies with similar financial risk profiles.
""")

st.markdown("---")

# --- Expected Return Prediction ---
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

st.markdown("""
We evaluate model performance using RMSE and MAE, and select the best predictive model for each GICS sector:
- CAPM for Healthcare
- Fama-French 3-Factor for Consumer Discretionary
- CAPM for Information Technology

Users can toggle between using historical market returns or forward-looking risk premium estimates from [NYU Stern](https://pages.stern.nyu.edu/~adamodar/).
""")

st.markdown("#### Peer Expected Return Range")
st.markdown("""
The app calculates minimum and maximum expected returns among a company's peers using the sector's best-fit model.
""")

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
st.markdown("### Price Forecast Methodology")
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

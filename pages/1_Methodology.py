import streamlit as st

st.title("📚 Methodology")

st.markdown("""
# Methodology

### Cluster Analysis
The app applies cluster analysis to group companies based on their financial characteristics. Each cluster represents companies with similar financial risk profiles.

---
""")

st.markdown("### Expected Return Prediction")
st.markdown("#### Regression Model")

st.markdown("""
We train and test predictive models using historical stock return data from 2000 to 2024. The models incorporate market, size, value, and momentum factors, evaluated using:
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


st.markdown("### Peer Expected Return Range")
st.markdown("""
The app calculates minimum and maximum expected returns among a company's peers using the sector's best-fit model.
""")


st.markdown("### Analyst Estimation of Expected Return")
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

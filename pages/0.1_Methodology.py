import streamlit as st

st.title("📚 Methodology")

st.markdown("""
# Methodology

### Cluster Analysis
The app applies cluster analysis to group companies based on their financial characteristics. Each cluster represents companies with similar financial risk profiles.

---

### Expected Return Prediction

#### Regression Model
We train and test predictive models using historical stock return data from 2000 to 2024. The models incorporate market, size, value, and momentum factors, evaluated using:

- **CAPM**:  
  \( R_i - R_f = \alpha + \beta_{MKT} (R_{MKT} - R_f) + \epsilon \)

- **Fama-French 3-Factor**:  
  \( R_i - R_f = \alpha + \beta_{MKT} (R_{MKT} - R_f) + \beta_{SMB} SMB + \beta_{HML} HML + \epsilon \)

- **Carhart 4-Factor**:  
  \( R_i - R_f = \alpha + \beta_{MKT} (R_{MKT} - R_f) + \beta_{SMB} SMB + \beta_{HML} HML + \beta_{MOM} MOM + \epsilon \)

We evaluate model performance using RMSE and MAE, and select the best predictive model for each GICS sector:
- CAPM for Healthcare
- Fama-French 3-Factor for Consumer Discretionary
- CAPM for Information Technology

Users can toggle between using historical market returns or forward-looking risk premium estimates from [NYU Stern](https://pages.stern.nyu.edu/~adamodar/).

---

### Peer Expected Return Range
The app calculates minimum and maximum expected returns among a company's peers using the sector's best-fit model.

---

### Analyst Estimation of Expected Return
Using real-time forward P/E data from Yahoo Finance and assuming a 3% GDP growth rate, implied expected returns are computed using:

\[
r = \frac{1}{P/E} + g
\]
""")

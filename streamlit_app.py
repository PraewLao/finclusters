# The app structure is cloned from Professor Wysocki's Multipage Template and the team made adjustments for the FinClusters App
import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "pages/0_main.py",
    title="Welcome to FinClusters!",
    default=True
)
App_page_1 = st.Page(
    "pages/1_Methodology.py",
    title="Methodology"
)
App_page_2 = st.Page(
    "pages/2_Peer_Cluster.py",
    title="Step 1: Cluster Analysis"
)
App_page_3 = st.Page(
    "pages/3_Expected_Return.py",
    title="Step 2: Expected Returns"
)
App_page_4 = st.Page(
    "pages/4_Price_Forecast.py",
    title="Step 3: Price Forecast"
)

# **** Set up navigation with section headers ****
pg = st.navigation(
    {
        "Start Here:": [App_page_0, App_page_1],
        "Explore Analysis:": [App_page_2, App_page_3, App_page_4],
    }
)

# **** Sidebar Layout ****
with st.sidebar:
    st.markdown("### 🎯 Select a Company")
    ticker = st.text_input("Enter stock ticker", value=st.session_state.get("ticker", "")).upper().strip()
    st.session_state["ticker"] = ticker
    

# **** Execute the navigation code ****
pg.run()

# The app structure is cloned from Professor Wysocki's Multipage Template and the team made adjustments for the FinClusters App
import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "pages/0_main.py",
    title="Click here to select stock",
    default=True
)
App_page_1 = st.Page(
    "pages/1_Peer_Cluster.py",
    title="Step 1: Peers from cluster analysis"
)
App_page_2 = st.Page(
    "pages/2_Expected_Return.py",
    title="Step 2: Expected returns"
)
App_page_3 = st.Page(
    "pages/3_Price_Forecast.py",
    title="Step 3: Price forecast"
)

# **** Set up navigation with section headers ****
pg = st.navigation(
    {
        "Start Here:": [App_page_0],
        "Dashboard Options": [App_page_1, App_page_2, App_page_3],
    }
)

# **** Sidebar Layout ****
with st.sidebar:
    st.markdown("### 👉 Start here!")
    ticker = st.text_input("Enter stock ticker", value=st.session_state.get("ticker", "")).upper().strip()
    st.session_state["ticker"] = ticker

    st.markdown("---")
    st.markdown("### Sidebar Prompts:")

# **** Execute the navigation code ****
pg.run()

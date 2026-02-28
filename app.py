import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Revenue Optimization",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove all Streamlit padding
st.markdown("""
<style>
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TABLEAU DASHBOARD (FULL SCREEN)
# --------------------------------------------------

DASHBOARD_URL = "https://public.tableau.com/views/RevenueOptimizationPromotionImpactSimulator/RevenueOptimizationPromotionImpactSimulator"

st.components.v1.html(
    f"""
    <script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>

    <style>
        body {{
            margin: 0;
            padding: 0;
        }}

        tableau-viz {{
            width: 100vw !important;
            height: 100vh !important;
            display: block !important;
        }}
    </style>

    <tableau-viz
        src="{DASHBOARD_URL}"
        device="desktop"
        toolbar="bottom"
        hide-tabs>
    </tableau-viz>
    """,
    height=1000,
    scrolling=False,
)
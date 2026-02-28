import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Retail Revenue Optimization",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit container: full width + clean padding
st.markdown(
    """
    <style>
      .block-container {
        max-width: 100% !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
      }

      /* Optional: reduce top whitespace on mobile */
      @media (max-width: 768px) {
        .block-container {
          padding-left: 0.6rem !important;
          padding-right: 0.6rem !important;
          padding-top: 0.6rem !important;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Retail Revenue Optimization")

# -----------------------------
# TABLEAU DASHBOARD (RESPONSIVE)
# -----------------------------
DASHBOARD_URL = "https://public.tableau.com/views/RevenueOptimizationPromotionImpactSimulator/RevenueOptimizationPromotionImpactSimulator"

st.components.v1.html(
    f"""
    <script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>

    <style>
      .viz-wrap {{
        width: 100%;
        max-width: 100%;
      }}

      /* Responsive sizing: use viewport height minus Streamlit UI space */
      tableau-viz {{
        width: 100% !important;
        display: block !important;
        height: calc(100vh - 170px) !important;
        min-height: 650px !important;
      }}

      /* Tablets */
      @media (max-width: 1024px) {{
        tableau-viz {{
          height: calc(100vh - 150px) !important;
          min-height: 560px !important;
        }}
      }}

      /* Phones */
      @media (max-width: 768px) {{
        tableau-viz {{
          height: calc(100vh - 120px) !important;
          min-height: 500px !important;
        }}
      }}
    </style>

    <div class="viz-wrap">
      <tableau-viz
        src="{DASHBOARD_URL}"
        device="desktop"
        toolbar="bottom"
        hide-tabs>
      </tableau-viz>
    </div>
    """,
    height=900,
    scrolling=True,
)
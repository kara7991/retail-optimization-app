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

# -----------------------------
# DASHBOARD LIST
# -----------------------------
VIZZES = {
    "Revenue Optimization": "https://public.tableau.com/views/RevenueOptimizationPromotionImpactSimulator/RevenueOptimizationPromotionImpactSimulator",
    "FP-Growth (Main)": "https://public.tableau.com/views/fp_growth/fp_growth1",
    "FP-Growth (Advanced)": "https://public.tableau.com/views/fp_growth_2/fp_growth2",
    "FP-Growth (Synthesis)": "https://public.tableau.com/views/fp_growth_synthese/Synthesefp_growth",
}

def embed_tableau(viz_src: str):
    st.components.v1.html(
        f"""
        <script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>

        <style>
          .viz-wrap {{
            width: 100%;
            max-width: 100%;
          }}

          tableau-viz {{
            width: 100% !important;
            display: block !important;
            height: calc(100vh - 230px) !important; /* header + selector space */
            min-height: 650px !important;
          }}

          @media (max-width: 1024px) {{
            tableau-viz {{
              height: calc(100vh - 210px) !important;
              min-height: 560px !important;
            }}
          }}

          @media (max-width: 768px) {{
            tableau-viz {{
              height: calc(100vh - 190px) !important;
              min-height: 500px !important;
            }}
          }}
        </style>

        <div class="viz-wrap">
          <tableau-viz
            src="{viz_src}"
            device="desktop"
            toolbar="bottom"
            hide-tabs>
          </tableau-viz>
        </div>
        """,
        height=900,
        scrolling=True,
    )

# -----------------------------
# HEADER (BANDEAU)
# -----------------------------
st.markdown("## 📊 Retail Revenue Optimization")
st.caption("Choose a dashboard — responsive display on all screens.")

# Dashboard selector (the “bandeau” control you want)
selected = st.radio(
    "Select dashboard",
    options=list(VIZZES.keys()),
    index=0
)
embed_tableau(VIZZES[selected])

# -----------------------------
# SHOW DASHBOARD
# -----------------------------
embed_tableau(VIZZES[selected])
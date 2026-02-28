import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retail Revenue Optimization", layout="wide")

# ---------------- TABLEAU DASHBOARDS ----------------
VIZZES = {
    "Revenue Optimization": {
        "src": "https://public.tableau.com/views/RevenueOptimizationPromotionImpactSimulator/RevenueOptimizationPromotionImpactSimulator",
        "height": 860,
    },
    "FP-Growth (Main)": {
        "src": "https://public.tableau.com/views/fp_growth/fp_growth1",
        "height": 820,
    },
    "FP-Growth (Advanced)": {
        "src": "https://public.tableau.com/views/fp_growth_2/fp_growth2",
        "height": 820,
    },
    "FP-Growth (Synthesis)": {
        "src": "https://public.tableau.com/views/fp_growth_synthese/Synthesefp_growth",
        "height": 820,
    },
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
            height: calc(100vh - 200px) !important;
            min-height: 600px !important;
          }}

          @media (max-width: 768px) {{
            tableau-viz {{
              height: calc(100vh - 150px) !important;
              min-height: 500px !important;
            }}
          }}
        </style>

        <div class="viz-wrap">
          <tableau-viz
            src="{viz_src}"
            toolbar="bottom"
            hide-tabs>
          </tableau-viz>
        </div>
        """,
        height=900,
        scrolling=True,
    )

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboards", "Decision Layer"])

# ---------------- HOME ----------------
if page == "Home":
    st.title("🛒 Retail Revenue Optimization")
    st.markdown("### Business Question")
    st.markdown(
        "> **If we adopt these insights, how much money do we earn — and why?**"
    )

    st.markdown("### This tool combines:")
    st.markdown(
        """
- 📊 Tableau dashboards (exploration & insight)
- 🧠 Advanced FP-Growth (bundle strategy)
- 🧮 Python decision engine (ROI & profit impact)
"""
    )

# ---------------- DASHBOARDS ----------------
elif page == "Dashboards":
    st.title("📊 Interactive Dashboards")

    selected = st.selectbox("Select dashboard", list(VIZZES.keys()))
    embed_tableau(VIZZES[selected]["src"], VIZZES[selected]["height"])

# ---------------- DECISION LAYER ----------------
elif page == "Decision Layer":

    st.title("🧮 Promotion ROI Decision Engine")

    col1, col2, col3 = st.columns(3)

    with col1:
        base_revenue = st.number_input("Base Revenue (€)", value=150_000_000, step=1_000_000)
        margin = st.slider("Margin %", 0, 80, 30)

    with col2:
        discount = st.slider("Discount %", 0, 50, 10)
        uplift = st.slider("Demand Uplift %", -30, 100, 15)

    with col3:
        targeting_eff = st.slider("Targeting Efficiency %", 0, 100, 30)
        adoption = st.slider("Adoption Rate %", 0, 100, 30)

    m = margin / 100
    d = discount / 100
    u = uplift / 100
    te = targeting_eff / 100
    adopt = adoption / 100

    # Untargeted
    rev_u = base_revenue * (1 + u) * (1 - d)
    prof_u = rev_u * m

    # Targeted (optimized uplift + reduced discount waste)
    rev_t = base_revenue * (1 + u * (1 + te)) * (1 - d * (1 - te))
    prof_t = rev_t * m

    profit_delta = prof_t - prof_u
    profit_delta_adopted = profit_delta * adopt
    roi = profit_delta / (base_revenue * d + 1e-9)

    st.markdown("---")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Untargeted Profit (€)", f"{prof_u:,.0f}")
    k2.metric("Targeted Profit (€)", f"{prof_t:,.0f}")
    k3.metric("Profit Δ Adopted (€)", f"{profit_delta_adopted:,.0f}")
    k4.metric("ROI (proxy)", f"{roi:.2f}")

    if profit_delta_adopted <= 0:
        st.error("❌ Not profitable — reduce discount or improve targeting.")
    elif roi < 1:
        st.warning("⚠️ Profitable but weak ROI — optimize targeting.")
    else:
        st.success("🚀 Strong ROI — strategy recommended.")

    # Export scenario
    df = pd.DataFrame([{
        "base_revenue": base_revenue,
        "margin_pct": margin,
        "discount_pct": discount,
        "uplift_pct": uplift,
        "targeting_eff_pct": targeting_eff,
        "adoption_pct": adoption,
        "profit_delta_adopted": profit_delta_adopted,
        "roi": roi
    }])

    st.download_button(
        "Download Scenario (CSV)",
        df.to_csv(index=False),
        "scenario.csv",
        "text/csv"
    )
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Retail Revenue Optimization",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Tableau vizzes (Public)
# -----------------------------
VIZZES = {
    "Revenue Optimization & Promotion Impact Simulator": {
        "src": "https://public.tableau.com/views/RevenueOptimizationPromotionImpactSimulator/RevenueOptimizationPromotionImpactSimulator"
    },
    "FP-Growth (fp_growth)": {
        "src": "https://public.tableau.com/views/fp_growth/fp_growth1"
    },
    "FP-Growth (fp_growth_2)": {
        "src": "https://public.tableau.com/views/fp_growth_2/fp_growth2"
    },
    "FP-Growth Synthesis": {
        "src": "https://public.tableau.com/views/fp_growth_synthese/Synthesefp_growth"
    },
}

# -----------------------------
# Responsive Tableau Embed
# -----------------------------
def embed_tableau(viz_src: str, min_height: int = 650):
    st.components.v1.html(
        f"""
        <script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>

        <style>
          /* prend toute la largeur */
          .viz-wrap {{
            width: 100%;
            max-width: 100%;
          }}

          tableau-viz {{
            width: 100% !important;
            display: block !important;
            height: calc(100vh - 180px) !important;
            min-height: {min_height}px !important;
          }}

          /* important: évite un conteneur trop étroit */
          iframe {{
            width: 100% !important;
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
        height=950,
        scrolling=True,
    )

# -----------------------------
# Sidebar Navigation (NO HOME)
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboards", "Decision Layer"], index=0)

# -----------------------------
# Page: Dashboards
# -----------------------------
if page == "Dashboards":
    st.title("📊 Dashboards (Tableau)")
    st.caption("Choose a dashboard and explore insights. The visualization auto-adjusts to your screen.")

    selected = st.selectbox("Select a dashboard", list(VIZZES.keys()))
    embed_tableau(VIZZES[selected]["src"])

    st.divider()
    st.subheader("How to use (quick)")
    st.markdown(
        """
- Use the **filters** inside the dashboard to compare scenarios (discount %, uplift %, bundle effect).
- Focus on **profit & ROI** indicators, not only revenue.
- Then go to **Decision Layer** to quantify business impact with transparent assumptions.
        """
    )

# -----------------------------
# Page: Decision Layer
# -----------------------------
else:
    st.title("🧮 Decision Layer (Python) — Promotion ROI Engine")
    st.caption("A transparent calculation layer to quantify expected profit impact & ROI.")

    col1, col2, col3 = st.columns(3)

    with col1:
        base_revenue = st.number_input("Base Revenue (€)", min_value=0, value=150_000_000, step=1_000_000)
        margin = st.slider("Margin %", 0, 80, 30)

    with col2:
        discount = st.slider("Discount %", 0, 50, 10)
        uplift = st.slider("Demand Uplift %", -30, 100, 15)

    with col3:
        targeting_eff = st.slider("Targeting Efficiency %", 0, 100, 30)
        adoption = st.slider("Adoption Rate %", 0, 100, 30)

    # Normalize
    m = margin / 100
    d = discount / 100
    u = uplift / 100
    te = targeting_eff / 100
    a = adoption / 100

    # Baseline
    baseline_profit = base_revenue * m

    # Untargeted promotion (everyone gets discount)
    rev_u = base_revenue * (1 + u) * (1 - d)
    prof_u = rev_u * m
    delta_u = prof_u - baseline_profit

    # Targeted promotion (less discount waste + better uplift on targeted group)
    # Simple model:
    # - Only "adoption" part is affected
    # - Discount waste reduced by targeting efficiency (effective discount cost reduced)
    effective_discount = d * (1 - te)
    targeted_uplift = u * (1 + te)

    rev_t = base_revenue * ((1 - a) * 1 + a * (1 + targeted_uplift)) * (1 - effective_discount)
    prof_t = rev_t * m
    delta_t = prof_t - baseline_profit

    # ROI proxy: profit delta divided by discount "cost"
    discount_cost_u = base_revenue * d
    discount_cost_t = base_revenue * effective_discount

    roi_u = delta_u / (discount_cost_u + 1e-9)
    roi_t = delta_t / (discount_cost_t + 1e-9)

    st.divider()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Baseline Profit (€)", f"{baseline_profit:,.0f}")
    k2.metric("Profit Δ Untargeted (€)", f"{delta_u:,.0f}")
    k3.metric("Profit Δ Targeted (€)", f"{delta_t:,.0f}")
    k4.metric("ROI (Targeted) proxy", f"{roi_t:.2f}")

    st.divider()
    st.subheader("Recommendation")
    if delta_t > delta_u and delta_t > 0:
        st.success("✅ Targeted promotion is the best option under current assumptions (higher profit impact than untargeted).")
    elif delta_u > 0 and delta_u >= delta_t:
        st.warning("⚠ Untargeted promotion performs better (or targeted is not efficient enough).")
    else:
        st.error("❌ Promotion may destroy value under these assumptions. Reduce discount or improve targeting/uplift.")

    st.subheader("Notes (assumptions)")
    st.markdown(
        """
- This is a simplified financial model to **support decisions quickly**.
- Tableau dashboards remain the **exploration layer**; Python provides an **auditable decision layer**.
- Targeted promotions reduce discount waste (targeting efficiency) and increase uplift on the engaged group (adoption rate).
        """
    )
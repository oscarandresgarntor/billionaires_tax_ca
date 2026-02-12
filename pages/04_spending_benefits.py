"""
Spending Benefits page: Revenue spending impact analysis.
"""

import streamlit as st
import pandas as pd

from src.models.revenue_model import estimate_aggregate_revenue
from src.models.spending_model import compute_total_spending_impact
from src.data.baseline_data import TOTAL_COLLECTIVE_WEALTH_B, TOTAL_CA_BILLIONAIRES
from src.visualization.charts import spending_allocation_donut, spending_impact_sankey
from src.visualization.formatters import format_billions, format_number, format_pct

st.title("Spending Benefits")
st.markdown("""
How would the tax revenue be spent, and what would the economic and social
impact be? The initiative allocates 90% to healthcare, 5% to education,
and 5% to food assistance.
""")

# Sidebar controls
st.sidebar.header("Spending Parameters")

st.sidebar.markdown("**Fiscal Multipliers**")
hc_mult = st.sidebar.slider(
    "Healthcare Multiplier",
    min_value=0.8, max_value=2.5, value=1.5, step=0.1,
    help="Richmond Fed Medicaid estimate: 1.5x",
)

ed_mult = st.sidebar.slider(
    "Education Multiplier",
    min_value=0.5, max_value=2.0, value=1.2, step=0.1,
    help="CBO estimate: 1.2x",
)

food_mult = st.sidebar.slider(
    "Food Assistance Multiplier",
    min_value=1.0, max_value=2.5, value=1.7, step=0.1,
    help="USDA SNAP estimate: 1.7x (high MPC)",
)

spending_years = st.sidebar.slider(
    "Spending Period (years)",
    min_value=1, max_value=10, value=5, step=1,
    help="Years over which revenue is spent",
)

# Use baseline revenue for spending calculations
revenue = estimate_aggregate_revenue(
    total_wealth_b=TOTAL_COLLECTIVE_WEALTH_B,
    num_billionaires=TOTAL_CA_BILLIONAIRES,
)

spending = compute_total_spending_impact(
    net_revenue_b=revenue["net_revenue_b"],
    healthcare_multiplier=hc_mult,
    education_multiplier=ed_mult,
    food_multiplier=food_mult,
    spending_years=spending_years,
)

# Key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Net Revenue to Spend", format_billions(revenue["net_revenue_b"]))
with col2:
    st.metric("Total GDP Impact", format_billions(spending["total_gdp_impact_b"]))
with col3:
    st.metric("Weighted Avg. Multiplier", f"{spending['weighted_avg_multiplier']:.2f}x")

st.divider()

# Allocation donut + Sankey
col_donut, col_sankey = st.columns(2)

with col_donut:
    fig = spending_allocation_donut(spending["allocation"])
    st.plotly_chart(fig, use_container_width=True)

with col_sankey:
    fig = spending_impact_sankey(spending)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Healthcare impact
st.subheader("Healthcare Impact (90% of Revenue)")

hc = spending["healthcare"]
hc_cols = st.columns(4)
with hc_cols[0]:
    st.metric("Total Spending", format_billions(hc["total_spending_b"]))
with hc_cols[1]:
    st.metric("Annual Spending", format_billions(hc["annual_spending_b"]))
with hc_cols[2]:
    st.metric("Additional Enrollee-Years", format_number(hc["total_enrollee_years"]))
with hc_cols[3]:
    st.metric("Direct Jobs Created", format_number(hc["direct_jobs_created"]))

st.markdown(f"""
- **{format_number(hc['annual_additional_enrollees'])}** additional Medi-Cal enrollees per year
  ({hc['pct_of_uninsured_covered']:.1f}% of CA's {hc['context']['uninsured_m']:.1f}M uninsured)
- **{format_billions(hc['gdp_impact_b'])}** total GDP impact ({hc_mult}x multiplier)
- Context: Current Medi-Cal serves {hc['context']['current_enrollees_m']:.1f}M at
  {format_billions(hc['context']['current_medi_cal_spending_b'])}/year
""")

st.divider()

# Education impact
st.subheader("Education Impact (5% of Revenue)")

ed = spending["education"]
ed_cols = st.columns(4)
with ed_cols[0]:
    st.metric("Total Spending", format_billions(ed["total_spending_b"]))
with ed_cols[1]:
    st.metric("Annual Spending", format_billions(ed["annual_spending_b"]))
with ed_cols[2]:
    st.metric("Teacher Position-Years", format_number(ed["total_teacher_position_years"]))
with ed_cols[3]:
    st.metric("GDP Impact", format_billions(ed["gdp_impact_b"]))

st.markdown(f"""
- **{format_number(ed['annual_teacher_positions'])}** additional teacher positions per year
- Average teacher salary + benefits: ${ed['avg_teacher_salary']:,}
- **{format_billions(ed['gdp_impact_b'])}** total GDP impact ({ed_mult}x multiplier)
""")

st.divider()

# Food assistance impact
st.subheader("Food Assistance Impact (5% of Revenue)")

food = spending["food_assistance"]
food_cols = st.columns(4)
with food_cols[0]:
    st.metric("Total Spending", format_billions(food["total_spending_b"]))
with food_cols[1]:
    st.metric("Annual Spending", format_billions(food["annual_spending_b"]))
with food_cols[2]:
    st.metric("Household-Years Served", format_number(food["total_household_years"]))
with food_cols[3]:
    st.metric("GDP Impact", format_billions(food["gdp_impact_b"]))

st.markdown(f"""
- **{format_number(food['annual_households_served'])}** additional households served per year
  ({food['pct_food_insecure_served']:.1f}% of CA's {food['context']['food_insecure_households_m']:.1f}M food insecure)
- **{format_billions(food['gdp_impact_b'])}** total GDP impact ({food_mult}x multiplier)
- Context: Current CalFresh serves {food['context']['current_recipients_m']:.1f}M at
  ${food['context']['avg_monthly_benefit']}/month average
""")

with st.expander("Technical Details"):
    st.markdown(f"""
    **Fiscal Multiplier Formula**:
    ```
    GDP Impact = Spending × Multiplier
    ```

    **Multiplier Sources**:
    - Healthcare (1.5x): Richmond Fed Medicaid multiplier estimate
    - Education (1.2x): CBO education spending multiplier
    - Food Assistance (1.7x): USDA SNAP analysis (high MPC recipients)

    **Important Caveats**:
    - Multipliers assume normal economic conditions
    - Higher during recessions, lower during expansions
    - Long-term education returns (human capital) not captured in near-term multiplier
    - Healthcare jobs estimate assumes ~15,000 direct jobs per $1B

    **Weighted Average Multiplier**: {spending['weighted_avg_multiplier']:.3f}x
    (90% × {hc_mult} + 5% × {ed_mult} + 5% × {food_mult})
    """)

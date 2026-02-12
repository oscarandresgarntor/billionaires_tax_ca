"""
Cost-Benefit Analysis page: Integrated timeline and NPV.
"""

import streamlit as st
import pandas as pd

from src.models.cost_benefit_model import (
    compute_cost_benefit_timeline,
    sensitivity_analysis,
)
from src.models.scenarios import SCENARIOS, get_scenario_params, COMMON_PARAMS
from src.visualization.charts import (
    cost_benefit_timeline,
    cumulative_npv_chart,
    tornado_chart,
)
from src.visualization.formatters import format_billions, format_pct, format_ratio

st.title("Cost-Benefit Analysis")
st.markdown("""
Integrated analysis combining revenue, migration costs, and spending benefits
into a unified timeline with Net Present Value (NPV) calculations.
""")

# Sidebar controls
st.sidebar.header("Analysis Parameters")

scenario_key = st.sidebar.selectbox(
    "Pre-built Scenario",
    options=list(SCENARIOS.keys()),
    format_func=lambda k: f"{SCENARIOS[k]['name']} - {SCENARIOS[k]['description'][:40]}...",
    index=1,  # Default to baseline
)

discount_rate = st.sidebar.slider(
    "Discount Rate",
    min_value=0.01, max_value=0.07, value=0.03, step=0.005,
    format="%.1f%%",
    help="Rate for discounting future costs/benefits to present value",
)

horizon = st.sidebar.slider(
    "Analysis Horizon (years)",
    min_value=5, max_value=30, value=20, step=5,
)

# Get scenario params and override user selections
params = get_scenario_params(scenario_key)
params["discount_rate"] = discount_rate
params["horizon_years"] = horizon

# Compute
result = compute_cost_benefit_timeline(**params)
summary = result["summary"]

# Key metrics
st.subheader(f"Scenario: {SCENARIOS[scenario_key]['name']}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Net Revenue", format_billions(summary["net_revenue_b"]))
with col2:
    st.metric(
        f"{horizon}-Year NPV",
        format_billions(summary["npv_b"]),
        delta="Positive" if summary["npv_b"] > 0 else "Negative",
        delta_color="normal" if summary["npv_b"] > 0 else "inverse",
    )
with col3:
    st.metric("Benefit-Cost Ratio", format_ratio(summary["benefit_cost_ratio"]))
with col4:
    breakeven = summary.get("breakeven_year")
    st.metric(
        "Breakeven Year",
        str(breakeven) if breakeven else "Year 1",
    )

st.divider()

# Timeline charts
col_timeline, col_npv = st.columns(2)

with col_timeline:
    fig = cost_benefit_timeline(result["timeline"])
    st.plotly_chart(fig, use_container_width=True)

with col_npv:
    fig = cumulative_npv_chart(result["timeline"])
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Summary breakdown
st.subheader("Cost-Benefit Breakdown")

col_ben, col_cost = st.columns(2)

with col_ben:
    st.markdown("**Benefits**")
    st.markdown(f"- Total Benefits: {format_billions(summary['total_benefits_b'])}")
    st.markdown(f"- Net Revenue: {format_billions(summary['net_revenue_b'])}")
    st.markdown(f"- GDP Impact: {format_billions(result['spending']['total_gdp_impact_b'])}")
    st.markdown(f"- Weighted Multiplier: {result['spending']['weighted_multiplier']:.2f}x")

with col_cost:
    st.markdown("**Costs**")
    st.markdown(f"- Total Costs: {format_billions(summary['total_costs_b'])}")
    st.markdown(f"- Departures: {result['migration']['departures']['estimated_departures']:.1f}")
    st.markdown(f"- Annual Migration Cost: {format_billions(result['migration']['annual_cost_b'])}")
    st.markdown(f"- Elasticity: {result['migration']['departures']['elasticity']}")

st.divider()

# Sensitivity analysis
st.subheader("Sensitivity Analysis")
st.markdown("""
Which parameters have the biggest impact on NPV? The tornado diagram shows
the effect of varying each parameter between its low and high bounds.
""")

@st.cache_data
def run_sensitivity(base_params):
    return sensitivity_analysis(base_params)

sens_df = run_sensitivity(params)
fig = tornado_chart(sens_df)
st.plotly_chart(fig, use_container_width=True)

# Sensitivity table
st.dataframe(
    sens_df[["parameter", "low_value", "high_value", "low_npv_b", "high_npv_b", "swing_b"]].rename(
        columns={
            "parameter": "Parameter",
            "low_value": "Low Value",
            "high_value": "High Value",
            "low_npv_b": "Low NPV ($B)",
            "high_npv_b": "High NPV ($B)",
            "swing_b": "Swing ($B)",
        }
    ),
    hide_index=True,
    use_container_width=True,
)

# Year-by-year data
with st.expander("Year-by-Year Data"):
    display_cols = [
        "year", "revenue_collected_b", "gdp_benefit_b", "total_benefits_b",
        "total_costs_b", "net_benefit_b", "cumulative_npv_b",
    ]
    st.dataframe(
        result["timeline"][display_cols].rename(columns={
            "year": "Year",
            "revenue_collected_b": "Revenue ($B)",
            "gdp_benefit_b": "GDP Benefit ($B)",
            "total_benefits_b": "Total Benefits ($B)",
            "total_costs_b": "Total Costs ($B)",
            "net_benefit_b": "Net Benefit ($B)",
            "cumulative_npv_b": "Cumulative NPV ($B)",
        }),
        hide_index=True,
        use_container_width=True,
    )

with st.expander("Technical Details"):
    st.markdown(f"""
    **NPV Formula**:
    ```
    NPV = Σ (Net_Benefit_t / (1 + r)^t) for t = 0 to {horizon}
    ```
    Where r = {format_pct(discount_rate)} discount rate.

    **Benefit-Cost Ratio**: Total discounted benefits / Total discounted costs = {format_ratio(summary['benefit_cost_ratio'])}

    **Key Assumptions in This Scenario ({SCENARIOS[scenario_key]['name']})**:
    - Elasticity: {params['elasticity']}
    - Compliance: {format_pct(params['compliance_rate'])}
    - Admin Cost: ${params['admin_cost_m']}M
    - Healthcare Multiplier: {params['healthcare_multiplier']}x
    - Anti-avoidance Discount: {format_pct(params['anti_avoidance_discount'])}
    - Firm Effect Discount: {format_pct(params['firm_effect_discount'])}
    """)

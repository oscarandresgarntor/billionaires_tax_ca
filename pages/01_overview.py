"""
Overview page: Key findings and initiative summary.
"""

import streamlit as st
import pandas as pd

from src.data.baseline_data import (
    TOTAL_CA_BILLIONAIRES,
    TOTAL_COLLECTIVE_WEALTH_B,
    TAX_RATE,
    ALLOCATION,
    INDUSTRY_BREAKDOWN,
    get_baseline_summary,
)
from src.models.scenarios import SCENARIOS, get_scenario_params
from src.models.cost_benefit_model import compute_cost_benefit_timeline
from src.visualization.charts import scenario_comparison_bars, industry_breakdown_chart
from src.visualization.formatters import format_billions, format_pct

st.title("California 2026 Billionaire Tax Act")
st.subheader("Cost-Benefit Analysis Dashboard")

st.markdown("""
**Initiative 25-0024** proposes a one-time 5% excise tax on individuals with
net worth exceeding $1 billion. Filed by SEIU-UHW in October 2025 for the
November 2026 ballot, it would allocate 90% of revenue to healthcare,
with the remainder split between education and food assistance.
""")

# Key metrics
summary = get_baseline_summary()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("CA Billionaires", f"{summary['total_billionaires']}")
with col2:
    st.metric("Collective Wealth", format_billions(summary['total_wealth_b']))
with col3:
    st.metric("Tax Rate", format_pct(summary['tax_rate'], 0))
with col4:
    st.metric(
        "Est. Net Revenue (Baseline)",
        format_billions(summary['gross_revenue_estimate_b'] * 0.85 - 0.15),
    )

st.divider()

# Scenario comparison
st.subheader("Scenario Comparison")
st.markdown("""
The analysis models four scenarios with different assumptions about
billionaire migration, tax compliance, and spending multipliers.
""")

@st.cache_data
def compute_all_scenarios():
    results = {}
    for key in SCENARIOS:
        params = get_scenario_params(key)
        results[key] = compute_cost_benefit_timeline(**params)
    return results

scenarios_results = compute_all_scenarios()

col_chart, col_table = st.columns([2, 1])

with col_chart:
    fig = scenario_comparison_bars(scenarios_results)
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    rows = []
    for key, result in scenarios_results.items():
        s = SCENARIOS[key]
        rows.append({
            "Scenario": s["name"],
            "Net Revenue": format_billions(result["revenue"]["net_revenue_b"]),
            "Departures": f"{result['migration']['departures']['estimated_departures']:.0f}",
            "20-Yr NPV": format_billions(result["summary"]["npv_b"]),
            "BCR": f"{result['summary']['benefit_cost_ratio']:.1f}x",
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

st.divider()

# Industry breakdown
st.subheader("California Billionaires by Industry")
fig = industry_breakdown_chart(INDUSTRY_BREAKDOWN)
st.plotly_chart(fig, use_container_width=True)

# Revenue allocation
st.divider()
st.subheader("Revenue Allocation")

alloc_cols = st.columns(3)
with alloc_cols[0]:
    st.metric("Healthcare", format_pct(ALLOCATION["healthcare"], 0))
    st.caption("Medi-Cal expansion, community clinics, workforce")
with alloc_cols[1]:
    st.metric("Education", format_pct(ALLOCATION["education"], 0))
    st.caption("K-12 and higher education funding")
with alloc_cols[2]:
    st.metric("Food Assistance", format_pct(ALLOCATION["food_assistance"], 0))
    st.caption("CalFresh and food bank support")

with st.expander("Technical Details"):
    st.markdown("""
    **Data Sources**:
    - **Primary**: Forbes Real-Time Billionaires API (Feb 2026): 250 CA billionaires, $2.25T wealth
    - **Cross-reference**: UC Berkeley expert report (Dec 2025): 204 billionaires, $2.19T
    - CA Legislative Analyst's Office for administrative cost estimates

    Forbes data is used as the primary baseline because each entry is individually
    verifiable (top billionaires can be cross-checked against public stock holdings).
    The Berkeley report did not disclose its data sources. The ~46-person gap is
    likely due to date differences and 59 billionaires near the $1B threshold
    who frequently cross in/out with market movements.

    **Key Assumptions**:
    - The tax is ONE-TIME, not annual. Published migration elasticities are for annual taxes.
    - Anti-avoidance provisions (Jan 1, 2026 residency date) limit strategic departure.
    - All model parameters are adjustable in the Scenario Explorer.

    **Residency Determination**: As of January 1, 2026 (before ballot qualification),
    with a 25% minimum apportionment factor for partial residents.
    """)

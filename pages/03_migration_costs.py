"""
Migration & Costs page: Migration and economic cost analysis.
"""

import streamlit as st
import pandas as pd

from src.data.baseline_data import TOTAL_CA_BILLIONAIRES, TAX_RATE
from src.data.california_fiscal import AVG_BILLIONAIRE_INCOME_TAX_M
from src.models.migration_model import (
    estimate_departures,
    estimate_annual_income_tax_loss,
    estimate_firm_level_effects,
    estimate_vc_ecosystem_impact,
    compute_total_migration_costs,
)
from src.visualization.charts import migration_cost_area
from src.visualization.formatters import format_billions, format_pct, format_number

st.title("Migration & Economic Costs")
st.markdown("""
This page models billionaire departures from California and the ongoing
economic costs of migration: lost income tax, firm-level effects, and
VC ecosystem impacts.
""")

# Sidebar controls
st.sidebar.header("Migration Parameters")

elasticity = st.sidebar.slider(
    "Migration Elasticity",
    min_value=0.0, max_value=3.0, value=0.35, step=0.05,
    help="% change in billionaire population / % change in net-of-tax rate. "
         "Young 2016: 0.06, Moretti & Wilson 2019: 0.35, M&W 2017: 1.9",
)

one_time_adj = st.sidebar.checkbox(
    "Apply one-time tax adjustment",
    value=True,
    help="Convert annual elasticity to one-time equivalent (5% / 5 years = 1% annual)",
)

anti_avoidance = st.sidebar.slider(
    "Anti-Avoidance Discount",
    min_value=0.0, max_value=0.60, value=0.30, step=0.05,
    format="%.0f%%",
    help="Reduction in departures due to Jan 1, 2026 residency date and 25% min apportionment",
)

avg_income_tax = st.sidebar.slider(
    "Avg. Income Tax per Billionaire ($M/yr)",
    min_value=10, max_value=150, value=50, step=5,
    help="Average annual CA income tax paid per billionaire",
)

firm_discount = st.sidebar.slider(
    "Firm Effect CA Discount",
    min_value=0.0, max_value=0.90, value=0.50, step=0.05,
    format="%.0f%%",
    help="Discount on Swedish firm-level data for CA tech context",
)

horizon = st.sidebar.slider(
    "Analysis Horizon (years)",
    min_value=5, max_value=30, value=20, step=5,
)

# Compute departures
departures_result = estimate_departures(
    num_billionaires=TOTAL_CA_BILLIONAIRES,
    elasticity=elasticity,
    tax_rate=TAX_RATE,
    one_time_adjustment=one_time_adj,
    anti_avoidance_discount=anti_avoidance,
)

# Key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Estimated Departures",
        f"{departures_result['estimated_departures']:.1f}",
        delta=f"{departures_result['departure_rate']:.1%} of {TOTAL_CA_BILLIONAIRES}",
        delta_color="inverse",
    )
with col2:
    income_loss = estimate_annual_income_tax_loss(
        departures_result["estimated_departures"], avg_income_tax
    )
    st.metric(
        "Annual Income Tax Loss",
        format_billions(income_loss["annual_lost_income_tax_b"]),
        delta_color="inverse",
    )
with col3:
    firm_effects = estimate_firm_level_effects(
        departures_result["estimated_departures"],
        firm_effect_discount=firm_discount,
    )
    st.metric(
        "Annual Firm-Level Loss",
        format_billions(firm_effects["estimated_revenue_loss_b"]),
        delta_color="inverse",
    )

st.divider()

# Departure comparison across elasticities
st.subheader("Departure Estimates by Elasticity")

elasticity_scenarios = [
    ("Young 2016 (Millionaires)", 0.06),
    ("Moretti & Wilson 2019 (Ultra-wealthy)", 0.35),
    ("Conservative Upper Bound", 1.0),
    ("M&W 2017 (Star Scientists)", 1.9),
]

scenario_rows = []
for label, e in elasticity_scenarios:
    dep = estimate_departures(
        TOTAL_CA_BILLIONAIRES, e, TAX_RATE, one_time_adj, anti_avoidance
    )
    loss = estimate_annual_income_tax_loss(dep["estimated_departures"], avg_income_tax)
    scenario_rows.append({
        "Source": label,
        "Elasticity": e,
        "Raw Departures": f"{dep['raw_departures']:.1f}",
        "After Anti-Avoidance": f"{dep['estimated_departures']:.1f}",
        "Annual Tax Loss": format_billions(loss["annual_lost_income_tax_b"]),
    })

st.dataframe(pd.DataFrame(scenario_rows), hide_index=True, use_container_width=True)

st.divider()

# Migration cost timeline
st.subheader("Cumulative Migration Costs Over Time")

migration_costs = compute_total_migration_costs(
    num_billionaires=TOTAL_CA_BILLIONAIRES,
    elasticity=elasticity,
    tax_rate=TAX_RATE,
    one_time_adjustment=one_time_adj,
    anti_avoidance_discount=anti_avoidance,
    avg_income_tax_m=avg_income_tax,
    firm_effect_discount=firm_discount,
    horizon_years=horizon,
)

fig = migration_cost_area(migration_costs["timeline"])
st.plotly_chart(fig, use_container_width=True)

col_cost1, col_cost2 = st.columns(2)
with col_cost1:
    st.metric(
        f"Annual Total Cost",
        format_billions(migration_costs["annual_total_cost_b"]),
    )
with col_cost2:
    st.metric(
        f"Cumulative Cost ({horizon} years)",
        format_billions(migration_costs["cumulative_cost_b"]),
    )

# VC ecosystem impact
st.divider()
st.subheader("VC Ecosystem Impact")

vc = estimate_vc_ecosystem_impact(
    departures_result["estimated_departures"],
    TOTAL_CA_BILLIONAIRES,
)

vc_cols = st.columns(3)
with vc_cols[0]:
    st.metric("Billionaire VC Total", format_billions(vc["billionaire_vc_total_b"]))
with vc_cols[1]:
    st.metric("Lost VC (Annual)", format_billions(vc["lost_vc_annual_b"]))
with vc_cols[2]:
    st.metric("Economic Impact (3x)", format_billions(vc["total_economic_impact_b"]))

with st.expander("Technical Details"):
    st.markdown(f"""
    **Migration Elasticity Formula**:
    ```
    departures = N × elasticity × (effective_rate / (1 - effective_rate))
    ```
    Where `effective_rate = statutory_rate × 0.2` for one-time tax adjustment.

    **Current Parameters**:
    - Elasticity: {elasticity}
    - Effective annual rate: {departures_result['effective_annual_rate']:.4f}
    - % change in net-of-tax rate: {departures_result['pct_change_net_of_tax']:.4f}
    - Raw departures: {departures_result['raw_departures']:.1f}
    - Anti-avoidance discount: {format_pct(anti_avoidance)}
    - Final departures: {departures_result['estimated_departures']:.1f}

    **Key Assumption**: Published elasticities are for ANNUAL taxes. The one-time
    tax adjustment (÷5) is a major modeling assumption. Without this adjustment,
    departure estimates would be ~5x higher.

    **Firm-Level Effects** (from Munoz 2024, Swedish data):
    - Employment: {firm_effects['employment_effect_raw']:.0%} raw → {firm_effects['employment_effect_adjusted']:.1%} adjusted
    - Value Added: {firm_effects['value_added_effect_adjusted']:.1%} adjusted
    - CA discount: {format_pct(firm_discount)} (tech firms may be more resilient)

    **Sources**:
    - Young et al. 2016: Millionaire migration elasticity = 0.06
    - Moretti & Wilson 2019: Ultra-wealthy elasticity = 0.35
    - Moretti & Wilson 2017: Star scientists elasticity = 1.9
    - Munoz 2024: Swedish wealth tax firm-level effects
    """)

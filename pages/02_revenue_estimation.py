"""
Revenue Estimation page: Interactive revenue model exploration.
"""

import streamlit as st

from src.data.baseline_data import TOTAL_COLLECTIVE_WEALTH_B, TOTAL_CA_BILLIONAIRES
from src.data.billionaire_data import get_billionaire_data
from src.models.revenue_model import (
    estimate_aggregate_revenue,
    compute_collection_timeline,
)
from src.visualization.charts import (
    revenue_waterfall,
    collection_timeline,
    billionaire_distribution_histogram,
)
from src.visualization.formatters import format_billions, format_pct

st.title("Revenue Estimation")
st.markdown("""
Explore how gross wealth translates into net revenue, accounting for
exclusions, compliance rates, and administrative costs.
""")

# Sidebar controls
st.sidebar.header("Revenue Parameters")

tax_rate = st.sidebar.slider(
    "Tax Rate",
    min_value=0.01, max_value=0.10, value=0.05, step=0.005,
    format="%.1f%%",
    help="Statutory tax rate (initiative sets 5%)",
)

re_exclusion = st.sidebar.slider(
    "Real Estate Exclusion",
    min_value=0.0, max_value=0.30, value=0.10, step=0.01,
    format="%.0f%%",
    help="Fraction of wealth in real estate (excluded from tax base)",
)

pension_exclusion = st.sidebar.slider(
    "Pension/Retirement Exclusion",
    min_value=0.0, max_value=0.05, value=0.01, step=0.005,
    format="%.1f%%",
    help="Fraction in pension/retirement accounts (excluded)",
)

compliance = st.sidebar.slider(
    "Compliance Rate",
    min_value=0.50, max_value=1.0, value=0.85, step=0.05,
    format="%.0f%%",
    help="Expected fraction of owed tax actually collected",
)

admin_cost = st.sidebar.slider(
    "Admin Cost ($M)",
    min_value=15, max_value=500, value=150, step=5,
    help="Administrative cost in millions (LAO range: $15M-$300M)",
)

installment_pct = st.sidebar.slider(
    "Installment Election Rate",
    min_value=0.0, max_value=0.80, value=0.40, step=0.05,
    format="%.0f%%",
    help="Fraction of taxpayers choosing 5-year installment plan",
)

# Compute revenue
revenue = estimate_aggregate_revenue(
    total_wealth_b=TOTAL_COLLECTIVE_WEALTH_B,
    num_billionaires=TOTAL_CA_BILLIONAIRES,
    tax_rate=tax_rate,
    real_estate_exclusion=re_exclusion,
    pension_exclusion=pension_exclusion,
    compliance_rate=compliance,
    admin_cost_m=admin_cost,
)

# Key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Taxable Wealth", format_billions(revenue["taxable_wealth_b"]))
with col2:
    st.metric("Gross Tax", format_billions(revenue["gross_tax_b"]))
with col3:
    st.metric("Expected Collected", format_billions(revenue["expected_collected_b"]))
with col4:
    st.metric("Net Revenue", format_billions(revenue["net_revenue_b"]))

st.divider()

# Waterfall chart
col_wf, col_detail = st.columns([3, 1])

with col_wf:
    fig = revenue_waterfall(revenue)
    st.plotly_chart(fig, use_container_width=True)

with col_detail:
    st.markdown("**Revenue Breakdown**")
    st.markdown(f"- Gross Wealth: {format_billions(revenue['gross_wealth_b'])}")
    st.markdown(f"- Exclusions: -{format_billions(revenue['total_exclusions_b'])}")
    st.markdown(f"- Taxable Wealth: {format_billions(revenue['taxable_wealth_b'])}")
    st.markdown(f"- Gross Tax ({format_pct(tax_rate, 0)}): {format_billions(revenue['gross_tax_b'])}")
    st.markdown(f"- Non-compliance: -{format_billions(revenue['uncollected_b'])}")
    st.markdown(f"- Admin Costs: -{format_billions(revenue['admin_cost_b'])}")
    st.markdown(f"- **Net Revenue: {format_billions(revenue['net_revenue_b'])}**")

st.divider()

# Collection timeline
st.subheader("Collection Timeline")
st.markdown("""
Taxpayers can elect to pay in installments over 5 years (with interest).
This chart shows expected year-by-year revenue collection.
""")

timeline = compute_collection_timeline(
    net_revenue_b=revenue["net_revenue_b"],
    installment_pct=installment_pct,
)

fig = collection_timeline(timeline)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Billionaire distribution
st.subheader("Wealth Distribution")

df = get_billionaire_data()
fig = billionaire_distribution_histogram(df)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Technical Details"):
    st.markdown(f"""
    **Formulas**:
    - Taxable Wealth = Gross Wealth × (1 - RE Exclusion - Pension Exclusion)
    - Gross Tax = Taxable Wealth × Tax Rate (with phase-in for $1.0-1.1B)
    - Expected Collected = Gross Tax × Compliance Rate
    - Net Revenue = Expected Collected - Admin Costs

    **Phase-in**: Tax rate phases in linearly between $1.0B and $1.1B net worth.
    At $1.05B, effective rate is {format_pct(tax_rate/2, 1)}.

    **Installment Option**: Taxpayers can pay over 5 years at 5% annual interest.

    **Sources**:
    - Forbes Real-Time Billionaires API (Feb 2026): 250 billionaires, $2.25T wealth
    - Cross-reference: UC Berkeley report (Dec 2025): 204 billionaires, $2.19T
    - LAO analysis: Admin cost range $15M-$300M
    - IRS data: High-income compliance rates
    """)

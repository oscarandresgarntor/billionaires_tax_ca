"""
California 2026 Billionaire Tax Act: Cost-Benefit Analyzer

Interactive Streamlit dashboard for analyzing the proposed one-time 5%
excise tax on billionaires (Initiative 25-0024).
"""

import streamlit as st

st.set_page_config(
    page_title="CA Billionaire Tax Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigation
overview = st.Page("pages/01_overview.py", title="Overview", icon="📋", default=True)
revenue = st.Page("pages/02_revenue_estimation.py", title="Revenue Estimation", icon="💰")
migration = st.Page("pages/03_migration_costs.py", title="Migration & Costs", icon="🏃")
spending = st.Page("pages/04_spending_benefits.py", title="Spending Benefits", icon="🏥")
cost_benefit = st.Page("pages/05_cost_benefit.py", title="Cost-Benefit Analysis", icon="⚖️")
explorer = st.Page("pages/06_scenario_explorer.py", title="Scenario Explorer", icon="🔬")
methodology = st.Page("pages/07_methodology.py", title="Methodology", icon="📚")

pg = st.navigation([overview, revenue, migration, spending, cost_benefit, explorer, methodology])
pg.run()

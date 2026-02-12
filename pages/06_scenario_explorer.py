"""
Scenario Explorer page: Full parameter sandbox.
"""

import streamlit as st
import pandas as pd

from src.models.cost_benefit_model import compute_cost_benefit_timeline
from src.models.scenarios import SCENARIOS, get_scenario_params, COMMON_PARAMS
from src.visualization.charts import cost_benefit_timeline, cumulative_npv_chart
from src.visualization.formatters import format_billions, format_pct, format_ratio

st.title("Scenario Explorer")
st.markdown("""
Build and compare custom scenarios by adjusting all model parameters.
Compare up to 3 scenarios side by side.
""")

# Number of scenarios to compare
num_scenarios = st.radio(
    "Number of scenarios to compare",
    options=[1, 2, 3],
    index=0,
    horizontal=True,
)

def scenario_controls(col, label, default_key="baseline"):
    """Render scenario controls in a column and return params dict."""
    with col:
        st.subheader(label)

        preset = st.selectbox(
            "Start from preset",
            options=["custom"] + list(SCENARIOS.keys()),
            format_func=lambda k: k.title() if k != "custom" else "Custom",
            index=list(SCENARIOS.keys()).index(default_key) + 1,
            key=f"preset_{label}",
        )

        if preset != "custom":
            defaults = get_scenario_params(preset)
        else:
            defaults = get_scenario_params("baseline")

        st.markdown("**Revenue**")
        compliance = st.slider(
            "Compliance Rate", 0.50, 1.0, defaults["compliance_rate"], 0.05,
            format="%.0f%%", key=f"comp_{label}",
        )
        admin_cost = st.slider(
            "Admin Cost ($M)", 15, 500, int(defaults["admin_cost_m"]), 5,
            key=f"admin_{label}",
        )
        installment = st.slider(
            "Installment Rate", 0.0, 0.80, defaults["installment_pct"], 0.05,
            format="%.0f%%", key=f"inst_{label}",
        )

        st.markdown("**Migration**")
        elasticity = st.slider(
            "Migration Elasticity", 0.0, 3.0, defaults["elasticity"], 0.05,
            key=f"elast_{label}",
        )
        anti_avoid = st.slider(
            "Anti-Avoidance Discount", 0.0, 0.60, defaults["anti_avoidance_discount"], 0.05,
            format="%.0f%%", key=f"avoid_{label}",
        )
        firm_disc = st.slider(
            "Firm Effect Discount", 0.0, 0.90, defaults["firm_effect_discount"], 0.05,
            format="%.0f%%", key=f"firm_{label}",
        )

        st.markdown("**Spending Multipliers**")
        hc_mult = st.slider(
            "Healthcare", 0.8, 2.5, defaults["healthcare_multiplier"], 0.1,
            key=f"hc_{label}",
        )
        ed_mult = st.slider(
            "Education", 0.5, 2.0, defaults["education_multiplier"], 0.1,
            key=f"ed_{label}",
        )
        food_mult = st.slider(
            "Food Assistance", 1.0, 2.5, defaults["food_multiplier"], 0.1,
            key=f"food_{label}",
        )

        return {
            **COMMON_PARAMS,
            "compliance_rate": compliance,
            "admin_cost_m": admin_cost,
            "installment_pct": installment,
            "elasticity": elasticity,
            "anti_avoidance_discount": anti_avoid,
            "firm_effect_discount": firm_disc,
            "healthcare_multiplier": hc_mult,
            "education_multiplier": ed_mult,
            "food_multiplier": food_mult,
        }


# Create scenario columns
default_keys = ["baseline", "optimistic", "pessimistic"]
cols = st.columns(num_scenarios)

all_params = []
all_results = []

for i in range(num_scenarios):
    params = scenario_controls(cols[i], f"Scenario {i+1}", default_keys[i])
    all_params.append(params)

st.divider()

# Compute results
for params in all_params:
    result = compute_cost_benefit_timeline(**params)
    all_results.append(result)

# Comparison table
st.subheader("Results Comparison")

comparison_rows = []
for i, result in enumerate(all_results):
    s = result["summary"]
    comparison_rows.append({
        "Scenario": f"Scenario {i+1}",
        "Net Revenue": format_billions(s["net_revenue_b"]),
        "Departures": f"{result['migration']['departures']['estimated_departures']:.1f}",
        "Total Benefits": format_billions(s["total_benefits_b"]),
        "Total Costs": format_billions(s["total_costs_b"]),
        "Net Benefit": format_billions(s["net_benefit_b"]),
        "BCR": format_ratio(s["benefit_cost_ratio"]),
        "20-Year NPV": format_billions(s["npv_b"]),
    })

st.dataframe(pd.DataFrame(comparison_rows), hide_index=True, use_container_width=True)

# Timeline charts
st.divider()
st.subheader("Timeline Comparison")

chart_cols = st.columns(num_scenarios)
for i in range(num_scenarios):
    with chart_cols[i]:
        st.markdown(f"**Scenario {i+1}**")
        fig = cost_benefit_timeline(all_results[i]["timeline"])
        fig.update_layout(height=350, title=f"Scenario {i+1}")
        st.plotly_chart(fig, use_container_width=True)

# NPV charts
npv_cols = st.columns(num_scenarios)
for i in range(num_scenarios):
    with npv_cols[i]:
        fig = cumulative_npv_chart(all_results[i]["timeline"])
        fig.update_layout(height=350, title=f"NPV - Scenario {i+1}")
        st.plotly_chart(fig, use_container_width=True)

# CSV Export
st.divider()
st.subheader("Export Data")

for i, result in enumerate(all_results):
    csv = result["timeline"].to_csv(index=False)
    st.download_button(
        label=f"Download Scenario {i+1} Timeline (CSV)",
        data=csv,
        file_name=f"scenario_{i+1}_timeline.csv",
        mime="text/csv",
        key=f"download_{i}",
    )

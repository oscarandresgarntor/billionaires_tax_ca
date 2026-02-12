"""
Reusable Plotly chart builders for the billionaire tax dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# Consistent color palette
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "positive": "#2ecc71",
    "negative": "#e74c3c",
    "neutral": "#95a5a6",
    "healthcare": "#3498db",
    "education": "#9b59b6",
    "food": "#e67e22",
    "light_blue": "#aec7e8",
    "light_green": "#98df8a",
    "light_red": "#ff9896",
}

LAYOUT_DEFAULTS = dict(
    template="plotly_white",
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(l=60, r=30, t=50, b=50),
    height=450,
)


def revenue_waterfall(revenue: dict) -> go.Figure:
    """
    Create a waterfall chart showing gross wealth -> net revenue.
    """
    labels = [
        "Gross Wealth",
        "Exclusions",
        "Taxable Wealth",
        "Gross Tax (5%)",
        "Non-compliance",
        "Admin Costs",
        "Net Revenue",
    ]

    measures = ["absolute", "relative", "total", "absolute", "relative", "relative", "total"]

    values = [
        revenue["gross_wealth_b"],
        -revenue["total_exclusions_b"],
        0,  # Taxable subtotal
        revenue["gross_tax_b"],
        -revenue["uncollected_b"],
        -revenue["admin_cost_b"],
        0,  # Net revenue total
    ]

    # For waterfall, we need to set it up differently
    fig = go.Figure()

    # Build custom waterfall since Plotly's waterfall needs specific setup
    running = 0
    bar_data = []

    steps = [
        ("Gross Wealth", revenue["gross_wealth_b"], "total"),
        ("Exclusions", -revenue["total_exclusions_b"], "decrease"),
        ("Taxable Wealth", revenue["taxable_wealth_b"], "subtotal"),
        ("Gross Tax (5%)", revenue["gross_tax_b"], "total"),
        ("Non-compliance", -revenue["uncollected_b"], "decrease"),
        ("Admin Costs", -revenue["admin_cost_b"], "decrease"),
        ("Net Revenue", revenue["net_revenue_b"], "total"),
    ]

    fig = go.Figure(go.Waterfall(
        x=[s[0] for s in steps],
        measure=["absolute", "relative", "total", "absolute", "relative", "relative", "total"],
        y=[
            revenue["gross_wealth_b"],
            -revenue["total_exclusions_b"],
            0,
            revenue["gross_tax_b"],
            -revenue["uncollected_b"],
            -revenue["admin_cost_b"],
            0,
        ],
        connector={"line": {"color": "#ccc"}},
        increasing={"marker": {"color": COLORS["positive"]}},
        decreasing={"marker": {"color": COLORS["negative"]}},
        totals={"marker": {"color": COLORS["primary"]}},
        textposition="outside",
        text=[
            f"${revenue['gross_wealth_b']:,.0f}B",
            f"-${revenue['total_exclusions_b']:,.0f}B",
            f"${revenue['taxable_wealth_b']:,.0f}B",
            f"${revenue['gross_tax_b']:,.0f}B",
            f"-${revenue['uncollected_b']:,.1f}B",
            f"-${revenue['admin_cost_b']:,.1f}B",
            f"${revenue['net_revenue_b']:,.0f}B",
        ],
    ))

    fig.update_layout(
        title="Revenue Waterfall: Gross Wealth to Net Revenue",
        yaxis_title="Billions ($)",
        showlegend=False,
        **LAYOUT_DEFAULTS,
    )

    return fig


def collection_timeline(timeline_df: pd.DataFrame) -> go.Figure:
    """Create a stacked bar chart of year-by-year revenue collection."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=timeline_df["year"],
        y=timeline_df["lump_sum_b"],
        name="Lump Sum",
        marker_color=COLORS["primary"],
    ))
    fig.add_trace(go.Bar(
        x=timeline_df["year"],
        y=timeline_df["installment_b"],
        name="Installment",
        marker_color=COLORS["light_blue"],
    ))
    fig.add_trace(go.Bar(
        x=timeline_df["year"],
        y=timeline_df["interest_b"],
        name="Interest",
        marker_color=COLORS["secondary"],
    ))

    fig.update_layout(
        title="Revenue Collection Timeline",
        xaxis_title="Year",
        yaxis_title="Revenue Collected ($B)",
        barmode="stack",
        **LAYOUT_DEFAULTS,
    )

    return fig


def departure_scenarios_bar(scenarios: dict) -> go.Figure:
    """Bar chart comparing departure estimates across scenarios."""
    names = []
    departures = []
    colors = []

    for key, data in scenarios.items():
        names.append(data["name"])
        departures.append(data["departures"])
        colors.append(data.get("color", COLORS["primary"]))

    fig = go.Figure(go.Bar(
        x=names,
        y=departures,
        marker_color=colors,
        text=[f"{d:.0f}" for d in departures],
        textposition="outside",
    ))

    fig.update_layout(
        title="Estimated Billionaire Departures by Scenario",
        yaxis_title="Number of Departures",
        **LAYOUT_DEFAULTS,
    )

    return fig


def cost_benefit_timeline(timeline_df: pd.DataFrame) -> go.Figure:
    """Dual-axis timeline showing benefits, costs, and net benefit over time."""
    fig = go.Figure()

    # Benefits area
    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["total_benefits_b"],
        name="Benefits",
        fill="tozeroy",
        fillcolor="rgba(46, 204, 113, 0.3)",
        line=dict(color=COLORS["positive"], width=2),
    ))

    # Costs area
    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["total_costs_b"],
        name="Costs",
        fill="tozeroy",
        fillcolor="rgba(231, 76, 60, 0.3)",
        line=dict(color=COLORS["negative"], width=2),
    ))

    # Net benefit line
    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["net_benefit_b"],
        name="Net Benefit",
        line=dict(color=COLORS["primary"], width=3, dash="dash"),
    ))

    # Zero line
    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="Cost-Benefit Timeline",
        xaxis_title="Year",
        yaxis_title="Billions ($)",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        **LAYOUT_DEFAULTS,
    )

    return fig


def cumulative_npv_chart(timeline_df: pd.DataFrame) -> go.Figure:
    """Line chart showing cumulative NPV over time."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["cumulative_npv_b"],
        name="Cumulative NPV",
        fill="tozeroy",
        fillcolor="rgba(31, 119, 180, 0.2)",
        line=dict(color=COLORS["primary"], width=3),
    ))

    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="Cumulative Net Present Value",
        xaxis_title="Year",
        yaxis_title="Cumulative NPV ($B)",
        **LAYOUT_DEFAULTS,
    )

    return fig


def tornado_chart(sensitivity_df: pd.DataFrame) -> go.Figure:
    """Tornado diagram for sensitivity analysis."""
    fig = go.Figure()

    base_npv = sensitivity_df.iloc[0]["base_npv_b"]

    for _, row in sensitivity_df.iterrows():
        low_delta = row["low_npv_b"] - base_npv
        high_delta = row["high_npv_b"] - base_npv

        # Determine which is the "positive" direction
        left = min(low_delta, high_delta)
        right = max(low_delta, high_delta)

        param_label = row["parameter"].replace("_", " ").title()

        fig.add_trace(go.Bar(
            y=[param_label],
            x=[left],
            orientation="h",
            marker_color=COLORS["negative"],
            showlegend=False,
            base=0,
        ))
        fig.add_trace(go.Bar(
            y=[param_label],
            x=[right],
            orientation="h",
            marker_color=COLORS["positive"],
            showlegend=False,
            base=0,
        ))

    fig.add_vline(x=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="Sensitivity Analysis: Impact on NPV",
        xaxis_title="Change in NPV ($B) from Baseline",
        barmode="overlay",
        **{**LAYOUT_DEFAULTS, "height": 400},
    )

    return fig


def scenario_comparison_bars(scenarios_results: dict) -> go.Figure:
    """Side-by-side bar chart comparing key metrics across scenarios."""
    names = []
    net_revenues = []
    npvs = []
    colors = []

    for key, result in scenarios_results.items():
        from src.models.scenarios import SCENARIOS
        names.append(SCENARIOS[key]["name"])
        net_revenues.append(result["summary"]["net_benefit_b"])
        npvs.append(result["summary"]["npv_b"])
        colors.append(SCENARIOS[key]["color"])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names,
        y=npvs,
        name="20-Year NPV",
        marker_color=colors,
        text=[f"${v:,.0f}B" for v in npvs],
        textposition="outside",
    ))

    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="20-Year Net Present Value by Scenario",
        yaxis_title="NPV ($B)",
        **LAYOUT_DEFAULTS,
    )

    return fig


def spending_allocation_donut(allocation: dict) -> go.Figure:
    """Donut chart showing revenue allocation."""
    labels = ["Healthcare (90%)", "Education (5%)", "Food Assistance (5%)"]
    values = [
        allocation["healthcare_b"],
        allocation["education_b"],
        allocation["food_assistance_b"],
    ]
    colors_list = [COLORS["healthcare"], COLORS["education"], COLORS["food"]]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors_list,
        textinfo="label+value",
        texttemplate="%{label}<br>$%{value:.1f}B",
    ))

    fig.update_layout(
        title="Revenue Allocation",
        **{**LAYOUT_DEFAULTS, "height": 400},
    )

    return fig


def spending_impact_sankey(spending: dict) -> go.Figure:
    """Sankey diagram showing revenue flow from tax to impacts."""
    total = spending["allocation"]["total_b"]
    hc = spending["allocation"]["healthcare_b"]
    ed = spending["allocation"]["education_b"]
    food = spending["allocation"]["food_assistance_b"]

    hc_gdp = spending["healthcare"]["gdp_impact_b"]
    ed_gdp = spending["education"]["gdp_impact_b"]
    food_gdp = spending["food_assistance"]["gdp_impact_b"]

    labels = [
        "Net Revenue",        # 0
        "Healthcare",         # 1
        "Education",          # 2
        "Food Assistance",    # 3
        "HC GDP Impact",      # 4
        "Ed GDP Impact",      # 5
        "Food GDP Impact",    # 6
    ]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=[
                COLORS["primary"], COLORS["healthcare"], COLORS["education"],
                COLORS["food"], COLORS["light_blue"], "#c39bd3", "#f0b27a",
            ],
        ),
        link=dict(
            source=[0, 0, 0, 1, 2, 3],
            target=[1, 2, 3, 4, 5, 6],
            value=[hc, ed, food, hc_gdp, ed_gdp, food_gdp],
            color=[
                "rgba(52, 152, 219, 0.4)",
                "rgba(155, 89, 182, 0.4)",
                "rgba(230, 126, 34, 0.4)",
                "rgba(52, 152, 219, 0.2)",
                "rgba(155, 89, 182, 0.2)",
                "rgba(230, 126, 34, 0.2)",
            ],
        ),
    ))

    fig.update_layout(
        title="Revenue Flow: From Tax to Economic Impact",
        **{**LAYOUT_DEFAULTS, "height": 500},
    )

    return fig


def billionaire_distribution_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of billionaire wealth distribution with phase-out zone."""
    fig = go.Figure()

    # Main histogram
    fig.add_trace(go.Histogram(
        x=df["net_worth_b"],
        nbinsx=30,
        name="Billionaires",
        marker_color=COLORS["primary"],
        opacity=0.7,
    ))

    # Phase-out zone highlight
    fig.add_vrect(
        x0=1.0, x1=1.1,
        fillcolor="rgba(255, 165, 0, 0.2)",
        layer="below",
        line_width=0,
        annotation_text="Phase-in Zone",
        annotation_position="top",
    )

    fig.update_layout(
        title="Distribution of Billionaire Net Worth",
        xaxis_title="Net Worth ($B)",
        yaxis_title="Count",
        **LAYOUT_DEFAULTS,
    )

    return fig


def industry_breakdown_chart(breakdown: dict) -> go.Figure:
    """Horizontal bar chart of billionaires by industry."""
    industries = list(breakdown.keys())
    counts = [v["count"] for v in breakdown.values()]
    wealth = [v["total_wealth_b"] for v in breakdown.values()]

    # Sort by wealth
    sorted_idx = sorted(range(len(wealth)), key=lambda i: wealth[i])
    industries = [industries[i] for i in sorted_idx]
    counts = [counts[i] for i in sorted_idx]
    wealth = [wealth[i] for i in sorted_idx]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=industries,
        x=wealth,
        orientation="h",
        name="Total Wealth ($B)",
        marker_color=COLORS["primary"],
        text=[f"${w:,.0f}B ({c} people)" for w, c in zip(wealth, counts)],
        textposition="outside",
    ))

    fig.update_layout(
        title="California Billionaires by Industry",
        xaxis_title="Total Wealth ($B)",
        **{**LAYOUT_DEFAULTS, "height": 500},
    )

    return fig


def migration_cost_area(timeline_df: pd.DataFrame) -> go.Figure:
    """Stacked area chart of cumulative migration costs."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["income_tax_loss_b"],
        name="Income Tax Loss",
        stackgroup="costs",
        fillcolor="rgba(231, 76, 60, 0.4)",
        line=dict(color=COLORS["negative"]),
    ))
    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["firm_level_loss_b"],
        name="Firm-Level Loss",
        stackgroup="costs",
        fillcolor="rgba(230, 126, 34, 0.4)",
        line=dict(color=COLORS["secondary"]),
    ))
    fig.add_trace(go.Scatter(
        x=timeline_df["year"],
        y=timeline_df["vc_ecosystem_loss_b"],
        name="VC Ecosystem Loss",
        stackgroup="costs",
        fillcolor="rgba(149, 165, 166, 0.4)",
        line=dict(color=COLORS["neutral"]),
    ))

    fig.update_layout(
        title="Annual Migration-Related Economic Costs",
        xaxis_title="Year",
        yaxis_title="Annual Cost ($B)",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        **LAYOUT_DEFAULTS,
    )

    return fig

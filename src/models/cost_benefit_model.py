"""
Integrated cost-benefit model for the California Billionaire Tax Act.

Combines revenue, migration costs, and spending benefits into a
unified 20-year timeline with NPV analysis.
"""

import numpy as np
import pandas as pd

from src.models.revenue_model import estimate_aggregate_revenue, compute_collection_timeline
from src.models.migration_model import compute_total_migration_costs
from src.models.spending_model import compute_total_spending_impact


def compute_cost_benefit_timeline(
    # Revenue parameters
    total_wealth_b: float = 2190,
    num_billionaires: int = 204,
    tax_rate: float = 0.05,
    real_estate_exclusion: float = 0.10,
    pension_exclusion: float = 0.01,
    compliance_rate: float = 0.85,
    admin_cost_m: float = 150,
    installment_pct: float = 0.40,
    # Migration parameters
    elasticity: float = 0.35,
    one_time_adjustment: bool = True,
    anti_avoidance_discount: float = 0.30,
    avg_income_tax_m: float = 50,
    firm_effect_discount: float = 0.50,
    # Spending parameters
    healthcare_pct: float = 0.90,
    education_pct: float = 0.05,
    food_pct: float = 0.05,
    healthcare_multiplier: float = 1.5,
    education_multiplier: float = 1.2,
    food_multiplier: float = 1.7,
    spending_years: int = 5,
    # Timeline parameters
    horizon_years: int = 20,
    discount_rate: float = 0.03,
    start_year: int = 2027,
) -> dict:
    """
    Compute the full cost-benefit timeline.

    For each year:
    - Benefits = tax collected + spending GDP impact
    - Costs = admin + lost income tax + firm losses + VC losses
    - Net = Benefits - Costs
    - NPV = sum of discounted net benefits

    Returns:
        Dict with summary metrics and year-by-year timeline DataFrame.
    """
    # Step 1: Revenue estimation
    revenue = estimate_aggregate_revenue(
        total_wealth_b=total_wealth_b,
        num_billionaires=num_billionaires,
        tax_rate=tax_rate,
        real_estate_exclusion=real_estate_exclusion,
        pension_exclusion=pension_exclusion,
        compliance_rate=compliance_rate,
        admin_cost_m=admin_cost_m,
    )

    # Step 2: Collection timeline
    collection = compute_collection_timeline(
        net_revenue_b=revenue["net_revenue_b"],
        installment_pct=installment_pct,
        start_year=start_year,
    )

    # Step 3: Migration costs
    migration = compute_total_migration_costs(
        num_billionaires=num_billionaires,
        elasticity=elasticity,
        tax_rate=tax_rate,
        one_time_adjustment=one_time_adjustment,
        anti_avoidance_discount=anti_avoidance_discount,
        avg_income_tax_m=avg_income_tax_m,
        firm_effect_discount=firm_effect_discount,
        horizon_years=horizon_years,
    )

    # Step 4: Spending impact
    spending = compute_total_spending_impact(
        net_revenue_b=revenue["net_revenue_b"],
        healthcare_pct=healthcare_pct,
        education_pct=education_pct,
        food_pct=food_pct,
        healthcare_multiplier=healthcare_multiplier,
        education_multiplier=education_multiplier,
        food_multiplier=food_multiplier,
        spending_years=spending_years,
    )

    # Step 5: Build year-by-year timeline
    annual_gdp_impact = spending["total_gdp_impact_b"] / spending_years
    migration_timeline = migration["timeline"]

    timeline = []
    cumulative_npv = 0
    cumulative_net = 0

    for i in range(horizon_years):
        year = start_year + i

        # Revenue collected this year
        if i < len(collection):
            collected = collection.iloc[i]["total_b"]
        else:
            collected = 0

        # Spending impact (spread over spending_years)
        if i < spending_years:
            gdp_benefit = annual_gdp_impact
        else:
            gdp_benefit = 0

        total_benefits = collected + gdp_benefit

        # Costs
        if i < len(migration_timeline):
            migration_row = migration_timeline.iloc[i]
            income_tax_loss = migration_row["income_tax_loss_b"]
            firm_loss = migration_row["firm_level_loss_b"]
            vc_loss = migration_row["vc_ecosystem_loss_b"]
        else:
            # Costs persist beyond migration timeline
            annual_cost = migration["annual_total_cost_b"]
            income_tax_loss = migration["income_tax_loss"]["annual_lost_income_tax_b"]
            firm_loss = migration["firm_effects"]["estimated_revenue_loss_b"]
            vc_loss = migration["vc_impact"]["lost_vc_annual_b"]

        admin_cost = revenue["admin_cost_b"] if i == 0 else 0
        total_costs = income_tax_loss + firm_loss + vc_loss + admin_cost

        net_benefit = total_benefits - total_costs
        cumulative_net += net_benefit

        # Discount factor
        discount_factor = 1 / (1 + discount_rate) ** i
        discounted_net = net_benefit * discount_factor
        cumulative_npv += discounted_net

        timeline.append({
            "year": year,
            "year_offset": i,
            # Benefits
            "revenue_collected_b": round(collected, 3),
            "gdp_benefit_b": round(gdp_benefit, 3),
            "total_benefits_b": round(total_benefits, 3),
            # Costs
            "admin_cost_b": round(admin_cost, 3),
            "income_tax_loss_b": round(income_tax_loss, 3),
            "firm_loss_b": round(firm_loss, 3),
            "vc_loss_b": round(vc_loss, 3),
            "total_costs_b": round(total_costs, 3),
            # Net
            "net_benefit_b": round(net_benefit, 3),
            "cumulative_net_b": round(cumulative_net, 3),
            "discount_factor": round(discount_factor, 4),
            "discounted_net_b": round(discounted_net, 3),
            "cumulative_npv_b": round(cumulative_npv, 3),
        })

    timeline_df = pd.DataFrame(timeline)

    # Summary metrics
    total_benefits = timeline_df["total_benefits_b"].sum()
    total_costs = timeline_df["total_costs_b"].sum()
    bcr = total_benefits / total_costs if total_costs > 0 else float("inf")

    # Find breakeven year (where cumulative net turns positive)
    breakeven_year = None
    for _, row in timeline_df.iterrows():
        if row["cumulative_net_b"] > 0:
            breakeven_year = row["year"]
            break

    return {
        "revenue": revenue,
        "migration": {
            "departures": migration["departures"],
            "annual_cost_b": migration["annual_total_cost_b"],
        },
        "spending": {
            "total_gdp_impact_b": spending["total_gdp_impact_b"],
            "weighted_multiplier": spending["weighted_avg_multiplier"],
        },
        "summary": {
            "net_revenue_b": revenue["net_revenue_b"],
            "total_benefits_b": round(total_benefits, 2),
            "total_costs_b": round(total_costs, 2),
            "net_benefit_b": round(total_benefits - total_costs, 2),
            "benefit_cost_ratio": round(bcr, 2),
            "npv_b": round(cumulative_npv, 2),
            "breakeven_year": breakeven_year,
            "horizon_years": horizon_years,
            "discount_rate": discount_rate,
        },
        "timeline": timeline_df,
    }


def sensitivity_analysis(
    base_params: dict,
    param_ranges: dict = None,
) -> pd.DataFrame:
    """
    Run tornado-style sensitivity analysis.

    Varies each parameter independently between low and high values
    while holding others at baseline.

    Args:
        base_params: Baseline parameter dict for compute_cost_benefit_timeline.
        param_ranges: Dict of {param_name: (low, high)} to test.

    Returns:
        DataFrame with param, low_value, high_value, low_npv, high_npv, swing.
    """
    if param_ranges is None:
        param_ranges = {
            "elasticity": (0.06, 1.0),
            "compliance_rate": (0.70, 0.95),
            "admin_cost_m": (15, 300),
            "healthcare_multiplier": (1.2, 1.8),
            "anti_avoidance_discount": (0.10, 0.50),
            "firm_effect_discount": (0.25, 0.75),
            "discount_rate": (0.01, 0.05),
            "installment_pct": (0.20, 0.60),
        }

    # Baseline NPV
    base_result = compute_cost_benefit_timeline(**base_params)
    base_npv = base_result["summary"]["npv_b"]

    results = []
    for param, (low, high) in param_ranges.items():
        # Low scenario
        low_params = {**base_params, param: low}
        low_result = compute_cost_benefit_timeline(**low_params)
        low_npv = low_result["summary"]["npv_b"]

        # High scenario
        high_params = {**base_params, param: high}
        high_result = compute_cost_benefit_timeline(**high_params)
        high_npv = high_result["summary"]["npv_b"]

        results.append({
            "parameter": param,
            "low_value": low,
            "high_value": high,
            "low_npv_b": low_npv,
            "high_npv_b": high_npv,
            "base_npv_b": base_npv,
            "swing_b": abs(high_npv - low_npv),
        })

    return pd.DataFrame(results).sort_values("swing_b", ascending=False)

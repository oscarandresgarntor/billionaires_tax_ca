"""
Migration and economic cost model for the California Billionaire Tax Act.

Estimates billionaire departures and the ongoing economic costs of migration,
including lost income tax revenue, firm-level effects, and VC ecosystem impacts.
"""

import numpy as np
import pandas as pd

from src.data.baseline_data import (
    TOTAL_CA_BILLIONAIRES,
    TOTAL_COLLECTIVE_WEALTH_B,
    TAX_RATE,
    CA_ANNUAL_VC_INVESTMENT_B,
    BILLIONAIRE_SHARE_OF_VC,
)
from src.data.california_fiscal import (
    AVG_BILLIONAIRE_INCOME_TAX_M,
)


# One-time to annual tax rate conversion factor
# 5% one-time tax spread over 5 years ≈ 1% effective annual rate
ONE_TIME_TO_ANNUAL_FACTOR = 0.2  # 1/5


def estimate_departures(
    num_billionaires: int = TOTAL_CA_BILLIONAIRES,
    elasticity: float = 0.35,
    tax_rate: float = TAX_RATE,
    one_time_adjustment: bool = True,
    anti_avoidance_discount: float = 0.30,
) -> dict:
    """
    Estimate the number of billionaire departures.

    Uses migration elasticity from published literature, adjusted for:
    1. One-time vs annual tax nature
    2. Anti-avoidance provisions (Jan 1 2026 residency date, 25% min apportionment)

    Elasticity formula:
        departures = N * elasticity * (tax_rate / (1 - tax_rate))

    For one-time tax, we adjust the effective rate:
        effective_annual_rate = tax_rate * ONE_TIME_TO_ANNUAL_FACTOR

    Args:
        num_billionaires: Number of CA billionaires.
        elasticity: Migration elasticity (% pop change / % net-of-tax change).
        tax_rate: Statutory one-time tax rate.
        one_time_adjustment: Whether to apply the one-time to annual conversion.
        anti_avoidance_discount: Fraction reduction due to anti-avoidance provisions.

    Returns:
        Dict with departure estimates and methodology details.
    """
    if one_time_adjustment:
        effective_rate = tax_rate * ONE_TIME_TO_ANNUAL_FACTOR
    else:
        effective_rate = tax_rate

    # Compute the net-of-tax rate change
    # For a tax rate t, the net-of-tax rate is (1-t)
    # The % change in net-of-tax rate is t / (1-t)
    pct_change_net_of_tax = effective_rate / (1 - effective_rate)

    # Raw departures
    raw_departures = num_billionaires * elasticity * pct_change_net_of_tax

    # Apply anti-avoidance discount
    effective_departures = raw_departures * (1 - anti_avoidance_discount)

    # Clamp between 0 and total
    effective_departures = max(0, min(effective_departures, num_billionaires))

    return {
        "num_billionaires": num_billionaires,
        "elasticity": elasticity,
        "statutory_rate": tax_rate,
        "effective_annual_rate": round(effective_rate, 4),
        "one_time_adjusted": one_time_adjustment,
        "pct_change_net_of_tax": round(pct_change_net_of_tax, 4),
        "raw_departures": round(raw_departures, 1),
        "anti_avoidance_discount": anti_avoidance_discount,
        "estimated_departures": round(effective_departures, 1),
        "departure_rate": round(effective_departures / num_billionaires, 4),
    }


def estimate_annual_income_tax_loss(
    departures: float,
    avg_income_tax_m: float = AVG_BILLIONAIRE_INCOME_TAX_M,
) -> dict:
    """
    Estimate annual lost CA income tax from billionaire departures.

    Args:
        departures: Number of departing billionaires.
        avg_income_tax_m: Average annual CA income tax per billionaire ($M).

    Returns:
        Dict with annual and cumulative loss estimates.
    """
    annual_loss_m = departures * avg_income_tax_m
    annual_loss_b = annual_loss_m / 1000

    return {
        "departures": departures,
        "avg_income_tax_per_billionaire_m": avg_income_tax_m,
        "annual_lost_income_tax_m": round(annual_loss_m, 1),
        "annual_lost_income_tax_b": round(annual_loss_b, 3),
    }


def estimate_firm_level_effects(
    departures: float,
    avg_wealth_b: float = TOTAL_COLLECTIVE_WEALTH_B / TOTAL_CA_BILLIONAIRES,
    employment_effect: float = -0.33,
    value_added_effect: float = -0.34,
    tax_payment_effect: float = -0.50,
    firm_effect_discount: float = 0.50,
) -> dict:
    """
    Estimate firm-level effects of billionaire departures.

    Based on Swedish wealth tax data (Munoz 2024) showing that billionaire
    departures lead to significant firm-level effects. Applied with a discount
    because CA tech firms may be more resilient than Swedish firms.

    Args:
        departures: Number of departing billionaires.
        avg_wealth_b: Average wealth per billionaire.
        employment_effect: % change in employment (negative = loss).
        value_added_effect: % change in value added.
        tax_payment_effect: % change in corporate tax payments.
        firm_effect_discount: Discount for CA vs Sweden context.

    Returns:
        Dict with firm-level economic impact estimates.
    """
    # Estimate average firm revenue per billionaire (rough: 5% of wealth)
    avg_firm_revenue_b = avg_wealth_b * 0.05

    total_affected_revenue_b = departures * avg_firm_revenue_b
    effective_employment_loss = employment_effect * (1 - firm_effect_discount)
    effective_va_loss = value_added_effect * (1 - firm_effect_discount)
    effective_tax_loss = tax_payment_effect * (1 - firm_effect_discount)

    return {
        "departures": departures,
        "avg_firm_revenue_b": round(avg_firm_revenue_b, 2),
        "total_affected_revenue_b": round(total_affected_revenue_b, 2),
        "employment_effect_raw": employment_effect,
        "employment_effect_adjusted": round(effective_employment_loss, 3),
        "value_added_effect_adjusted": round(effective_va_loss, 3),
        "tax_payment_effect_adjusted": round(effective_tax_loss, 3),
        "firm_effect_discount": firm_effect_discount,
        "estimated_revenue_loss_b": round(
            total_affected_revenue_b * abs(effective_va_loss), 3
        ),
    }


def estimate_vc_ecosystem_impact(
    departures: float,
    num_billionaires: int = TOTAL_CA_BILLIONAIRES,
    annual_vc_b: float = CA_ANNUAL_VC_INVESTMENT_B,
    billionaire_vc_share: float = BILLIONAIRE_SHARE_OF_VC,
    vc_multiplier: float = 3.0,
) -> dict:
    """
    Estimate impact on California's VC ecosystem from departures.

    Args:
        departures: Number of departing billionaires.
        num_billionaires: Total CA billionaires.
        annual_vc_b: Total annual CA VC investment.
        billionaire_vc_share: Share of VC from billionaires.
        vc_multiplier: Economic multiplier on VC investment.

    Returns:
        Dict with VC ecosystem impact estimates.
    """
    departure_rate = departures / num_billionaires if num_billionaires > 0 else 0
    billionaire_vc_total_b = annual_vc_b * billionaire_vc_share
    lost_vc_b = billionaire_vc_total_b * departure_rate
    economic_impact_b = lost_vc_b * vc_multiplier

    return {
        "departure_rate": round(departure_rate, 4),
        "billionaire_vc_total_b": round(billionaire_vc_total_b, 2),
        "lost_vc_annual_b": round(lost_vc_b, 2),
        "vc_multiplier": vc_multiplier,
        "total_economic_impact_b": round(economic_impact_b, 2),
    }


def compute_total_migration_costs(
    num_billionaires: int = TOTAL_CA_BILLIONAIRES,
    elasticity: float = 0.35,
    tax_rate: float = TAX_RATE,
    one_time_adjustment: bool = True,
    anti_avoidance_discount: float = 0.30,
    avg_income_tax_m: float = AVG_BILLIONAIRE_INCOME_TAX_M,
    firm_effect_discount: float = 0.50,
    horizon_years: int = 20,
) -> dict:
    """
    Compute total migration costs over a given time horizon.

    Integrates departure estimates, income tax losses, firm effects,
    and VC ecosystem impacts into annual and cumulative totals.

    Returns:
        Dict with all component costs and a year-by-year timeline.
    """
    departures_result = estimate_departures(
        num_billionaires, elasticity, tax_rate,
        one_time_adjustment, anti_avoidance_discount
    )
    departures = departures_result["estimated_departures"]

    income_tax_loss = estimate_annual_income_tax_loss(departures, avg_income_tax_m)
    firm_effects = estimate_firm_level_effects(
        departures, firm_effect_discount=firm_effect_discount
    )
    vc_impact = estimate_vc_ecosystem_impact(departures, num_billionaires)

    # Build annual timeline
    annual_income_tax_loss_b = income_tax_loss["annual_lost_income_tax_b"]
    annual_firm_loss_b = firm_effects["estimated_revenue_loss_b"]
    annual_vc_loss_b = vc_impact["lost_vc_annual_b"]
    annual_total_loss_b = annual_income_tax_loss_b + annual_firm_loss_b + annual_vc_loss_b

    timeline = []
    cumulative = 0

    for year_offset in range(horizon_years):
        year = 2027 + year_offset
        # Assume departures happen in year 1, costs persist
        if year_offset == 0:
            year_loss = annual_total_loss_b * 0.5  # Partial first year
        else:
            year_loss = annual_total_loss_b

        cumulative += year_loss
        timeline.append({
            "year": year,
            "income_tax_loss_b": round(
                annual_income_tax_loss_b * (0.5 if year_offset == 0 else 1), 3
            ),
            "firm_level_loss_b": round(
                annual_firm_loss_b * (0.5 if year_offset == 0 else 1), 3
            ),
            "vc_ecosystem_loss_b": round(
                annual_vc_loss_b * (0.5 if year_offset == 0 else 1), 3
            ),
            "total_loss_b": round(year_loss, 3),
            "cumulative_loss_b": round(cumulative, 3),
        })

    return {
        "departures": departures_result,
        "income_tax_loss": income_tax_loss,
        "firm_effects": firm_effects,
        "vc_impact": vc_impact,
        "annual_total_cost_b": round(annual_total_loss_b, 3),
        "cumulative_cost_b": round(cumulative, 3),
        "timeline": pd.DataFrame(timeline),
    }

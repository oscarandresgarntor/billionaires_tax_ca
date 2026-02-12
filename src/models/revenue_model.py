"""
Revenue estimation model for the California Billionaire Tax Act.

Estimates gross and net one-time tax revenue, accounting for exclusions,
compliance rates, administrative costs, and collection timeline.
"""

import numpy as np
import pandas as pd

from src.data.baseline_data import (
    ADMIN_COST_MID_M,
    INSTALLMENT_YEARS,
    PHASE_IN_CEILING_B,
    PHASE_IN_FLOOR_B,
    TAX_RATE,
    TOTAL_COLLECTIVE_WEALTH_B,
    TOTAL_EXCLUSION_PCT,
)


def compute_effective_tax_rate(net_worth_b: float, tax_rate: float = TAX_RATE) -> float:
    """
    Compute the effective tax rate for a given net worth, applying phase-in.

    The tax phases in linearly between $1.0B and $1.1B:
    - Below $1.0B: 0%
    - $1.0B to $1.1B: linear ramp from 0% to tax_rate
    - Above $1.1B: full tax_rate

    Args:
        net_worth_b: Net worth in billions.
        tax_rate: Statutory tax rate (default 5%).

    Returns:
        Effective tax rate (0 to tax_rate).
    """
    if net_worth_b <= PHASE_IN_FLOOR_B:
        return 0.0
    elif net_worth_b >= PHASE_IN_CEILING_B:
        return tax_rate
    else:
        # Linear phase-in
        fraction = (net_worth_b - PHASE_IN_FLOOR_B) / (PHASE_IN_CEILING_B - PHASE_IN_FLOOR_B)
        return tax_rate * fraction


def compute_individual_tax(
    net_worth_b: float,
    tax_rate: float = TAX_RATE,
    real_estate_exclusion: float = 0.10,
    pension_exclusion: float = 0.01,
) -> dict:
    """
    Compute tax for a single billionaire.

    Args:
        net_worth_b: Gross net worth in billions.
        tax_rate: Statutory tax rate.
        real_estate_exclusion: Fraction of wealth in real estate (excluded).
        pension_exclusion: Fraction in pension/retirement (excluded).

    Returns:
        Dict with gross_worth, exclusions, taxable_wealth, effective_rate, tax_owed.
    """
    total_exclusion = real_estate_exclusion + pension_exclusion
    taxable_wealth = net_worth_b * (1 - total_exclusion)
    effective_rate = compute_effective_tax_rate(net_worth_b, tax_rate)
    tax_owed = taxable_wealth * effective_rate

    return {
        "gross_worth_b": net_worth_b,
        "exclusion_pct": total_exclusion,
        "exclusion_amount_b": net_worth_b * total_exclusion,
        "taxable_wealth_b": taxable_wealth,
        "effective_rate": effective_rate,
        "tax_owed_b": tax_owed,
    }


def estimate_aggregate_revenue(
    billionaire_df: pd.DataFrame = None,
    total_wealth_b: float = None,
    num_billionaires: int = None,
    tax_rate: float = TAX_RATE,
    real_estate_exclusion: float = 0.10,
    pension_exclusion: float = 0.01,
    compliance_rate: float = 0.85,
    admin_cost_m: float = ADMIN_COST_MID_M,
) -> dict:
    """
    Estimate aggregate revenue from the billionaire tax.

    Can work from either a DataFrame of individual billionaires or
    aggregate totals (for quick estimation).

    Returns:
        Dict with detailed revenue breakdown.
    """
    total_exclusion = real_estate_exclusion + pension_exclusion

    if billionaire_df is not None and len(billionaire_df) > 0:
        # Individual-level calculation
        results = []
        for _, row in billionaire_df.iterrows():
            re_excl = row.get("estimated_re_pct", real_estate_exclusion)
            result = compute_individual_tax(
                row["net_worth_b"], tax_rate, re_excl, pension_exclusion
            )
            results.append(result)

        results_df = pd.DataFrame(results)
        gross_wealth = results_df["gross_worth_b"].sum()
        total_exclusion_amount = results_df["exclusion_amount_b"].sum()
        taxable_wealth = results_df["taxable_wealth_b"].sum()
        gross_tax = results_df["tax_owed_b"].sum()
        n_billionaires = len(results_df)
    else:
        # Aggregate estimation
        if total_wealth_b is None:
            total_wealth_b = TOTAL_COLLECTIVE_WEALTH_B
        if num_billionaires is None:
            from src.data.baseline_data import TOTAL_CA_BILLIONAIRES
            num_billionaires = TOTAL_CA_BILLIONAIRES

        gross_wealth = total_wealth_b
        total_exclusion_amount = total_wealth_b * total_exclusion
        taxable_wealth = total_wealth_b * (1 - total_exclusion)
        # For aggregate, assume all are above phase-in ceiling
        gross_tax = taxable_wealth * tax_rate
        n_billionaires = num_billionaires

    # Apply compliance rate
    expected_collected = gross_tax * compliance_rate
    uncollected = gross_tax * (1 - compliance_rate)

    # Admin costs
    admin_cost_b = admin_cost_m / 1000

    # Net revenue
    net_revenue = expected_collected - admin_cost_b

    return {
        "n_billionaires": n_billionaires,
        "gross_wealth_b": round(gross_wealth, 2),
        "total_exclusions_b": round(total_exclusion_amount, 2),
        "taxable_wealth_b": round(taxable_wealth, 2),
        "tax_rate": tax_rate,
        "gross_tax_b": round(gross_tax, 2),
        "compliance_rate": compliance_rate,
        "expected_collected_b": round(expected_collected, 2),
        "uncollected_b": round(uncollected, 2),
        "admin_cost_b": round(admin_cost_b, 3),
        "net_revenue_b": round(net_revenue, 2),
    }


def compute_collection_timeline(
    net_revenue_b: float,
    installment_pct: float = 0.40,
    interest_rate: float = 0.05,
    start_year: int = 2027,
) -> pd.DataFrame:
    """
    Model the year-by-year collection timeline.

    Some taxpayers will pay in full in year 1; others will use the
    5-year installment option with interest.

    Args:
        net_revenue_b: Total net revenue to collect.
        installment_pct: Fraction of taxpayers choosing installments.
        interest_rate: Annual interest on deferred payments.
        start_year: First year of collection.

    Returns:
        DataFrame with year, lump_sum, installment, interest, total columns.
    """
    lump_sum_total = net_revenue_b * (1 - installment_pct)
    installment_total = net_revenue_b * installment_pct
    annual_installment = installment_total / INSTALLMENT_YEARS

    timeline = []
    remaining_balance = installment_total

    for i in range(INSTALLMENT_YEARS):
        year = start_year + i

        if i == 0:
            lump = lump_sum_total
        else:
            lump = 0

        interest = remaining_balance * interest_rate
        remaining_balance -= annual_installment

        timeline.append({
            "year": year,
            "lump_sum_b": round(lump, 2),
            "installment_b": round(annual_installment, 2),
            "interest_b": round(interest, 2),
            "total_b": round(lump + annual_installment + interest, 2),
        })

    return pd.DataFrame(timeline)


def revenue_waterfall_data(revenue: dict) -> list:
    """
    Generate waterfall chart data from revenue estimation results.

    Returns list of dicts with label, value, running_total for waterfall chart.
    """
    steps = [
        {"label": "Gross Wealth", "value": revenue["gross_wealth_b"], "type": "total"},
        {"label": "Exclusions", "value": -revenue["total_exclusions_b"], "type": "decrease"},
        {"label": "Taxable Wealth", "value": revenue["taxable_wealth_b"], "type": "subtotal"},
        {"label": f"Tax @ {revenue['tax_rate']:.0%}", "value": -(revenue["taxable_wealth_b"] - revenue["gross_tax_b"]), "type": "decrease"},
        {"label": "Gross Tax", "value": revenue["gross_tax_b"], "type": "subtotal"},
        {"label": "Non-compliance", "value": -revenue["uncollected_b"], "type": "decrease"},
        {"label": "Admin Costs", "value": -revenue["admin_cost_b"], "type": "decrease"},
        {"label": "Net Revenue", "value": revenue["net_revenue_b"], "type": "total"},
    ]
    return steps

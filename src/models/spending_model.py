"""
Spending impact model for the California Billionaire Tax Act.

Estimates the economic and social impact of spending the tax revenue
across healthcare (90%), education (5%), and food assistance (5%).
"""

import numpy as np
import pandas as pd

from src.data.baseline_data import ALLOCATION
from src.data.california_fiscal import (
    AVERAGE_TEACHER_SALARY,
    CALFRESH_AVG_BENEFIT_MONTHLY,
    CALFRESH_RECIPIENTS_M,
    FOOD_INSECURE_HOUSEHOLDS_M,
    MEDI_CAL_ENROLLEES_M,
    MEDI_CAL_TOTAL_SPENDING_B,
    UNINSURED_CA_M,
)


# Default fiscal multipliers
DEFAULT_MULTIPLIERS = {
    "healthcare": 1.5,
    "education": 1.2,
    "food_assistance": 1.7,
}

# Healthcare impact parameters
HEALTHCARE_JOBS_PER_BILLION = 15000  # Direct healthcare jobs per $1B spent
MEDI_CAL_COST_PER_ENROLLEE_YEAR = 9400  # Average annual cost per enrollee

# Education impact parameters
TEACHER_POSITIONS_PER_BILLION = int(1_000_000_000 / AVERAGE_TEACHER_SALARY)

# Food assistance parameters
ANNUAL_BENEFIT_PER_PERSON = CALFRESH_AVG_BENEFIT_MONTHLY * 12


def allocate_revenue(
    net_revenue_b: float,
    healthcare_pct: float = ALLOCATION["healthcare"],
    education_pct: float = ALLOCATION["education"],
    food_pct: float = ALLOCATION["food_assistance"],
) -> dict:
    """
    Allocate net revenue across spending categories.

    Args:
        net_revenue_b: Total net revenue in billions.
        healthcare_pct: Fraction to healthcare (default 90%).
        education_pct: Fraction to education (default 5%).
        food_pct: Fraction to food assistance (default 5%).

    Returns:
        Dict with allocation amounts.
    """
    return {
        "total_b": round(net_revenue_b, 2),
        "healthcare_b": round(net_revenue_b * healthcare_pct, 2),
        "education_b": round(net_revenue_b * education_pct, 2),
        "food_assistance_b": round(net_revenue_b * food_pct, 2),
        "healthcare_pct": healthcare_pct,
        "education_pct": education_pct,
        "food_pct": food_pct,
    }


def estimate_healthcare_impact(
    healthcare_spending_b: float,
    multiplier: float = DEFAULT_MULTIPLIERS["healthcare"],
    spending_years: int = 5,
) -> dict:
    """
    Estimate the impact of healthcare spending.

    Args:
        healthcare_spending_b: Total healthcare allocation in billions.
        multiplier: Fiscal multiplier for healthcare spending.
        spending_years: Years over which spending is distributed.

    Returns:
        Dict with healthcare impact estimates.
    """
    annual_spending_b = healthcare_spending_b / spending_years

    # Enrollee-years of coverage
    cost_per_enrollee_b = MEDI_CAL_COST_PER_ENROLLEE_YEAR / 1_000_000_000
    total_enrollee_years = healthcare_spending_b / cost_per_enrollee_b
    annual_enrollees = total_enrollee_years / spending_years

    # Direct healthcare jobs
    total_jobs_created = healthcare_spending_b * HEALTHCARE_JOBS_PER_BILLION / spending_years

    # GDP impact
    gdp_impact_b = healthcare_spending_b * multiplier

    return {
        "total_spending_b": round(healthcare_spending_b, 2),
        "annual_spending_b": round(annual_spending_b, 2),
        "spending_years": spending_years,
        "multiplier": multiplier,
        "total_enrollee_years": int(total_enrollee_years),
        "annual_additional_enrollees": int(annual_enrollees),
        "pct_of_uninsured_covered": round(
            annual_enrollees / (UNINSURED_CA_M * 1_000_000) * 100, 1
        ),
        "direct_jobs_created": int(total_jobs_created),
        "gdp_impact_b": round(gdp_impact_b, 2),
        "context": {
            "current_medi_cal_spending_b": MEDI_CAL_TOTAL_SPENDING_B,
            "current_enrollees_m": MEDI_CAL_ENROLLEES_M,
            "uninsured_m": UNINSURED_CA_M,
        },
    }


def estimate_education_impact(
    education_spending_b: float,
    multiplier: float = DEFAULT_MULTIPLIERS["education"],
    spending_years: int = 5,
) -> dict:
    """
    Estimate the impact of education spending.

    Args:
        education_spending_b: Total education allocation in billions.
        multiplier: Fiscal multiplier for education spending.
        spending_years: Years over which spending is distributed.

    Returns:
        Dict with education impact estimates.
    """
    annual_spending_b = education_spending_b / spending_years

    # Teacher position-years
    teacher_salary_b = AVERAGE_TEACHER_SALARY / 1_000_000_000
    total_teacher_years = education_spending_b / teacher_salary_b
    annual_teachers = total_teacher_years / spending_years

    # GDP impact
    gdp_impact_b = education_spending_b * multiplier

    return {
        "total_spending_b": round(education_spending_b, 2),
        "annual_spending_b": round(annual_spending_b, 2),
        "spending_years": spending_years,
        "multiplier": multiplier,
        "total_teacher_position_years": int(total_teacher_years),
        "annual_teacher_positions": int(annual_teachers),
        "gdp_impact_b": round(gdp_impact_b, 2),
        "avg_teacher_salary": AVERAGE_TEACHER_SALARY,
    }


def estimate_food_assistance_impact(
    food_spending_b: float,
    multiplier: float = DEFAULT_MULTIPLIERS["food_assistance"],
    spending_years: int = 5,
) -> dict:
    """
    Estimate the impact of food assistance spending.

    Args:
        food_spending_b: Total food assistance allocation in billions.
        multiplier: Fiscal multiplier for food assistance.
        spending_years: Years over which spending is distributed.

    Returns:
        Dict with food assistance impact estimates.
    """
    annual_spending_b = food_spending_b / spending_years

    # Household-years of assistance
    annual_benefit_b = ANNUAL_BENEFIT_PER_PERSON / 1_000_000_000
    # Assume average household size of 2.5
    household_benefit_b = annual_benefit_b * 2.5
    total_household_years = food_spending_b / household_benefit_b
    annual_households = total_household_years / spending_years

    # GDP impact
    gdp_impact_b = food_spending_b * multiplier

    return {
        "total_spending_b": round(food_spending_b, 2),
        "annual_spending_b": round(annual_spending_b, 2),
        "spending_years": spending_years,
        "multiplier": multiplier,
        "total_household_years": int(total_household_years),
        "annual_households_served": int(annual_households),
        "pct_food_insecure_served": round(
            annual_households / (FOOD_INSECURE_HOUSEHOLDS_M * 1_000_000) * 100, 1
        ),
        "gdp_impact_b": round(gdp_impact_b, 2),
        "context": {
            "current_recipients_m": CALFRESH_RECIPIENTS_M,
            "food_insecure_households_m": FOOD_INSECURE_HOUSEHOLDS_M,
            "avg_monthly_benefit": CALFRESH_AVG_BENEFIT_MONTHLY,
        },
    }


def compute_total_spending_impact(
    net_revenue_b: float,
    healthcare_pct: float = ALLOCATION["healthcare"],
    education_pct: float = ALLOCATION["education"],
    food_pct: float = ALLOCATION["food_assistance"],
    healthcare_multiplier: float = DEFAULT_MULTIPLIERS["healthcare"],
    education_multiplier: float = DEFAULT_MULTIPLIERS["education"],
    food_multiplier: float = DEFAULT_MULTIPLIERS["food_assistance"],
    spending_years: int = 5,
) -> dict:
    """
    Compute total spending impact across all categories.

    Returns:
        Dict with allocation, impacts per category, and totals.
    """
    allocation = allocate_revenue(
        net_revenue_b, healthcare_pct, education_pct, food_pct
    )

    healthcare = estimate_healthcare_impact(
        allocation["healthcare_b"], healthcare_multiplier, spending_years
    )
    education = estimate_education_impact(
        allocation["education_b"], education_multiplier, spending_years
    )
    food = estimate_food_assistance_impact(
        allocation["food_assistance_b"], food_multiplier, spending_years
    )

    total_gdp_impact = (
        healthcare["gdp_impact_b"]
        + education["gdp_impact_b"]
        + food["gdp_impact_b"]
    )

    # Weighted average multiplier
    weighted_multiplier = total_gdp_impact / net_revenue_b if net_revenue_b > 0 else 0

    return {
        "allocation": allocation,
        "healthcare": healthcare,
        "education": education,
        "food_assistance": food,
        "total_gdp_impact_b": round(total_gdp_impact, 2),
        "weighted_avg_multiplier": round(weighted_multiplier, 3),
        "total_direct_jobs": healthcare["direct_jobs_created"],
    }

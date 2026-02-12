"""
All model parameters with sources, confidence levels, and notes.

Each parameter maps to a structured entry for transparency and documentation.
"""

ASSUMPTIONS = {
    # --- Revenue Model ---
    "tax_rate": {
        "value": 0.05,
        "unit": "rate",
        "label": "Tax Rate",
        "source": "Initiative 25-0024 text",
        "confidence": "high",
        "notes": "Statutory rate set by the initiative. Not adjustable.",
    },
    "threshold": {
        "value": 1.0,
        "unit": "billions USD",
        "label": "Wealth Threshold",
        "source": "Initiative 25-0024 text",
        "confidence": "high",
        "notes": "Tax applies to individuals with net worth > $1B.",
    },
    "phase_in_range": {
        "value": [1.0, 1.1],
        "unit": "billions USD",
        "label": "Phase-In Range",
        "source": "Initiative 25-0024 text",
        "confidence": "high",
        "notes": "Rate phases in linearly from $1.0B to $1.1B.",
    },
    "real_estate_exclusion": {
        "value": 0.10,
        "unit": "fraction",
        "label": "Real Estate Exclusion",
        "source": "Average asset composition from Forbes/SEC data",
        "confidence": "medium",
        "notes": "Real estate holdings excluded from tax base. Average ~10% but varies widely by individual.",
    },
    "pension_exclusion": {
        "value": 0.01,
        "unit": "fraction",
        "label": "Pension/Retirement Exclusion",
        "source": "Estimate based on tax law",
        "confidence": "medium",
        "notes": "Pension and retirement accounts excluded. Small fraction for billionaires.",
    },
    "compliance_rate": {
        "value": 0.85,
        "unit": "fraction",
        "label": "Compliance Rate",
        "source": "IRS high-income compliance estimates, adjusted for wealth tax novelty",
        "confidence": "low",
        "notes": "Major uncertainty. No precedent for US wealth tax compliance. Range: 60-95%.",
    },
    "admin_cost": {
        "value": 150,
        "unit": "millions USD",
        "label": "Administrative Cost",
        "source": "LAO 2025 analysis (range: $15M-$300M)",
        "confidence": "medium",
        "notes": "LAO range is very wide. Midpoint used as baseline.",
    },

    # --- Migration Model ---
    "elasticity": {
        "value": 0.35,
        "unit": "elasticity",
        "label": "Migration Elasticity",
        "source": "Moretti & Wilson 2019 (ultra-wealthy)",
        "confidence": "medium",
        "notes": "Applies to annual taxes; adjustment needed for one-time tax. Range in literature: 0.06-1.9.",
    },
    "one_time_to_annual_factor": {
        "value": 0.2,
        "unit": "fraction",
        "label": "One-Time to Annual Conversion",
        "source": "Model assumption: 5% one-time / 5 years = 1% equivalent annual",
        "confidence": "low",
        "notes": "Critical assumption. Published elasticities are for annual taxes. This conversion is a major source of uncertainty.",
    },
    "anti_avoidance_discount": {
        "value": 0.30,
        "unit": "fraction",
        "label": "Anti-Avoidance Effectiveness",
        "source": "Model assumption based on Jan 1 2026 date + 25% min apportionment",
        "confidence": "low",
        "notes": "The Jan 1 2026 residency date (before ballot qualification) limits avoidance strategies.",
    },
    "avg_billionaire_income_tax": {
        "value": 50,
        "unit": "millions USD/year",
        "label": "Avg. Annual CA Income Tax per Billionaire",
        "source": "Estimated from FTB data on top earners",
        "confidence": "medium",
        "notes": "Varies enormously by individual based on income realization patterns.",
    },
    "firm_effect_discount": {
        "value": 0.50,
        "unit": "fraction",
        "label": "Firm Effect CA Discount",
        "source": "Model assumption (CA tech vs Swedish firms)",
        "confidence": "low",
        "notes": "Sweden firm data may not transfer to CA tech-heavy billionaire base. Tech firms may be more resilient.",
    },

    # --- Spending Model ---
    "healthcare_multiplier": {
        "value": 1.5,
        "unit": "multiplier",
        "label": "Healthcare Fiscal Multiplier",
        "source": "Richmond Fed Medicaid estimate",
        "confidence": "medium",
        "notes": "Assumes normal economic conditions. Higher in recessions, lower in expansions.",
    },
    "education_multiplier": {
        "value": 1.2,
        "unit": "multiplier",
        "label": "Education Fiscal Multiplier",
        "source": "CBO estimates",
        "confidence": "medium",
        "notes": "Near-term multiplier. Long-term returns from education investment are typically much higher.",
    },
    "food_multiplier": {
        "value": 1.7,
        "unit": "multiplier",
        "label": "Food Assistance Fiscal Multiplier",
        "source": "USDA SNAP analysis",
        "confidence": "medium",
        "notes": "High multiplier due to high marginal propensity to consume among recipients.",
    },
    "spending_years": {
        "value": 5,
        "unit": "years",
        "label": "Revenue Spending Period",
        "source": "Model assumption",
        "confidence": "medium",
        "notes": "Revenue assumed to be spent over 5 years. Faster spending would amplify short-term effects.",
    },

    # --- Cost-Benefit Model ---
    "discount_rate": {
        "value": 0.03,
        "unit": "rate",
        "label": "Discount Rate",
        "source": "Standard public policy discount rate (OMB Circular A-94)",
        "confidence": "medium",
        "notes": "3% is standard for public policy analysis. Range: 1-7%.",
    },
    "horizon_years": {
        "value": 20,
        "unit": "years",
        "label": "Analysis Horizon",
        "source": "Model assumption",
        "confidence": "high",
        "notes": "20-year horizon captures both short-term revenue and long-term migration costs.",
    },
}


def get_assumption(key: str) -> dict:
    """Get a single assumption entry."""
    return ASSUMPTIONS.get(key, {})


def get_assumptions_by_confidence(confidence: str) -> list:
    """Get all assumptions with a given confidence level."""
    return [
        {"key": k, **v}
        for k, v in ASSUMPTIONS.items()
        if v["confidence"] == confidence
    ]


def get_all_assumptions() -> list:
    """Get all assumptions as a list."""
    return [{"key": k, **v} for k, v in ASSUMPTIONS.items()]

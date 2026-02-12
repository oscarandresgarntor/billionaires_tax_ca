"""
Pre-built scenario definitions for the California Billionaire Tax Act analysis.

Each scenario represents a different set of assumptions about key parameters,
ranging from optimistic (proponent view) to extreme flight (worst case).
"""


SCENARIOS = {
    "optimistic": {
        "name": "Optimistic",
        "description": "Low migration, high compliance, strong fiscal multipliers. Represents the proponent view.",
        "params": {
            "elasticity": 0.06,
            "compliance_rate": 0.95,
            "admin_cost_m": 15,
            "healthcare_multiplier": 1.7,
            "education_multiplier": 1.4,
            "food_multiplier": 1.9,
            "anti_avoidance_discount": 0.50,
            "firm_effect_discount": 0.75,
            "installment_pct": 0.30,
        },
        "color": "#2ecc71",
        "icon": "chart_with_upwards_trend",
    },
    "baseline": {
        "name": "Baseline",
        "description": "Research-grounded central estimates. Balances optimistic and pessimistic assumptions.",
        "params": {
            "elasticity": 0.35,
            "compliance_rate": 0.85,
            "admin_cost_m": 150,
            "healthcare_multiplier": 1.5,
            "education_multiplier": 1.2,
            "food_multiplier": 1.7,
            "anti_avoidance_discount": 0.30,
            "firm_effect_discount": 0.50,
            "installment_pct": 0.40,
        },
        "color": "#3498db",
        "icon": "balance_scale",
    },
    "pessimistic": {
        "name": "Pessimistic",
        "description": "Higher migration, lower compliance, moderate multipliers. Represents opponent concerns.",
        "params": {
            "elasticity": 1.0,
            "compliance_rate": 0.70,
            "admin_cost_m": 300,
            "healthcare_multiplier": 1.3,
            "education_multiplier": 1.0,
            "food_multiplier": 1.5,
            "anti_avoidance_discount": 0.15,
            "firm_effect_discount": 0.30,
            "installment_pct": 0.50,
        },
        "color": "#e67e22",
        "icon": "warning",
    },
    "extreme_flight": {
        "name": "Extreme Flight",
        "description": "Maximum migration, lowest compliance, weak multipliers. Worst-case stress test.",
        "params": {
            "elasticity": 1.9,
            "compliance_rate": 0.60,
            "admin_cost_m": 300,
            "healthcare_multiplier": 1.2,
            "education_multiplier": 0.9,
            "food_multiplier": 1.4,
            "anti_avoidance_discount": 0.10,
            "firm_effect_discount": 0.20,
            "installment_pct": 0.60,
        },
        "color": "#e74c3c",
        "icon": "rotating_light",
    },
}

# Common parameters shared across all scenarios
COMMON_PARAMS = {
    "total_wealth_b": 2245,
    "num_billionaires": 250,
    "tax_rate": 0.05,
    "real_estate_exclusion": 0.10,
    "pension_exclusion": 0.01,
    "one_time_adjustment": True,
    "avg_income_tax_m": 50,
    "healthcare_pct": 0.90,
    "education_pct": 0.05,
    "food_pct": 0.05,
    "spending_years": 5,
    "horizon_years": 20,
    "discount_rate": 0.03,
    "start_year": 2027,
}


def get_scenario_params(scenario_key: str) -> dict:
    """
    Get the full parameter dict for a scenario.

    Merges scenario-specific params with common params.

    Args:
        scenario_key: One of 'optimistic', 'baseline', 'pessimistic', 'extreme_flight'.

    Returns:
        Complete parameter dict for compute_cost_benefit_timeline().
    """
    scenario = SCENARIOS[scenario_key]
    return {**COMMON_PARAMS, **scenario["params"]}


def get_all_scenario_params() -> dict:
    """Get params for all scenarios."""
    return {key: get_scenario_params(key) for key in SCENARIOS}


def get_scenario_descriptions() -> list:
    """Get list of scenario descriptions for display."""
    return [
        {
            "key": key,
            "name": s["name"],
            "description": s["description"],
            "color": s["color"],
        }
        for key, s in SCENARIOS.items()
    ]

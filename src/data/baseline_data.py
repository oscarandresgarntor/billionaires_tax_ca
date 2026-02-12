"""
Baseline data from the UC Berkeley expert report (Galle, Gamage, Saez, Shanske, Dec 2025).

Source: "Revenue Estimate for the California Billionaire Tax Act"
Authors: Brian Galle, David Gamage, Emmanuel Saez, Darien Shanske
Date: December 2025

All monetary values in billions USD unless otherwise noted.
"""

# --- Core statistics from UC Berkeley report ---

TOTAL_CA_BILLIONAIRES = 204
TOTAL_COLLECTIVE_WEALTH_B = 2190  # $2.19 trillion
AVERAGE_WEALTH_B = TOTAL_COLLECTIVE_WEALTH_B / TOTAL_CA_BILLIONAIRES  # ~$10.74B

# Tax parameters from the initiative text
TAX_RATE = 0.05  # 5% excise tax
THRESHOLD_B = 1.0  # $1 billion net worth threshold
PHASE_IN_FLOOR_B = 1.0  # Phase-in starts at $1B
PHASE_IN_CEILING_B = 1.1  # Full rate applies at $1.1B+

# Residency determination date
RESIDENCY_DATE = "January 1, 2026"
RESIDENCY_NOTE = (
    "Residency determined as of Jan 1, 2026, before ballot qualification. "
    "This limits pre-election avoidance strategies."
)

# Revenue allocation per initiative text
ALLOCATION = {
    "healthcare": 0.90,
    "education": 0.05,
    "food_assistance": 0.05,
}

# --- Asset composition (average across CA billionaires) ---

ASSET_COMPOSITION = {
    "public_equity": 0.60,
    "private_holdings": 0.25,
    "real_estate": 0.10,
    "other": 0.05,
}

# --- Exclusions ---

REAL_ESTATE_EXCLUSION_PCT = 0.10  # ~10% of wealth in real estate (excluded)
PENSION_RETIREMENT_EXCLUSION_PCT = 0.01  # ~1% pension/retirement (excluded)
TOTAL_EXCLUSION_PCT = REAL_ESTATE_EXCLUSION_PCT + PENSION_RETIREMENT_EXCLUSION_PCT

# --- Administrative cost estimates (LAO) ---

ADMIN_COST_LOW_M = 15  # $15M (LAO low estimate)
ADMIN_COST_MID_M = 150  # $150M (midpoint)
ADMIN_COST_HIGH_M = 300  # $300M (LAO high estimate)

# --- CA fiscal context ---

CA_ANNUAL_INCOME_TAX_REVENUE_B = 120  # ~$120B annual
TOP_1_PCT_SHARE_OF_INCOME_TAX = 0.50  # Top 1% pays ~50%
CA_ANNUAL_VC_INVESTMENT_B = 150  # ~$150B annual VC
BILLIONAIRE_SHARE_OF_VC = 0.15  # ~15% from billionaires
CA_ANNUAL_HIGH_EARNER_MIGRATION_LOSS_B = 1.7  # ~$1.7B/year already

# --- Anti-avoidance provisions ---

MIN_APPORTIONMENT_FACTOR = 0.25  # 25% minimum for partial residents
INSTALLMENT_YEARS = 5  # Can pay over 5 years with interest

# --- Wealth distribution tiers (approximate from Forbes data) ---

WEALTH_TIERS = [
    {"range": "$1B-$2B", "count": 68, "avg_wealth_b": 1.4, "total_wealth_b": 95.2},
    {"range": "$2B-$5B", "count": 65, "avg_wealth_b": 3.1, "total_wealth_b": 201.5},
    {"range": "$5B-$10B", "count": 35, "avg_wealth_b": 7.0, "total_wealth_b": 245.0},
    {"range": "$10B-$50B", "count": 28, "avg_wealth_b": 22.0, "total_wealth_b": 616.0},
    {"range": "$50B+", "count": 8, "avg_wealth_b": 129.0, "total_wealth_b": 1032.0},
]

# --- Industry breakdown (from Forbes Real-Time Billionaires API, Feb 2026) ---
# Note: Forbes identifies 280 CA billionaires ($2,378B) vs Berkeley report's 204 ($2,190B).
# Difference due to date, residency definitions, and methodology.
# Industry proportions from Forbes are used for the chart; tax model uses Berkeley totals.

INDUSTRY_BREAKDOWN = {
    "Technology": {"count": 125, "total_wealth_b": 1764.2},
    "Finance & Investments": {"count": 65, "total_wealth_b": 285.8},
    "Retail & Consumer": {"count": 32, "total_wealth_b": 115.6},
    "Media & Entertainment": {"count": 18, "total_wealth_b": 68.0},
    "Real Estate": {"count": 11, "total_wealth_b": 60.5},
    "Manufacturing": {"count": 9, "total_wealth_b": 38.5},
    "Healthcare": {"count": 8, "total_wealth_b": 18.1},
    "Energy": {"count": 3, "total_wealth_b": 7.4},
    "Other": {"count": 9, "total_wealth_b": 19.6},
}

FORBES_DATA_NOTE = (
    "Industry breakdown sourced from Forbes Real-Time Billionaires API "
    "(komed3/rtb-api), fetched Feb 2026. Forbes identifies 280 CA billionaires "
    "vs Berkeley report's 204 due to different dates and residency criteria."
)


def get_baseline_summary():
    """Return a summary dict of baseline data for display."""
    return {
        "total_billionaires": TOTAL_CA_BILLIONAIRES,
        "total_wealth_b": TOTAL_COLLECTIVE_WEALTH_B,
        "average_wealth_b": round(AVERAGE_WEALTH_B, 2),
        "tax_rate": TAX_RATE,
        "threshold_b": THRESHOLD_B,
        "gross_taxable_wealth_b": round(
            TOTAL_COLLECTIVE_WEALTH_B * (1 - TOTAL_EXCLUSION_PCT), 1
        ),
        "gross_revenue_estimate_b": round(
            TOTAL_COLLECTIVE_WEALTH_B * (1 - TOTAL_EXCLUSION_PCT) * TAX_RATE, 1
        ),
    }

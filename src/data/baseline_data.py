"""
Baseline data for the California 2026 Billionaire Tax Act analysis.

Primary source: Forbes Real-Time Billionaires API (komed3/rtb-api), fetched Feb 2026.
Cross-reference: UC Berkeley expert report (Galle, Gamage, Saez, Shanske, Dec 2025).

Forbes provides verifiable, individual-level data for 250 CA billionaires.
The Berkeley report cited 204 billionaires ($2.19T) but did not disclose
its data sources or methodology. The ~46-person gap is likely due to date
differences (Dec 2025 vs Feb 2026), residency definitions, and 59 billionaires
near the $1B threshold who frequently cross in/out with market movements.

All monetary values in billions USD unless otherwise noted.
"""

# --- Core statistics (Forbes Real-Time Billionaires API, Feb 2026) ---

TOTAL_CA_BILLIONAIRES = 250
TOTAL_COLLECTIVE_WEALTH_B = 2245  # $2.245 trillion
AVERAGE_WEALTH_B = TOTAL_COLLECTIVE_WEALTH_B / TOTAL_CA_BILLIONAIRES  # ~$8.98B

# Cross-reference: Berkeley report (Dec 2025)
BERKELEY_BILLIONAIRES = 204
BERKELEY_WEALTH_B = 2190

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

# --- Wealth distribution tiers (from Forbes API, Feb 2026) ---

WEALTH_TIERS = [
    {"range": "$1B-$2B", "count": 91, "avg_wealth_b": 1.4, "total_wealth_b": 125.3},
    {"range": "$2B-$5B", "count": 93, "avg_wealth_b": 3.1, "total_wealth_b": 289.2},
    {"range": "$5B-$10B", "count": 37, "avg_wealth_b": 6.8, "total_wealth_b": 250.8},
    {"range": "$10B-$50B", "count": 24, "avg_wealth_b": 17.7, "total_wealth_b": 425.9},
    {"range": "$50B+", "count": 5, "avg_wealth_b": 230.8, "total_wealth_b": 1154.0},
]

# --- Industry breakdown (from Forbes API, Feb 2026) ---

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
        "source": "Forbes Real-Time Billionaires API (Feb 2026)",
        "berkeley_comparison": {
            "billionaires": BERKELEY_BILLIONAIRES,
            "wealth_b": BERKELEY_WEALTH_B,
        },
    }

"""
Structured citation database for all research sources used in the analysis.
"""

CITATIONS = {
    "forbes_rtb_2026": {
        "authors": "Forbes / komed3 (RTB API)",
        "year": 2026,
        "title": "Forbes Real-Time Billionaires List",
        "source": "Forbes Real-Time Billionaires API (github.com/komed3/rtb-api)",
        "date": "February 2026",
        "key_findings": [
            "250 California billionaires with $2.25T collective wealth",
            "Technology sector: 125 billionaires, $1.76T (74% of total wealth)",
            "Individual-level data verifiable against SEC filings",
        ],
        "url": "https://github.com/komed3/rtb-api",
    },
    "berkeley_2025": {
        "authors": "Galle, B., Gamage, D., Saez, E., & Shanske, D.",
        "year": 2025,
        "title": "Revenue Estimate for the California Billionaire Tax Act",
        "source": "UC Berkeley",
        "date": "December 2025",
        "key_findings": [
            "Cited 204 California billionaires with $2.19T collective wealth",
            "Data sources and methodology not disclosed in report",
            "Used as cross-reference; Forbes API data (250 billionaires, $2.25T) used as primary baseline",
        ],
        "url": "",
    },
    "young_2016": {
        "authors": "Young, C., Varner, C., Lurie, I., & Prisinzano, R.",
        "year": 2016,
        "title": "Millionaire Migration and Taxation of the Elite: Evidence from Administrative Data",
        "source": "American Sociological Review, 81(3), 421-446",
        "key_findings": [
            "Very low migration elasticity (0.06) for millionaires",
            "Only 2.4% of millionaires move across state lines annually",
            "Tax-motivated migration is rare among the general wealthy population",
        ],
        "url": "https://doi.org/10.1177/0003122416639625",
    },
    "moretti_wilson_2017": {
        "authors": "Moretti, E., & Wilson, D.",
        "year": 2017,
        "title": "The Effect of State Taxes on the Geographical Location of Top Earners: Evidence from Star Scientists",
        "source": "American Economic Review, 107(7), 1858-1903",
        "key_findings": [
            "High migration elasticity (1.9) for star scientists",
            "Highly mobile knowledge workers respond strongly to tax differentials",
            "Not directly applicable to billionaire wealth tax",
        ],
        "url": "https://doi.org/10.1257/aer.20150508",
    },
    "moretti_wilson_2019": {
        "authors": "Moretti, E., & Wilson, D.",
        "year": 2019,
        "title": "Taxing Billionaires: Estate Taxes and the Geographical Location of the Ultra-Wealthy",
        "source": "NBER Working Paper",
        "key_findings": [
            "Moderate elasticity (0.35) for ultra-wealthy individuals",
            "Estate tax differentials affect location decisions",
            "Used as baseline elasticity for our model",
        ],
        "url": "",
    },
    "munoz_2024": {
        "authors": "Munoz, M.",
        "year": 2024,
        "title": "Do Wealth Taxes Affect Economic Growth? Evidence from Swedish Billionaires",
        "source": "Working Paper",
        "key_findings": [
            "Billionaire departures led to -33% employment at their firms",
            "-34% value added, -50% tax payments",
            "Significant real economic effects from wealth tax-induced migration",
        ],
        "url": "",
    },
    "lao_2025": {
        "authors": "California Legislative Analyst's Office",
        "year": 2025,
        "title": "Analysis of Proposed Initiative: Billionaire Tax Act",
        "source": "LAO",
        "key_findings": [
            "Revenue estimate: 'tens of billions of dollars'",
            "Administrative cost: $15M-$300M range",
            "Significant implementation challenges noted",
        ],
        "url": "",
    },
    "richmond_fed_medicaid": {
        "authors": "Federal Reserve Bank of Richmond",
        "year": 2023,
        "title": "Medicaid Spending Multiplier Estimates",
        "source": "Richmond Fed Economic Brief",
        "key_findings": [
            "Healthcare spending multiplier estimated at 1.5x",
            "Higher during recessions, lower during expansions",
        ],
        "url": "",
    },
    "usda_snap": {
        "authors": "USDA Economic Research Service",
        "year": 2019,
        "title": "The Supplemental Nutrition Assistance Program (SNAP) and the Economy",
        "source": "USDA ERS",
        "key_findings": [
            "SNAP multiplier estimated at 1.5-1.7x",
            "High marginal propensity to consume among recipients",
        ],
        "url": "",
    },
}


def get_citation_text(key: str) -> str:
    """Get a formatted citation string."""
    c = CITATIONS[key]
    return f"{c['authors']} ({c['year']}). {c['title']}. {c['source']}."


def get_all_citations() -> list:
    """Get all citations as formatted strings."""
    return [
        {"key": k, "text": get_citation_text(k), **v}
        for k, v in CITATIONS.items()
    ]

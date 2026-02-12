"""
Methodology page: Documentation, citations, and assumptions.
"""

import streamlit as st
import pandas as pd

from src.references.citations import CITATIONS, get_citation_text
from src.references.assumptions import ASSUMPTIONS, get_all_assumptions

st.title("Methodology & Sources")
st.markdown("""
This page documents all data sources, model assumptions, formulas, and
citations used in the analysis. Transparency is a core design principle.
""")

# Data Sources
st.header("Data Sources")

st.markdown("""
| Source | What It Provides | Confidence |
|--------|-----------------|-----------|
| **Forbes Real-Time Billionaires API** (Feb 2026) | **Primary baseline**: 250 CA billionaires, $2.25T wealth, industry, individual data | **High** |
| UC Berkeley expert report (Dec 2025) | Cross-reference: 204 billionaires, $2.19T (methodology not disclosed) | Medium |
| CA Legislative Analyst's Office (2025) | Admin cost range ($15M-$300M), revenue order of magnitude | Medium |
| Franchise Tax Board / IRS SOI | Income tax revenue, high-earner migration data | High |
| Published migration studies | Elasticity estimates (0.06 to 1.9) | Medium |
| Federal Reserve / USDA | Fiscal multiplier estimates | Medium |

Forbes data is preferred because each entry is individually verifiable against public stock holdings
and SEC filings. The Berkeley report did not disclose its data sources or methodology.
""")

st.divider()

# Model Overview
st.header("Model Architecture")

st.markdown("""
The analysis integrates four sub-models:

1. **Revenue Model**: Gross wealth → exclusions → taxable wealth → gross tax → compliance → net revenue
2. **Migration Model**: Elasticity-based departure estimates → income tax loss + firm effects + VC impact
3. **Spending Model**: Revenue allocation → fiscal multiplier → GDP impact + social outcomes
4. **Cost-Benefit Model**: Benefits (revenue + GDP impact) − Costs (admin + migration losses) → NPV

All parameters are adjustable in the Scenario Explorer page.
""")

st.divider()

# Key Formulas
st.header("Key Formulas")

st.markdown("""
### Revenue Estimation
```
Taxable_Wealth = Gross_Wealth × (1 - RE_Exclusion - Pension_Exclusion)
Effective_Rate = Tax_Rate × phase_in_factor(net_worth)
Gross_Tax = Σ Taxable_Wealth_i × Effective_Rate_i
Net_Revenue = Gross_Tax × Compliance_Rate - Admin_Cost
```

### Phase-In
```
For net_worth in [$1.0B, $1.1B]:
    effective_rate = 5% × (net_worth - 1.0) / (1.1 - 1.0)
```

### Migration Departures
```
effective_annual_rate = statutory_rate × (1/5)   [one-time adjustment]
pct_change = effective_rate / (1 - effective_rate)
raw_departures = N × elasticity × pct_change
departures = raw_departures × (1 - anti_avoidance_discount)
```

### Annual Migration Cost
```
income_tax_loss = departures × avg_income_tax_per_billionaire
firm_loss = departures × avg_firm_revenue × value_added_effect × (1 - CA_discount)
vc_loss = (departures / N) × billionaire_vc_total
total_annual_cost = income_tax_loss + firm_loss + vc_loss
```

### Spending Impact
```
GDP_Impact = Σ (Allocation_category × Multiplier_category)
```

### Net Present Value
```
NPV = Σ_{t=0}^{T} (Benefits_t - Costs_t) / (1 + r)^t
```
""")

st.divider()

# Assumptions Table
st.header("All Model Assumptions")

assumptions = get_all_assumptions()
assumptions_df = pd.DataFrame(assumptions)

# Color-code confidence
def confidence_color(conf):
    colors = {"high": "🟢", "medium": "🟡", "low": "🔴"}
    return colors.get(conf, "⚪")

display_df = assumptions_df[["label", "value", "unit", "confidence", "source", "notes"]].copy()
display_df["confidence"] = display_df["confidence"].apply(
    lambda c: f"{confidence_color(c)} {c.title()}"
)
display_df.columns = ["Parameter", "Value", "Unit", "Confidence", "Source", "Notes"]

st.dataframe(display_df, hide_index=True, use_container_width=True, height=600)

st.markdown("""
**Confidence Levels**:
- 🟢 **High**: Directly from initiative text or official data
- 🟡 **Medium**: From published research, reasonable range
- 🔴 **Low**: Major uncertainty, significant modeling assumptions
""")

st.divider()

# Key Uncertainties
st.header("Key Uncertainties & Limitations")

st.markdown("""
### 1. One-Time vs. Annual Tax Elasticity
Published migration elasticities are estimated for **annual** taxes. Applying them to a
**one-time** tax likely overstates the migration response. Our conversion (÷5) is a
simplification. The actual behavioral response to a one-time levy is genuinely unknown.

### 2. Compliance Rate
No precedent exists for a US state-level wealth tax. The compliance rate (60-95% range)
is highly uncertain. Wealthy individuals have significant resources for legal challenges
and tax planning, but the one-time nature limits avoidance windows.

### 3. Anti-Avoidance Effectiveness
The January 1, 2026 residency date (set before ballot qualification) is novel. Its
effectiveness at preventing strategic relocation is untested.

### 4. Firm-Level Effects
Swedish wealth tax data (Munoz 2024) shows significant firm-level effects from billionaire
departures, but CA's tech-heavy billionaire base may behave differently. Tech firms often
have professional management and may be more resilient to founder departure.

### 5. Fiscal Multipliers
Multiplier estimates assume normal economic conditions. If the revenue is spent during
a recession, multipliers would be higher; during an expansion, lower. The timing and
efficiency of government spending also affect realized multipliers.

### 6. Legal Challenges
The initiative may face constitutional challenges. This analysis assumes the tax is
implemented as written, but legal risk is a significant real-world uncertainty not
modeled here.
""")

st.divider()

# Citations
st.header("References")

for key, citation in CITATIONS.items():
    st.markdown(f"**{citation['authors']} ({citation['year']})**. "
                f"*{citation['title']}*. {citation['source']}.")
    if citation.get("url"):
        st.markdown(f"[Link]({citation['url']})")
    if citation.get("key_findings"):
        for finding in citation["key_findings"]:
            st.markdown(f"  - {finding}")
    st.markdown("")

st.divider()

# Disclaimer
st.info("""
**Disclaimer**: This tool is for educational and research purposes. It is not
investment, legal, or tax advice. The analysis uses simplified models and
published estimates that involve significant uncertainty. Users should consult
the original sources and professional advisors for decision-making.
""")

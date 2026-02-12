"""
California fiscal context data.

Provides state-level fiscal data for contextualizing the billionaire tax
revenue and costs against California's broader budget.
"""

# All monetary values in billions USD unless otherwise noted.

# --- State Budget Context ---

CA_GENERAL_FUND_B = 225  # ~$225B total state budget (2025-26)
CA_INCOME_TAX_REVENUE_B = 120  # Personal income tax revenue
CA_CORPORATE_TAX_REVENUE_B = 22  # Corporate tax revenue
CA_SALES_TAX_REVENUE_B = 32  # Sales & use tax revenue

# --- Healthcare Spending Context ---

MEDI_CAL_TOTAL_SPENDING_B = 145  # Total Medi-Cal spending (federal + state)
MEDI_CAL_STATE_SHARE_B = 45  # State share of Medi-Cal
MEDI_CAL_ENROLLEES_M = 15.4  # ~15.4 million enrolled
UNINSURED_CA_M = 2.7  # ~2.7 million uninsured Californians

# --- Education Context ---

K12_PER_PUPIL_SPENDING = 16500  # Per-pupil spending ($ per student)
K12_TOTAL_ENROLLMENT_M = 5.9  # Million students
AVERAGE_TEACHER_SALARY = 92000  # Average CA teacher salary + benefits
CSU_UC_ENROLLMENT_M = 0.8  # ~800K students in public higher ed

# --- Food Assistance Context ---

CALFRESH_RECIPIENTS_M = 5.1  # ~5.1 million CalFresh recipients
CALFRESH_AVG_BENEFIT_MONTHLY = 234  # Average monthly benefit per person
FOOD_INSECURE_HOUSEHOLDS_M = 4.2  # ~4.2 million food insecure

# --- High-Earner Migration Context ---

ANNUAL_HIGH_EARNER_OUTMIGRATION_B = 1.7  # Lost tax revenue from high-earner migration
NET_DOMESTIC_MIGRATION_THOUSANDS = -340  # Net domestic out-migration (annual)
TOP_INCOME_TAX_RATE = 0.133  # 13.3% top marginal rate

# --- Income Tax Concentration ---

INCOME_TAX_CONCENTRATION = {
    "top_0_1_pct": {"share_of_tax": 0.25, "avg_agi_m": 12.5},
    "top_1_pct": {"share_of_tax": 0.50, "avg_agi_m": 2.8},
    "top_5_pct": {"share_of_tax": 0.70, "avg_agi_m": 0.8},
    "top_10_pct": {"share_of_tax": 0.80, "avg_agi_m": 0.45},
}

# Average CA income tax paid per billionaire (estimated)
AVG_BILLIONAIRE_INCOME_TAX_M = 50  # ~$50M/year average


def get_fiscal_context():
    """Return a dict summarizing CA fiscal context."""
    return {
        "state_budget_b": CA_GENERAL_FUND_B,
        "income_tax_revenue_b": CA_INCOME_TAX_REVENUE_B,
        "medi_cal_spending_b": MEDI_CAL_TOTAL_SPENDING_B,
        "medi_cal_enrollees_m": MEDI_CAL_ENROLLEES_M,
        "uninsured_m": UNINSURED_CA_M,
        "food_insecure_m": FOOD_INSECURE_HOUSEHOLDS_M,
        "annual_migration_loss_b": ANNUAL_HIGH_EARNER_OUTMIGRATION_B,
        "top_tax_rate": TOP_INCOME_TAX_RATE,
    }

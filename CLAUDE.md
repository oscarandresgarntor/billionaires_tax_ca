# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive Streamlit dashboard analyzing the California 2026 Billionaire Tax Act (Initiative 25-0024) — a proposed one-time 5% excise tax on individuals with net worth >$1B. The central question: **What is the cost-benefit for California in the short and long term?**

## Commands

```bash
# Run the dashboard locally
streamlit run app.py

# Run all tests (60 tests)
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_revenue_model.py -v

# Run a single test class or method
python -m pytest tests/test_cost_benefit_model.py::TestCostBenefitTimeline::test_baseline_runs -v
```

## Architecture

**Entry point**: `app.py` uses `st.navigation` + `st.Page` to route between 7 pages.

**Data flow**: Pages import from `src/models/` which import from `src/data/`. Pages never call data layer directly for computations.

```
pages/ (Streamlit UI) → src/models/ (computation) → src/data/ (constants)
                       → src/visualization/ (charts)
                       → src/references/ (citations, assumptions)
```

### Models (src/models/)

Four models compose into the integrated cost-benefit analysis:

- **revenue_model.py**: Phase-in calculation ($1B-$1.1B), exclusions (RE, pensions), compliance, admin costs, installment timeline. Core function: `estimate_aggregate_revenue()` → ~$97B gross, ~$82B net at baseline.
- **migration_model.py**: Elasticity-based departure estimation with one-time-to-annual conversion (`ONE_TIME_TO_ANNUAL_FACTOR = 0.2`), anti-avoidance discount, firm-level effects (Sweden data), VC ecosystem impact. Core function: `compute_total_migration_costs()`.
- **spending_model.py**: Fiscal multiplier impacts for healthcare (1.5x), education (1.2x), food assistance (1.7x). Computes enrollee-years, jobs, GDP impact. Core function: `compute_total_spending_impact()`.
- **cost_benefit_model.py**: Integrates all three models into a year-by-year timeline (2027-2046) with NPV and sensitivity analysis. Core function: `compute_cost_benefit_timeline()` — takes ~30 parameters, returns dict with `summary`, `timeline` DataFrame, `revenue`, `migration`, `spending`.
- **scenarios.py**: Four pre-built scenarios (optimistic/baseline/pessimistic/extreme_flight). `get_scenario_params()` merges `COMMON_PARAMS` with scenario-specific params into a dict passable to `compute_cost_benefit_timeline(**params)`.

### Data Layer (src/data/)

- **baseline_data.py**: UC Berkeley report constants (204 billionaires, $2.19T wealth), tax parameters, wealth tiers, industry breakdown. Also contains VC investment constants (`CA_ANNUAL_VC_INVESTMENT_B`, `BILLIONAIRE_SHARE_OF_VC`).
- **california_fiscal.py**: State budget, Medi-Cal, education, food assistance, migration context. Contains `AVG_BILLIONAIRE_INCOME_TAX_M`.

All monetary constants are in **billions USD** unless the variable name ends in `_M` (millions).

### Key Modeling Decision

Published migration elasticities are for **annual** taxes. This is a **one-time** tax. The model converts via `effective_rate = tax_rate * 0.2` (5% one-time ≈ 1% annual equivalent over 5 years), then applies an anti-avoidance discount (default 30%). This is the most impactful and uncertain assumption in the entire model.

### Scenario Ordering Invariant

Tests enforce: optimistic NPV > baseline NPV > pessimistic NPV > extreme_flight NPV. All four scenarios produce positive NPV over 20 years.

## Deployment

Deployed on Streamlit Community Cloud. No secrets or API keys required — all data is hardcoded from public sources. The Forbes RTB API client (`src/data/billionaire_data.py`) exists but the app works entirely from baseline constants.

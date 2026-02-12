# Methodology

## Overview

This dashboard analyzes the proposed California 2026 Billionaire Tax Act (Initiative 25-0024) using four integrated models:

1. **Revenue Model** - Estimates gross and net one-time tax revenue
2. **Migration Model** - Estimates billionaire departures and economic costs
3. **Spending Model** - Estimates impact of revenue spending
4. **Cost-Benefit Model** - Integrates all models into a 20-year NPV timeline

## Revenue Model

### Inputs
- 204 California billionaires with $2.19 trillion collective wealth (UC Berkeley report, Dec 2025)
- 5% excise tax rate with phase-in between $1.0B and $1.1B
- Real estate exclusion (~10% of wealth)
- Pension/retirement exclusion (~1%)
- Compliance rate (baseline: 85%)
- Administrative cost ($15M-$300M, baseline: $150M)

### Calculation
```
Taxable_Wealth = Gross_Wealth × (1 - RE_Exclusion - Pension_Exclusion)
Gross_Tax = Σ Taxable_Wealth_i × Effective_Rate_i
Net_Revenue = Gross_Tax × Compliance_Rate - Admin_Cost
```

### Phase-In
The tax rate phases in linearly for net worth between $1.0B and $1.1B:
- At $1.0B: 0% effective rate
- At $1.05B: 2.5% effective rate
- At $1.1B+: 5% full rate

## Migration Model

### Elasticity-Based Departure Estimation

We use published migration elasticity estimates, adjusted for the one-time nature of the tax:

| Source | Elasticity | Population |
|--------|-----------|-----------|
| Young et al. 2016 | 0.06 | Millionaires (general) |
| Moretti & Wilson 2019 | 0.35 | Ultra-wealthy |
| Conservative bound | 1.0 | Upper bound estimate |
| Moretti & Wilson 2017 | 1.9 | Star scientists |

### One-Time Tax Adjustment

**Critical assumption**: Published elasticities are for annual taxes. We convert to a one-time equivalent:

```
effective_annual_rate = statutory_rate / 5 = 1%
```

This assumes a 5% one-time tax is behaviorally equivalent to a 1% annual tax over 5 years. This is a simplification - the actual behavioral response to a one-time levy is unknown.

### Anti-Avoidance Discount

The initiative includes anti-avoidance provisions:
- Residency determined as of January 1, 2026 (before ballot qualification)
- 25% minimum apportionment for partial residents

We apply a discount (baseline: 30%) to raw departure estimates.

### Cost Components

1. **Lost income tax**: departures × $50M/year average CA income tax per billionaire
2. **Firm-level effects**: Based on Munoz 2024 Swedish data, discounted 50% for CA tech context
3. **VC ecosystem**: Proportional loss of ~$22.5B billionaire VC investment

## Spending Model

### Allocation
- 90% healthcare
- 5% education
- 5% food assistance

### Fiscal Multipliers
- Healthcare: 1.5x (Richmond Fed Medicaid estimate)
- Education: 1.2x (CBO)
- Food assistance: 1.7x (USDA SNAP)

### Impact Metrics
- Healthcare: enrollee-years, direct jobs (15,000 per $1B)
- Education: teacher position-years ($92K avg salary+benefits)
- Food assistance: household-years served

## Cost-Benefit Integration

### Annual Benefits
- Tax revenue collected (including installment + interest)
- GDP impact from spending (distributed over spending_years)

### Annual Costs
- Administrative costs (year 1 only)
- Lost income tax from departures (ongoing)
- Firm-level economic losses (ongoing)
- VC ecosystem losses (ongoing)

### Net Present Value
```
NPV = Σ_{t=0}^{T} (Benefits_t - Costs_t) / (1 + r)^t
```

Default discount rate: 3% (OMB Circular A-94 standard for public policy).

## Scenarios

| Scenario | Elasticity | Compliance | Admin Cost | HC Multiplier | View |
|----------|-----------|-----------|-----------|--------------|------|
| Optimistic | 0.06 | 95% | $15M | 1.7x | Proponent |
| Baseline | 0.35 | 85% | $150M | 1.5x | Research-grounded |
| Pessimistic | 1.0 | 70% | $300M | 1.3x | Opponent |
| Extreme Flight | 1.9 | 60% | $300M | 1.2x | Worst case |

## Key Limitations

1. No precedent for US state-level wealth tax - compliance rate highly uncertain
2. One-time vs annual elasticity conversion is a major simplification
3. Firm-level effects from Sweden may not apply to CA tech sector
4. Legal challenges not modeled
5. General equilibrium effects not captured
6. Wealth measurement and valuation challenges simplified

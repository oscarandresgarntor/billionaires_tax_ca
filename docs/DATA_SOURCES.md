# Data Sources

## Primary Sources

### Forbes Real-Time Billionaires API (Primary Baseline)
- **Source**: github.com/komed3/rtb-api (community mirror of Forbes daily data)
- **What it provides**: Individual-level data for 250 CA billionaires ($2.25T), including name, net worth, industry, city, wealth source
- **Access**: Free JSON API via GitHub CDN (no auth required)
- **Confidence**: High — top holdings verifiable against SEC filings and public stock data
- **Used for**: Primary baseline for all model calculations
- **Data fetch**: Feb 11, 2026 — profiles for all 1,208 US billionaires fetched, filtered to California residents with net worth >= $1B
- **Note**: Forbes has tracked billionaires since 1987 with dedicated research teams

### UC Berkeley Expert Report (Cross-Reference)
- **Authors**: Brian Galle, David Gamage, Emmanuel Saez, Darien Shanske
- **Title**: "Revenue Estimate for the California Billionaire Tax Act"
- **Date**: December 2025
- **What it provides**: Cited 204 CA billionaires with $2.19T wealth
- **Confidence**: Medium — data sources and methodology not disclosed in the report
- **Used for**: Cross-reference only
- **Note**: The ~46-person gap vs Forbes is likely due to date differences (Dec 2025 vs Feb 2026), different residency definitions, and 59 billionaires near the $1B threshold who fluctuate with markets

### California Legislative Analyst's Office (2025)
- **What it provides**: Revenue order of magnitude ("tens of billions"), administrative cost range ($15M-$300M)
- **Access**: Public web
- **Confidence**: Medium
- **Used for**: Admin cost parameter range

## Migration Elasticity Literature

### Young, Varner, Lurie, & Prisinzano (2016)
- **Title**: "Millionaire Migration and Taxation of the Elite"
- **Source**: American Sociological Review, 81(3), 421-446
- **Finding**: Elasticity = 0.06 for millionaires
- **Relevance**: Lower bound for migration response

### Moretti & Wilson (2017)
- **Title**: "The Effect of State Taxes on the Geographical Location of Top Earners: Evidence from Star Scientists"
- **Source**: American Economic Review, 107(7), 1858-1903
- **Finding**: Elasticity = 1.9 for star scientists
- **Relevance**: Upper bound (highly mobile population)

### Moretti & Wilson (2019)
- **Title**: "Taxing Billionaires: Estate Taxes and the Geographical Location of the Ultra-Wealthy"
- **Source**: NBER Working Paper
- **Finding**: Elasticity = 0.35 for ultra-wealthy
- **Relevance**: Baseline elasticity estimate

### Munoz (2024)
- **Title**: "Do Wealth Taxes Affect Economic Growth? Evidence from Swedish Billionaires"
- **Finding**: Departures led to -33% employment, -34% value added, -50% tax payments at affected firms
- **Relevance**: Firm-level economic effects of billionaire departure

## Fiscal Multiplier Sources

### Federal Reserve Bank of Richmond
- **What**: Medicaid spending multiplier estimate (1.5x)
- **Used for**: Healthcare fiscal multiplier

### Congressional Budget Office (CBO)
- **What**: Government spending multiplier estimates
- **Used for**: Education fiscal multiplier (1.2x)

### USDA Economic Research Service
- **What**: SNAP multiplier analysis (1.5-1.7x)
- **Used for**: Food assistance fiscal multiplier

## State Fiscal Data

### California Franchise Tax Board / IRS Statistics of Income
- **What**: Personal income tax revenue (~$120B), concentration by income group, migration patterns
- **Confidence**: High
- **Used for**: Contextualizing migration costs, income tax loss estimates

## Data Freshness

- Baseline data: December 2025 (Berkeley report)
- Forbes API: Updated daily (cached for 24 hours in app)
- Fiscal data: Latest available (2023-2025 fiscal years)
- Elasticity estimates: Published 2016-2024

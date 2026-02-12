# Data Sources

## Primary Sources

### UC Berkeley Expert Report (December 2025)
- **Authors**: Brian Galle, David Gamage, Emmanuel Saez, Darien Shanske
- **Title**: "Revenue Estimate for the California Billionaire Tax Act"
- **What it provides**: Core dataset of 204 CA billionaires, $2.19T collective wealth, revenue estimation framework
- **Confidence**: High
- **Used for**: Baseline billionaire count, total wealth, revenue estimation

### Forbes Real-Time Billionaires API
- **Source**: github.com/komed3/rtb-api
- **What it provides**: Current net worth, industry classification, residence
- **Access**: Free JSON API via GitHub CDN
- **Confidence**: Medium (self-reported, estimates)
- **Used for**: Cross-referencing baseline data, industry breakdown
- **Note**: The app falls back to cached baseline data if the API is unavailable

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

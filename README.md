# California 2026 Billionaire Tax Act: Cost-Benefit Analyzer

An interactive public dashboard analyzing the proposed California 2026 Billionaire Tax Act (Initiative 25-0024), which would impose a one-time 5% excise tax on individuals with net worth exceeding $1 billion.

## What This Does

This tool provides a transparent, research-grounded cost-benefit analysis covering:

- **Revenue Estimation**: Gross and net revenue from the one-time tax (~$82-100B)
- **Migration & Economic Costs**: Billionaire departure risks and ongoing revenue losses
- **Spending Benefits**: Healthcare, education, and food assistance impacts
- **Integrated Cost-Benefit Timeline**: 20-year NPV analysis across scenarios
- **Scenario Explorer**: Full parameter sandbox for custom analysis

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Sources

- UC Berkeley expert report (Galle, Gamage, Saez, Shanske, Dec 2025)
- Forbes Real-Time Billionaires API
- CA Legislative Analyst's Office estimates
- Published migration elasticity studies (Young 2016, Moretti & Wilson 2017/2019)

## Testing

```bash
python -m pytest tests/ -v
```

## License

MIT

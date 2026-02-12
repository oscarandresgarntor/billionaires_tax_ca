"""Tests for the revenue estimation model."""

import pytest
import pandas as pd

from src.models.revenue_model import (
    compute_effective_tax_rate,
    compute_individual_tax,
    estimate_aggregate_revenue,
    compute_collection_timeline,
)


class TestEffectiveTaxRate:
    def test_below_threshold(self):
        """No tax below $1B."""
        assert compute_effective_tax_rate(0.5) == 0.0
        assert compute_effective_tax_rate(0.99) == 0.0
        assert compute_effective_tax_rate(1.0) == 0.0

    def test_above_ceiling(self):
        """Full rate above $1.1B."""
        assert compute_effective_tax_rate(1.1) == 0.05
        assert compute_effective_tax_rate(5.0) == 0.05
        assert compute_effective_tax_rate(100.0) == 0.05

    def test_phase_in_midpoint(self):
        """Half rate at $1.05B (midpoint of phase-in)."""
        rate = compute_effective_tax_rate(1.05)
        assert abs(rate - 0.025) < 1e-10

    def test_phase_in_quarter(self):
        """Quarter rate at $1.025B."""
        rate = compute_effective_tax_rate(1.025)
        assert abs(rate - 0.0125) < 1e-10

    def test_custom_rate(self):
        """Works with custom tax rates."""
        assert compute_effective_tax_rate(5.0, tax_rate=0.10) == 0.10
        assert compute_effective_tax_rate(1.05, tax_rate=0.10) == 0.05


class TestIndividualTax:
    def test_basic_calculation(self):
        """Basic individual tax calculation."""
        result = compute_individual_tax(10.0)
        assert result["gross_worth_b"] == 10.0
        assert result["effective_rate"] == 0.05
        # Taxable = 10 * (1 - 0.10 - 0.01) = 8.9
        assert abs(result["taxable_wealth_b"] - 8.9) < 0.01
        # Tax = 8.9 * 0.05 = 0.445
        assert abs(result["tax_owed_b"] - 0.445) < 0.001

    def test_below_threshold(self):
        """No tax for sub-billionaire."""
        result = compute_individual_tax(0.5)
        assert result["tax_owed_b"] == 0.0

    def test_exclusions(self):
        """Exclusions reduce taxable wealth."""
        result = compute_individual_tax(10.0, real_estate_exclusion=0.20)
        # Taxable = 10 * (1 - 0.20 - 0.01) = 7.9
        assert abs(result["taxable_wealth_b"] - 7.9) < 0.01


class TestAggregateRevenue:
    def test_baseline_gross_revenue_range(self):
        """Gross revenue should be ~$97-100B with baseline data."""
        result = estimate_aggregate_revenue()
        assert 90 <= result["gross_tax_b"] <= 110

    def test_net_revenue_less_than_gross(self):
        """Net revenue should be less than gross."""
        result = estimate_aggregate_revenue()
        assert result["net_revenue_b"] < result["gross_tax_b"]

    def test_compliance_reduces_revenue(self):
        """Lower compliance = lower revenue."""
        high = estimate_aggregate_revenue(compliance_rate=0.95)
        low = estimate_aggregate_revenue(compliance_rate=0.60)
        assert high["net_revenue_b"] > low["net_revenue_b"]

    def test_admin_cost_reduces_revenue(self):
        """Higher admin cost = lower net revenue."""
        low_admin = estimate_aggregate_revenue(admin_cost_m=15)
        high_admin = estimate_aggregate_revenue(admin_cost_m=300)
        assert low_admin["net_revenue_b"] > high_admin["net_revenue_b"]

    def test_with_dataframe(self):
        """Works with individual billionaire DataFrame."""
        df = pd.DataFrame({
            "net_worth_b": [5.0, 10.0, 20.0],
            "estimated_re_pct": [0.10, 0.10, 0.10],
        })
        result = estimate_aggregate_revenue(billionaire_df=df)
        assert result["n_billionaires"] == 3
        assert result["gross_tax_b"] > 0


class TestCollectionTimeline:
    def test_timeline_length(self):
        """Timeline should be 5 years."""
        timeline = compute_collection_timeline(100.0)
        assert len(timeline) == 5

    def test_total_exceeds_input(self):
        """Total collected (with interest) should exceed input."""
        timeline = compute_collection_timeline(100.0, installment_pct=0.50)
        total = timeline["total_b"].sum()
        assert total > 100.0  # Interest makes total > principal

    def test_lump_sum_in_year_one(self):
        """Lump sum should be collected in year 1 only."""
        timeline = compute_collection_timeline(100.0, installment_pct=0.40)
        assert timeline.iloc[0]["lump_sum_b"] > 0
        assert timeline.iloc[1]["lump_sum_b"] == 0

    def test_no_installment(self):
        """All lump sum scenario."""
        timeline = compute_collection_timeline(100.0, installment_pct=0.0)
        assert timeline.iloc[0]["lump_sum_b"] == 100.0

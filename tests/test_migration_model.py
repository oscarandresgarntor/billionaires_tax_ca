"""Tests for the migration and economic cost model."""

import pytest

from src.models.migration_model import (
    estimate_departures,
    estimate_annual_income_tax_loss,
    estimate_firm_level_effects,
    estimate_vc_ecosystem_impact,
    compute_total_migration_costs,
)


class TestEstimateDepartures:
    def test_zero_elasticity(self):
        """Zero elasticity = zero departures."""
        result = estimate_departures(elasticity=0.0)
        assert result["estimated_departures"] == 0.0

    def test_higher_elasticity_more_departures(self):
        """Higher elasticity should produce more departures."""
        low = estimate_departures(elasticity=0.06)
        mid = estimate_departures(elasticity=0.35)
        high = estimate_departures(elasticity=1.0)
        assert low["estimated_departures"] < mid["estimated_departures"]
        assert mid["estimated_departures"] < high["estimated_departures"]

    def test_one_time_adjustment_reduces_departures(self):
        """One-time adjustment should reduce departures vs unadjusted."""
        adjusted = estimate_departures(elasticity=0.35, one_time_adjustment=True)
        unadjusted = estimate_departures(elasticity=0.35, one_time_adjustment=False)
        assert adjusted["estimated_departures"] < unadjusted["estimated_departures"]

    def test_anti_avoidance_reduces_departures(self):
        """Anti-avoidance discount should reduce departures."""
        low_discount = estimate_departures(anti_avoidance_discount=0.10)
        high_discount = estimate_departures(anti_avoidance_discount=0.50)
        assert high_discount["estimated_departures"] < low_discount["estimated_departures"]

    def test_departures_capped(self):
        """Departures should never exceed total billionaires."""
        result = estimate_departures(
            num_billionaires=204,
            elasticity=100.0,
            one_time_adjustment=False,
            anti_avoidance_discount=0.0,
        )
        assert result["estimated_departures"] <= 204

    def test_baseline_departures_reasonable(self):
        """Baseline departures should be in a reasonable range."""
        result = estimate_departures(elasticity=0.35)
        # With one-time adjustment (÷5) and anti-avoidance (30%), departures are small
        assert 0 <= result["estimated_departures"] <= 30


class TestIncomeTaxLoss:
    def test_basic_calculation(self):
        """Basic income tax loss calculation."""
        result = estimate_annual_income_tax_loss(10, avg_income_tax_m=50)
        assert result["annual_lost_income_tax_m"] == 500
        assert abs(result["annual_lost_income_tax_b"] - 0.5) < 0.01

    def test_zero_departures(self):
        """Zero departures = zero loss."""
        result = estimate_annual_income_tax_loss(0)
        assert result["annual_lost_income_tax_m"] == 0


class TestFirmLevelEffects:
    def test_basic_calculation(self):
        """Firm effects should be positive (loss)."""
        result = estimate_firm_level_effects(10)
        assert result["estimated_revenue_loss_b"] > 0

    def test_zero_departures(self):
        """Zero departures = zero firm effects."""
        result = estimate_firm_level_effects(0)
        assert result["estimated_revenue_loss_b"] == 0

    def test_discount_reduces_effects(self):
        """Higher CA discount should reduce firm effects."""
        low = estimate_firm_level_effects(10, firm_effect_discount=0.25)
        high = estimate_firm_level_effects(10, firm_effect_discount=0.75)
        assert high["estimated_revenue_loss_b"] < low["estimated_revenue_loss_b"]


class TestVCEcosystemImpact:
    def test_basic_calculation(self):
        """VC impact should scale with departures."""
        result = estimate_vc_ecosystem_impact(10, 204)
        assert result["lost_vc_annual_b"] > 0
        assert result["total_economic_impact_b"] > result["lost_vc_annual_b"]

    def test_zero_departures(self):
        """Zero departures = zero VC impact."""
        result = estimate_vc_ecosystem_impact(0, 204)
        assert result["lost_vc_annual_b"] == 0


class TestTotalMigrationCosts:
    def test_returns_timeline(self):
        """Should return a timeline DataFrame."""
        result = compute_total_migration_costs(horizon_years=20)
        assert len(result["timeline"]) == 20

    def test_cumulative_increases(self):
        """Cumulative cost should increase over time."""
        result = compute_total_migration_costs(horizon_years=10)
        timeline = result["timeline"]
        for i in range(1, len(timeline)):
            assert timeline.iloc[i]["cumulative_loss_b"] >= timeline.iloc[i-1]["cumulative_loss_b"]

    def test_zero_elasticity_zero_cost(self):
        """Zero elasticity should produce zero migration costs."""
        result = compute_total_migration_costs(elasticity=0.0)
        assert result["annual_total_cost_b"] == 0
        assert result["cumulative_cost_b"] == 0

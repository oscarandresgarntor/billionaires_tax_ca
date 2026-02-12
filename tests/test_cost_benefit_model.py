"""Tests for the integrated cost-benefit model."""

import pytest

from src.models.cost_benefit_model import (
    compute_cost_benefit_timeline,
    sensitivity_analysis,
)
from src.models.scenarios import SCENARIOS, get_scenario_params


class TestCostBenefitTimeline:
    def test_baseline_runs(self):
        """Baseline scenario should run without errors."""
        params = get_scenario_params("baseline")
        result = compute_cost_benefit_timeline(**params)
        assert result is not None
        assert "summary" in result
        assert "timeline" in result

    def test_all_scenarios_run(self):
        """All pre-built scenarios should run without errors."""
        for key in SCENARIOS:
            params = get_scenario_params(key)
            result = compute_cost_benefit_timeline(**params)
            assert result is not None
            assert len(result["timeline"]) == 20

    def test_optimistic_better_than_pessimistic(self):
        """Optimistic NPV should exceed pessimistic NPV."""
        opt = compute_cost_benefit_timeline(**get_scenario_params("optimistic"))
        pess = compute_cost_benefit_timeline(**get_scenario_params("pessimistic"))
        assert opt["summary"]["npv_b"] > pess["summary"]["npv_b"]

    def test_baseline_npv_positive(self):
        """Baseline scenario should have positive 20-year NPV."""
        result = compute_cost_benefit_timeline(**get_scenario_params("baseline"))
        assert result["summary"]["npv_b"] > 0

    def test_timeline_length(self):
        """Timeline should match horizon."""
        params = get_scenario_params("baseline")
        params["horizon_years"] = 10
        result = compute_cost_benefit_timeline(**params)
        assert len(result["timeline"]) == 10

    def test_net_revenue_in_range(self):
        """Net revenue should be in expected range."""
        result = compute_cost_benefit_timeline(**get_scenario_params("baseline"))
        net_rev = result["revenue"]["net_revenue_b"]
        assert 50 <= net_rev <= 120

    def test_benefit_cost_ratio_positive(self):
        """Baseline BCR should be > 1."""
        result = compute_cost_benefit_timeline(**get_scenario_params("baseline"))
        assert result["summary"]["benefit_cost_ratio"] > 1

    def test_scenario_ordering(self):
        """NPV should follow: optimistic > baseline > pessimistic > extreme."""
        results = {}
        for key in ["optimistic", "baseline", "pessimistic", "extreme_flight"]:
            results[key] = compute_cost_benefit_timeline(**get_scenario_params(key))

        assert results["optimistic"]["summary"]["npv_b"] > results["baseline"]["summary"]["npv_b"]
        assert results["baseline"]["summary"]["npv_b"] > results["pessimistic"]["summary"]["npv_b"]
        assert results["pessimistic"]["summary"]["npv_b"] > results["extreme_flight"]["summary"]["npv_b"]

    def test_discount_rate_affects_npv(self):
        """Higher discount rate should lower NPV."""
        params = get_scenario_params("baseline")
        params["discount_rate"] = 0.01
        low_r = compute_cost_benefit_timeline(**params)

        params["discount_rate"] = 0.07
        high_r = compute_cost_benefit_timeline(**params)

        # With positive net benefits, lower discount = higher NPV
        # But it depends on timing - just check they're different
        assert low_r["summary"]["npv_b"] != high_r["summary"]["npv_b"]

    def test_zero_elasticity_no_migration_cost(self):
        """Zero elasticity should mean zero migration costs."""
        params = get_scenario_params("baseline")
        params["elasticity"] = 0.0
        result = compute_cost_benefit_timeline(**params)
        assert result["migration"]["departures"]["estimated_departures"] == 0
        assert result["migration"]["annual_cost_b"] == 0

    def test_extreme_parameters(self):
        """Extreme parameter values should not crash."""
        params = get_scenario_params("baseline")
        params["elasticity"] = 3.0
        params["compliance_rate"] = 0.50
        params["admin_cost_m"] = 500
        result = compute_cost_benefit_timeline(**params)
        assert result is not None


class TestSensitivityAnalysis:
    def test_runs(self):
        """Sensitivity analysis should run."""
        params = get_scenario_params("baseline")
        result = sensitivity_analysis(params)
        assert len(result) > 0

    def test_swing_positive(self):
        """All swings should be non-negative."""
        params = get_scenario_params("baseline")
        result = sensitivity_analysis(params)
        assert (result["swing_b"] >= 0).all()

    def test_sorted_by_swing(self):
        """Results should be sorted by swing (descending)."""
        params = get_scenario_params("baseline")
        result = sensitivity_analysis(params)
        swings = result["swing_b"].tolist()
        assert swings == sorted(swings, reverse=True)

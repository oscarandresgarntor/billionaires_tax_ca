"""Tests for the spending impact model."""

import pytest

from src.models.spending_model import (
    allocate_revenue,
    estimate_healthcare_impact,
    estimate_education_impact,
    estimate_food_assistance_impact,
    compute_total_spending_impact,
)


class TestAllocateRevenue:
    def test_default_allocation(self):
        """Default allocation sums to total."""
        alloc = allocate_revenue(100.0)
        total = alloc["healthcare_b"] + alloc["education_b"] + alloc["food_assistance_b"]
        assert abs(total - 100.0) < 0.01

    def test_percentages(self):
        """Default percentages are 90/5/5."""
        alloc = allocate_revenue(100.0)
        assert alloc["healthcare_b"] == 90.0
        assert alloc["education_b"] == 5.0
        assert alloc["food_assistance_b"] == 5.0

    def test_custom_allocation(self):
        """Custom allocation works."""
        alloc = allocate_revenue(100.0, healthcare_pct=0.80, education_pct=0.10, food_pct=0.10)
        assert alloc["healthcare_b"] == 80.0
        assert alloc["education_b"] == 10.0


class TestHealthcareImpact:
    def test_positive_impact(self):
        """Healthcare spending should produce positive impact."""
        result = estimate_healthcare_impact(75.0)
        assert result["gdp_impact_b"] > 0
        assert result["total_enrollee_years"] > 0
        assert result["direct_jobs_created"] > 0

    def test_multiplier_effect(self):
        """GDP impact should equal spending * multiplier."""
        result = estimate_healthcare_impact(75.0, multiplier=1.5)
        assert abs(result["gdp_impact_b"] - 75.0 * 1.5) < 0.1

    def test_higher_multiplier_more_impact(self):
        """Higher multiplier = higher GDP impact."""
        low = estimate_healthcare_impact(75.0, multiplier=1.2)
        high = estimate_healthcare_impact(75.0, multiplier=1.8)
        assert high["gdp_impact_b"] > low["gdp_impact_b"]


class TestEducationImpact:
    def test_positive_impact(self):
        """Education spending should produce positive impact."""
        result = estimate_education_impact(5.0)
        assert result["gdp_impact_b"] > 0
        assert result["total_teacher_position_years"] > 0

    def test_teacher_positions_reasonable(self):
        """Teacher positions should be reasonable count."""
        result = estimate_education_impact(5.0, spending_years=5)
        # ~$92K per teacher, $1B/year, so ~10,870 per year
        assert result["annual_teacher_positions"] > 5000
        assert result["annual_teacher_positions"] < 50000


class TestFoodAssistanceImpact:
    def test_positive_impact(self):
        """Food spending should produce positive impact."""
        result = estimate_food_assistance_impact(5.0)
        assert result["gdp_impact_b"] > 0
        assert result["total_household_years"] > 0

    def test_high_multiplier(self):
        """Food assistance should have higher multiplier than education."""
        food = estimate_food_assistance_impact(5.0, multiplier=1.7)
        edu = estimate_education_impact(5.0, multiplier=1.2)
        assert food["gdp_impact_b"] > edu["gdp_impact_b"]


class TestTotalSpendingImpact:
    def test_total_gdp_impact(self):
        """Total GDP impact should be sum of components."""
        result = compute_total_spending_impact(100.0)
        component_sum = (
            result["healthcare"]["gdp_impact_b"]
            + result["education"]["gdp_impact_b"]
            + result["food_assistance"]["gdp_impact_b"]
        )
        assert abs(result["total_gdp_impact_b"] - component_sum) < 0.1

    def test_weighted_multiplier(self):
        """Weighted multiplier should be between min and max component."""
        result = compute_total_spending_impact(100.0)
        mult = result["weighted_avg_multiplier"]
        assert mult >= 1.0
        assert mult <= 2.0

    def test_allocation_sums(self):
        """Allocation should sum to net revenue."""
        result = compute_total_spending_impact(100.0)
        alloc = result["allocation"]
        total = alloc["healthcare_b"] + alloc["education_b"] + alloc["food_assistance_b"]
        assert abs(total - 100.0) < 0.1

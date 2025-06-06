import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import health


def test_calculate_bmi():
    assert round(health.calculate_bmi(70, 1.75), 2) == 22.86
    with pytest.raises(ValueError):
        health.calculate_bmi(70, 0)

def test_bmi_category():
    assert health.bmi_category(17) == "Underweight"
    assert health.bmi_category(22) == "Normal weight"
    assert health.bmi_category(27) == "Overweight"
    assert health.bmi_category(32) == "Obesity"

def test_recommend_plan():
    assert "underweight" in health.recommend_plan(17).lower()
    assert "normal" in health.recommend_plan(22).lower()
    assert "overweight" in health.recommend_plan(27).lower()
    assert "obese" in health.recommend_plan(32).lower()

def test_total_daily_calories():
    assert health.total_daily_calories([100, 200, 300]) == 600

def test_suggest_foods():
    assert "tacos de pollo" in health.suggest_foods("mexico")
    assert "paella" in health.suggest_foods("spain")
    assert health.suggest_foods("unknown") == []

def test_age_recommendation():
    assert "pediatric" in health.age_recommendation(10).lower()
    assert "exercise" in health.age_recommendation(30).lower()
    assert "flexibility" in health.age_recommendation(70).lower()

def test_estimate_burned_calories():
    assert health.estimate_burned_calories(1000) == 40.0

def test_lookup_calories():
    assert health.lookup_calories("0123456789") == 150
    assert health.lookup_calories("0000000000") is None

def test_smart_calorie_goal():
    history = [{"total_calories": 2100}] * 7
    assert health.smart_calorie_goal(history, 17) > 2100
    assert health.smart_calorie_goal(history, 22) == 2100
    assert health.smart_calorie_goal(history, 27) < 2100
    assert health.smart_calorie_goal([], 17) == 2300

def test_calculate_points():
    assert health.calculate_points(1800, 2000) == 10
    assert health.calculate_points(2200, 2000) == 5

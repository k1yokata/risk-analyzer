import pandas as pd

from src.risk_scoring import get_risk_level, calculate_risk_score


def test_get_risk_level_low():
    assert get_risk_level(10) == "Low"
    assert get_risk_level(39) == "Low"


def test_get_risk_level_medium():
    assert get_risk_level(40) == "Medium"
    assert get_risk_level(69) == "Medium"


def test_get_risk_level_high():
    assert get_risk_level(70) == "High"
    assert get_risk_level(100) == "High"


def test_calculate_risk_score_adds_required_columns():
    df = pd.DataFrame({
        "is_single_bidder": [1, 0],
        "number_of_tenderers": [1, 5],
        "is_competitive": [0, 1],
        "tender_value": [1000000, 100],
        "has_cancelled_awards": [1, 0],
        "has_unsuccessful_awards": [1, 0],
        "price_change_pct": [25, 0],
        "award_concentration": [0.9, 0.1],
    })

    result = calculate_risk_score(df)

    assert "single_bidder_risk" in result.columns
    assert "low_competition_risk" in result.columns
    assert "high_value_risk" in result.columns
    assert "cancelled_awards_risk" in result.columns
    assert "unsuccessful_awards_risk" in result.columns
    assert "price_change_risk" in result.columns
    assert "award_concentration_risk" in result.columns
    assert "risk_score" in result.columns
    assert "risk_level" in result.columns
    assert "risk_reasons" in result.columns


def test_calculate_risk_score_values():
    df = pd.DataFrame({
        "is_single_bidder": [1, 0],
        "number_of_tenderers": [1, 5],
        "is_competitive": [0, 1],
        "tender_value": [1000000, 100],
        "has_cancelled_awards": [1, 0],
        "has_unsuccessful_awards": [1, 0],
        "price_change_pct": [25, 0],
        "award_concentration": [0.9, 0.1],
    })

    result = calculate_risk_score(df)

    assert result.loc[0, "risk_score"] == 110
    assert result.loc[0, "risk_level"] == "High"
    assert "Single bidder participation" in result.loc[0, "risk_reasons"]

    assert result.loc[1, "risk_score"] == 0
    assert result.loc[1, "risk_level"] == "Low"
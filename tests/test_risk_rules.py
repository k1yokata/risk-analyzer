import pandas as pd

from src.risk_rules import (
    calculate_single_bidder_risk,
    calculate_low_competition_risk,
    calculate_high_value_risk,
    calculate_cancelled_awards_risk,
    calculate_unsuccessful_awards_risk,
    calculate_price_change_risk,
    calculate_award_concentration_risk,
)


def test_single_bidder_risk_by_is_single_bidder():
    df = pd.DataFrame({
        "is_single_bidder": [1, 0],
        "number_of_tenderers": [3, 3],
    })

    result = calculate_single_bidder_risk(df)

    assert result.tolist() == [30, 0]


def test_single_bidder_risk_by_number_of_tenderers():
    df = pd.DataFrame({
        "number_of_tenderers": [1, 3],
    })

    result = calculate_single_bidder_risk(df)

    assert result.tolist() == [30, 0]


def test_low_competition_risk():
    df = pd.DataFrame({
        "is_competitive": [0, 1],
    })

    result = calculate_low_competition_risk(df)

    assert result.tolist() == [20, 0]


def test_high_value_risk():
    df = pd.DataFrame({
        "tender_value": [100, 200, 300],
    })

    result = calculate_high_value_risk(df)

    assert result.tolist() == [0, 0, 15]


def test_cancelled_awards_risk():
    df = pd.DataFrame({
        "has_cancelled_awards": [1, 0],
    })

    result = calculate_cancelled_awards_risk(df)

    assert result.tolist() == [15, 0]


def test_unsuccessful_awards_risk():
    df = pd.DataFrame({
        "has_unsuccessful_awards": [1, 0],
    })

    result = calculate_unsuccessful_awards_risk(df)

    assert result.tolist() == [10, 0]


def test_price_change_risk():
    df = pd.DataFrame({
        "price_change_pct": [25, -30, 10],
    })

    result = calculate_price_change_risk(df)

    assert result.tolist() == [10, 10, 0]


def test_award_concentration_risk():
    df = pd.DataFrame({
        "award_concentration": [0.9, 0.5],
    })

    result = calculate_award_concentration_risk(df)

    assert result.tolist() == [10, 0]
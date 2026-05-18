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


def get_risk_level(score: int) -> str:
    """
    Converts numeric risk score into risk level.
    """

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    return "Low"


def build_risk_reasons(row: pd.Series) -> str:
    """
    Creates readable explanation for each risk score.
    """

    reasons = []

    if row.get("single_bidder_risk", 0) > 0:
        reasons.append("Single bidder participation")

    if row.get("low_competition_risk", 0) > 0:
        reasons.append("Low competition")

    if row.get("high_value_risk", 0) > 0:
        reasons.append("High tender value")

    if row.get("cancelled_awards_risk", 0) > 0:
        reasons.append("Cancelled awards")

    if row.get("unsuccessful_awards_risk", 0) > 0:
        reasons.append("Unsuccessful awards")

    if row.get("price_change_risk", 0) > 0:
        reasons.append("Significant price change")

    if row.get("award_concentration_risk", 0) > 0:
        reasons.append("High award concentration")

    if not reasons:
        return "No significant risk indicators"

    return ", ".join(reasons)


def calculate_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates corruption risk score for ProZorro procurement data.
    """

    df = df.copy()

    df["single_bidder_risk"] = calculate_single_bidder_risk(df)
    df["low_competition_risk"] = calculate_low_competition_risk(df)
    df["high_value_risk"] = calculate_high_value_risk(df)
    df["cancelled_awards_risk"] = calculate_cancelled_awards_risk(df)
    df["unsuccessful_awards_risk"] = calculate_unsuccessful_awards_risk(df)
    df["price_change_risk"] = calculate_price_change_risk(df)
    df["award_concentration_risk"] = calculate_award_concentration_risk(df)

    df["risk_score"] = (
        df["single_bidder_risk"]
        + df["low_competition_risk"]
        + df["high_value_risk"]
        + df["cancelled_awards_risk"]
        + df["unsuccessful_awards_risk"]
        + df["price_change_risk"]
        + df["award_concentration_risk"]
    )

    df["risk_level"] = df["risk_score"].apply(get_risk_level)
    df["risk_reasons"] = df.apply(build_risk_reasons, axis=1)

    return df
import pandas as pd


def safe_numeric(series: pd.Series) -> pd.Series:
    """
    Converts a pandas Series to numeric values safely.
    """
    return pd.to_numeric(series, errors="coerce").fillna(0)


def calculate_single_bidder_risk(df: pd.DataFrame) -> pd.Series:
    """
    High risk if tender has only one bidder.
    Uses is_single_bidder or number_of_tenderers.
    """

    if "is_single_bidder" in df.columns:
        values = safe_numeric(df["is_single_bidder"])
        return values.apply(lambda x: 30 if x == 1 else 0)

    if "number_of_tenderers" in df.columns:
        values = safe_numeric(df["number_of_tenderers"])
        return values.apply(lambda x: 30 if x == 1 else 0)

    return pd.Series([0] * len(df), index=df.index)


def calculate_low_competition_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if procurement is not competitive.
    """

    if "is_competitive" in df.columns:
        values = safe_numeric(df["is_competitive"])
        return values.apply(lambda x: 20 if x == 0 else 0)

    return pd.Series([0] * len(df), index=df.index)


def calculate_high_value_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if tender value is higher than the dataset median.
    """

    if "tender_value" not in df.columns:
        return pd.Series([0] * len(df), index=df.index)

    values = safe_numeric(df["tender_value"])

    if values.sum() == 0:
        return pd.Series([0] * len(df), index=df.index)

    median_value = values.median()

    return values.apply(lambda x: 15 if x > median_value else 0)


def calculate_cancelled_awards_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if tender has cancelled awards.
    """

    if "has_cancelled_awards" in df.columns:
        values = safe_numeric(df["has_cancelled_awards"])
        return values.apply(lambda x: 15 if x == 1 else 0)

    return pd.Series([0] * len(df), index=df.index)


def calculate_unsuccessful_awards_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if tender has unsuccessful awards.
    """

    if "has_unsuccessful_awards" in df.columns:
        values = safe_numeric(df["has_unsuccessful_awards"])
        return values.apply(lambda x: 10 if x == 1 else 0)

    return pd.Series([0] * len(df), index=df.index)


def calculate_price_change_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if price change percentage is unusually high.
    """

    if "price_change_pct" not in df.columns:
        return pd.Series([0] * len(df), index=df.index)

    values = safe_numeric(df["price_change_pct"])

    return values.apply(lambda x: 10 if abs(x) >= 20 else 0)


def calculate_award_concentration_risk(df: pd.DataFrame) -> pd.Series:
    """
    Risk if award concentration is high.
    """

    if "award_concentration" not in df.columns:
        return pd.Series([0] * len(df), index=df.index)

    values = safe_numeric(df["award_concentration"])

    return values.apply(lambda x: 10 if x >= 0.8 else 0)
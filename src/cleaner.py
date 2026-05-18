import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts column names to a standard format.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace(".", "_")
    )

    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning for uploaded procurement data.
    """

    df = df.copy()

    df = normalize_columns(df)

    df = df.drop_duplicates()

    df = df.dropna(how="all")

    return df
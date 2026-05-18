import pandas as pd

from src.cleaner import normalize_columns, clean_dataframe


def test_normalize_columns():
    df = pd.DataFrame({
        "Tender ID": [1],
        "Tender-Value": [1000],
        "Price.Change.Pct": [10],
    })

    result = normalize_columns(df)

    assert list(result.columns) == [
        "tender_id",
        "tender_value",
        "price_change_pct",
    ]


def test_clean_dataframe_removes_duplicates():
    df = pd.DataFrame({
        "Tender ID": [1, 1, 2],
        "Tender Value": [1000, 1000, 2000],
    })

    result = clean_dataframe(df)

    assert len(result) == 2
    assert "tender_id" in result.columns
    assert "tender_value" in result.columns


def test_clean_dataframe_removes_empty_rows():
    df = pd.DataFrame({
        "Tender ID": [1, None],
        "Tender Value": [1000, None],
    })

    result = clean_dataframe(df)

    assert len(result) == 1
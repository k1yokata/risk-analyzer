import pandas as pd


def load_csv(file_path: str, nrows: int | None = None) -> pd.DataFrame:
    """
    Loads CSV file into pandas DataFrame.
    nrows is used to load only part of large files.
    """
    try:
        return pd.read_csv(file_path, nrows=nrows, low_memory=False)
    except Exception as error:
        raise RuntimeError(f"Error loading CSV file: {error}")


def save_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Saves DataFrame to CSV file.
    """
    df.to_csv(file_path, index=False)
import pandas as pd
from pathlib import Path

files = [
    "tenders_2025.csv",
    "bids_2025.csv",
    "buyers.csv",
    "suppliers.csv",
    "bidders.csv",
]

for file_name in files:
    file_path = Path("data/raw") / file_name

    print("=" * 80)
    print(file_name)

    df = pd.read_csv(file_path, nrows=5, low_memory=False)

    print("Shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())

    print("Preview:")
    print(df.head())
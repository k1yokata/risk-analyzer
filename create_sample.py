import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/tenders_2025.csv")
OUTPUT_PATH = Path("data/processed/tenders_2025_sample.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, nrows=5000, low_memory=False)

df.to_csv(OUTPUT_PATH, index=False)

print("Sample file created:")
print(OUTPUT_PATH)
print(df.shape)
print(df.columns.tolist())
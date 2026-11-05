
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATA_FILE = (
    PROJECT_ROOT / "data" / "raw" / "sales_data.csv"
)


def load_sales_data(
    file_path: str | Path = DEFAULT_DATA_FILE,
) -> pd.DataFrame:
    """
    Load sales records from a CSV file.

    Returns a Pandas DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Sales data file not found: {path}"
        )

    df = pd.read_csv(path)

    return df


def inspect_sales_data(df: pd.DataFrame) -> None:
  
    """Print a basic overview of the sales dataset."""

    print("\n========== SALES DATA OVERVIEW ==========")

    print(f"\nTotal records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst five records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate order IDs:")
    print(df["order_id"].duplicated().sum())

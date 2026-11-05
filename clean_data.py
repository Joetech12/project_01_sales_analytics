
import pandas as pd
from pathlib import Path


# 1. Define our file locations.
RAW_FILE = Path("data/raw/messy_sales.csv")

PROCESSED_FOLDER = Path("data/processed")

CLEAN_FILE = PROCESSED_FOLDER / "cleaned_sales.csv"


# 2. Load the original data.
sales = pd.read_csv(RAW_FILE)

original_count = len(sales)

print("\n========== DATA CLEANING ==========")

print(f"Original records: {original_count}")


# 3. Remove duplicate orders.
sales = sales.drop_duplicates(
    subset=["order_id"],
    keep="first",
)

# 4. Convert quantity and price into numbers.
sales["quantity"] = pd.to_numeric(
    sales["quantity"],
    errors="coerce",
)

sales["price"] = pd.to_numeric(
    sales["price"],
    errors="coerce",
)


# 5. Remove records missing important information.
sales = sales.dropna(
    subset=[
        "order_id",
        "product",
        "category",
        "quantity",
        "price",
    ]
)


# 6. Remove invalid quantities and prices.
sales = sales[
    (sales["quantity"] > 0)
    & (sales["price"] >= 0)
].copy()


# 7. Calculate revenue for valid records.
sales["revenue"] = (
    sales["quantity"] * sales["price"]
)


# 8. Create the processed-data folder.
PROCESSED_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)


# 9. Save the cleaned dataset.
sales.to_csv(
    CLEAN_FILE,
    index=False,
)


# 10. Display the cleaning summary.
cleaned_count = len(sales)

removed_count = original_count - cleaned_count

print(f"Cleaned records: {cleaned_count}")
print(f"Removed records: {removed_count}")

print(f"\nCleaned data saved to: {CLEAN_FILE}")

print("\n========== CLEANED SALES DATA ==========")

print(sales)

print("\nData cleaning completed successfully.")


import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "price",
    "unit_cost",
]


def clean_sales_data(sales: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sales records and calculate revenue and profit.
    """

    sales = sales.copy()

    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in sales.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Remove duplicate orders
    sales = sales.drop_duplicates(
        subset=["order_id"],
        keep="first",
    )

    # Convert numeric columns
    numeric_columns = [
        "quantity",
        "price",
        "unit_cost",
    ]

    for column in numeric_columns:
        sales[column] = pd.to_numeric(
            sales[column],
            errors="coerce",
        )

    # Convert dates
    sales["order_date"] = pd.to_datetime(
        sales["order_date"],
        errors="coerce",
    )

    # Remove records with missing required values
    sales = sales.dropna(
        subset=REQUIRED_COLUMNS
    )

    # Remove invalid values
    sales = sales[
        (sales["quantity"] > 0)
        & (sales["price"] >= 0)
        & (sales["unit_cost"] >= 0)
        & (sales["price"] >= sales["unit_cost"])
    ].copy()

    # Calculate revenue
    sales["revenue"] = (
        sales["quantity"] * sales["price"]
    )

    # Calculate total cost
    sales["total_cost"] = (
        sales["quantity"] * sales["unit_cost"]
    )

    # Calculate gross profit
    sales["gross_profit"] = (
        sales["revenue"] - sales["total_cost"]
    )

    # Calculate profit margin
    sales["profit_margin"] = (
        sales["gross_profit"]
        / sales["revenue"].replace(0, float("nan"))
    ) * 100

    return sales.reset_index(drop=True)

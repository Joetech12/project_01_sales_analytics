
from src.data.loader import (
    inspect_sales_data,
    load_sales_data,
)


def main() -> None:
    sales_df = load_sales_data()

    inspect_sales_data(sales_df)


if __name__ == "__main__":
    main()

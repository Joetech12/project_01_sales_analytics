
import pandas as pd

from data_cleaner import clean_sales_data


# Load and clean sales data
raw_sales = pd.read_csv("data/raw/sales.csv")
sales = clean_sales_data(raw_sales)


# Calculate business KPIs
total_revenue = sales["revenue"].sum()
total_cost = sales["total_cost"].sum()
total_profit = sales["gross_profit"].sum()

profit_margin = (
    total_profit / total_revenue
) * 100


# Display results
print("\nSALES PERFORMANCE")
print("-------------------------")

print(f"Total Revenue: ₦{total_revenue:,.2f}")
print(f"Total Cost: ₦{total_cost:,.2f}")
print(f"Gross Profit: ₦{total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")


# Product profitability
product_performance = (
    sales.groupby("product")
    .agg(
        revenue=("revenue", "sum"),
        cost=("total_cost", "sum"),
        gross_profit=("gross_profit", "sum"),
    )
    .sort_values(
        by="gross_profit",
        ascending=False,
    )
)

print("\nPRODUCT PROFITABILITY")
print("-------------------------")
print(product_performance)

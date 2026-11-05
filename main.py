
import pandas as pd


# Load sales data.
sales = pd.read_csv("data/raw/sales.csv")


# Calculate revenue for every transaction.
sales["revenue"] = sales["quantity"] * sales["price"]


# 1. Display all sales.
print("\n========== ALL SALES ==========")
print(sales)


# 2. Calculate total units sold per product.
print("\n========== QUANTITY SOLD PER PRODUCT ==========")

product_quantity = sales.groupby("product")["quantity"].sum()

print(product_quantity)


# 3. Calculate revenue per product.
print("\n========== REVENUE PER PRODUCT ==========")

product_revenue = sales.groupby("product")["revenue"].sum()

print(product_revenue)


# 4. Generate a complete product summary.
print("\n========== PRODUCT PERFORMANCE ==========")

product_summary = sales.groupby("product").agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
    average_price=("price", "mean"),
)

print(product_summary)


# 5. Identify bestselling products.
print("\n========== BESTSELLING PRODUCTS ==========")

best_selling_products = product_summary.sort_values(
    by="total_quantity",
    ascending=False,
)

print(best_selling_products)


# 6. Calculate revenue by category.
print("\n========== REVENUE BY CATEGORY ==========")

category_revenue = sales.groupby("category")["revenue"].sum()

print(category_revenue)

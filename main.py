
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# =====================================
# 1. LOAD SALES DATA
# =====================================

sales = pd.read_csv("data/raw/sales.csv")


# =====================================
# 2. CALCULATE REVENUE
# =====================================

sales["revenue"] = (
    sales["quantity"] * sales["price"]
)


# =====================================
# 3. BUSINESS PERFORMANCE
# =====================================

total_revenue = sales["revenue"].sum()
total_orders = len(sales)
total_units = sales["quantity"].sum()

average_order_value = total_revenue / total_orders


print("\n========== BUSINESS PERFORMANCE ==========")

print(f"Total revenue: ₦{total_revenue:,.2f}")
print(f"Total orders: {total_orders:,}")
print(f"Total units sold: {total_units:,}")

print(
    f"Average order value: ₦{average_order_value:,.2f}"
)


# =====================================
# 4. PRODUCT PERFORMANCE
# =====================================

product_performance = sales.groupby("product").agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
)


# =====================================
# 5. CATEGORY PERFORMANCE
# =====================================

category_performance = sales.groupby("category").agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
)


# =====================================
# 6. PRODUCT RANKINGS
# =====================================

top_products = product_performance.sort_values(
    by="total_revenue",
    ascending=False,
)

best_selling = product_performance.sort_values(
    by="total_quantity",
    ascending=False,
)


print("\n========== TOP PRODUCTS BY REVENUE ==========")
print(top_products)

print("\n========== BESTSELLING PRODUCTS ==========")
print(best_selling)

print("\n========== CATEGORY PERFORMANCE ==========")
print(category_performance)


# =====================================
# 7. CREATE REPORTS DIRECTORY
# =====================================

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)


# =====================================
# 8. EXPORT EXCEL REPORT
# =====================================

with pd.ExcelWriter(
    reports_dir / "sales_performance_report.xlsx"
) as writer:

    product_performance.to_excel(
        writer,
        sheet_name="Product Performance",
    )

    top_products.to_excel(
        writer,
        sheet_name="Top Products",
    )

    category_performance.to_excel(
        writer,
        sheet_name="Category Performance",
    )


# =====================================
# 9. REVENUE BY PRODUCT CHART
# =====================================

product_performance["total_revenue"].plot(
    kind="bar",
)

plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (NGN)")
plt.xticks(rotation=45)

plt.savefig(
    reports_dir / "revenue_by_product.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()
plt.close()


# =====================================
# 10. UNITS SOLD CHART
# =====================================

best_selling["total_quantity"].plot(
    kind="bar",
)

plt.title("Units Sold by Product")
plt.xlabel("Product")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)

plt.savefig(
    reports_dir / "units_sold_by_product.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()
plt.close()


# =====================================
# 11. CATEGORY REVENUE CHART
# =====================================

category_performance["total_revenue"].plot(
    kind="pie",
    autopct="%1.1f%%",
)

plt.title("Revenue Contribution by Category")
plt.ylabel("")

plt.savefig(
    reports_dir / "revenue_by_category.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()
plt.close()


print("\nAll reports and charts generated successfully!")

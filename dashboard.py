
import pandas as pd
import streamlit as st


# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="eCommerce Analytics",
    page_icon="📊",
    layout="wide",
)


# =====================================
# 2. LOAD SALES DATA
# =====================================

@st.cache_data
def load_sales_data():
    sales = pd.read_csv("data/raw/sales.csv")

    sales["revenue"] = (
        sales["quantity"] * sales["price"]
    )

    return sales


sales = load_sales_data()


# =====================================
# 3. DASHBOARD HEADER
# =====================================

st.title("eCommerce Sales Analytics")

st.write(
    "Monitor sales performance, product revenue "
    "and business growth."
)


# =====================================
# 4. DATA QUALITY CHECKS
# =====================================

st.sidebar.header("Dashboard Filters")

with st.expander("Data Quality Inspection"):

    missing_values = sales.isnull().sum().sum()

    duplicate_orders = (
        sales["order_id"].duplicated().sum()
    )

    invalid_quantities = (
        (sales["quantity"] <= 0).sum()
    )

    invalid_prices = (
        (sales["price"] < 0).sum()
    )

    st.subheader("Data Quality Overview")

    quality_col1, quality_col2, quality_col3, quality_col4 = (
        st.columns(4)
    )

    quality_col1.metric(
        "Total Records",
        len(sales),
    )

    quality_col2.metric(
        "Missing Values",
        int(missing_values),
    )

    quality_col3.metric(
        "Duplicate Orders",
        int(duplicate_orders),
    )

    quality_col4.metric(
        "Invalid Records",
        int(invalid_quantities + invalid_prices),
    )

    st.write("Missing values by column:")

    missing_report = sales.isnull().sum()

    missing_report = missing_report[
        missing_report > 0
    ]

    if missing_report.empty:
        st.success("No missing values detected.")
    else:
        st.dataframe(missing_report)

    st.write("Duplicate order references:")

    duplicate_records = sales[
        sales["order_id"].duplicated(keep=False)
    ]

    if duplicate_records.empty:
        st.success("No duplicate orders detected.")
    else:
        st.dataframe(duplicate_records)

    st.write("Invalid quantities:")

    invalid_quantity_records = sales[
        sales["quantity"] <= 0
    ]

    if invalid_quantity_records.empty:
        st.success("No invalid quantities detected.")
    else:
        st.dataframe(invalid_quantity_records)

    st.write("Invalid prices:")

    invalid_price_records = sales[
        sales["price"] < 0
    ]

    if invalid_price_records.empty:
        st.success("No invalid prices detected.")
    else:
        st.dataframe(invalid_price_records)


# =====================================
# 5. SIDEBAR FILTERS
# =====================================

available_categories = sorted(
    sales["category"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=available_categories,
    default=available_categories,
)


available_products = sorted(
    sales["product"].dropna().unique().tolist()
)

selected_products = st.sidebar.multiselect(
    "Select products",
    options=available_products,
    default=available_products,
)


# =====================================
# 6. FILTER SALES DATA
# =====================================

filtered_sales = sales[
    (sales["category"].isin(selected_categories))
    & (sales["product"].isin(selected_products))
]


# =====================================
# 7. CALCULATE BUSINESS KPIs
# =====================================

total_revenue = filtered_sales["revenue"].sum()

total_orders = len(filtered_sales)

total_units = filtered_sales["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# =====================================
# 8. DISPLAY KPI CARDS
# =====================================

st.subheader("Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₦{total_revenue:,.2f}",
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}",
)

col3.metric(
    "Units Sold",
    f"{total_units:,}",
)

col4.metric(
    "Average Order Value",
    f"₦{average_order_value:,.2f}",
)


# =====================================
# 9. PRODUCT PERFORMANCE
# =====================================

st.divider()

st.subheader("Product Performance")

product_performance = filtered_sales.groupby(
    "product"
).agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
)

product_performance = product_performance.sort_values(
    by="total_revenue",
    ascending=False,
)


left_column, right_column = st.columns(2)


with left_column:

    st.write("Revenue by Product")

    st.bar_chart(
        product_performance["total_revenue"]
    )


with right_column:

    st.write("Units Sold by Product")

    st.bar_chart(
        product_performance["total_quantity"]
    )


# =====================================
# 10. CATEGORY PERFORMANCE
# =====================================

st.divider()

st.subheader("Category Performance")

category_performance = filtered_sales.groupby(
    "category"
).agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
)

category_performance = category_performance.sort_values(
    by="total_revenue",
    ascending=False,
)

st.bar_chart(
    category_performance["total_revenue"]
)


# =====================================
# 11. PRODUCT PERFORMANCE TABLE
# =====================================

st.divider()

st.subheader("Product Performance Details")

st.dataframe(
    product_performance,
    use_container_width=True,
)


# =====================================
# 12. DOWNLOAD FILTERED DATA
# =====================================

csv_data = filtered_sales.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download filtered sales data",
    data=csv_data,
    file_name="sales_report.csv",
    mime="text/csv",
)


# =====================================
# 13. DISPLAY SALES TRANSACTIONS
# =====================================

with st.expander("View sales transactions"):

    st.dataframe(
        filtered_sales,
        use_container_width=True,
    )

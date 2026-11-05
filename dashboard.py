
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
# 4. SIDEBAR FILTERS
# =====================================

st.sidebar.header("Dashboard Filters")

available_categories = sorted(
    sales["category"].unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=available_categories,
    default=available_categories,
)


available_products = sorted(
    sales["product"].unique().tolist()
)

selected_products = st.sidebar.multiselect(
    "Select products",
    options=available_products,
    default=available_products,
)


# Filter the sales data.
filtered_sales = sales[
    (sales["category"].isin(selected_categories))
    & (sales["product"].isin(selected_products))
]


# =====================================
# 5. CALCULATE DASHBOARD KPIs
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
# 6. DISPLAY KPI CARDS
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
# 7. PRODUCT PERFORMANCE
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
# 8. CATEGORY PERFORMANCE
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
# 9. PRODUCT PERFORMANCE TABLE
# =====================================

st.divider()

st.subheader("Product Performance Details")

st.dataframe(
    product_performance,
    use_container_width=True,
)


# =====================================
# 10. DOWNLOAD FILTERED DATA
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
# 11. DISPLAY RAW DATA
# =====================================

with st.expander("View sales transactions"):

    st.dataframe(
        filtered_sales,
        use_container_width=True,
    )

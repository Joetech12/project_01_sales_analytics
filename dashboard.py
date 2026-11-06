
from pathlib import Path

import pandas as pd
import streamlit as st

from data_cleaner import clean_sales_data


st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 eCommerce Sales Analytics")
st.write("Analyse your business sales performance.")


# Load sales data
uploaded_file = st.sidebar.file_uploader(
    "Upload sales CSV",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        raw_sales = pd.read_csv(uploaded_file)
        sales = clean_sales_data(raw_sales)

        st.success(
            f"Processed {len(sales)} valid records "
            f"from {len(raw_sales)} uploaded records."
        )

    except Exception as error:
        st.error(f"Unable to process file: {error}")
        st.stop()

else:
    cleaned_file = Path(
        "data/processed/cleaned_sales.csv"
    )

    if cleaned_file.exists():
        sales = pd.read_csv(cleaned_file)
    else:
        raw_sales = pd.read_csv("data/raw/sales.csv")
        sales = clean_sales_data(raw_sales)


if sales.empty:
    st.warning("No valid sales records available.")
    st.stop()


# Convert dates when available
if "order_date" in sales.columns:
    sales["order_date"] = pd.to_datetime(
        sales["order_date"],
        errors="coerce",
    )


# Sidebar filters
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select categories",
    options=sales["category"].unique(),
    default=sales["category"].unique(),
)

products = st.sidebar.multiselect(
    "Select products",
    options=sales["product"].unique(),
    default=sales["product"].unique(),
)


filtered_sales = sales[
    (sales["category"].isin(categories))
    & (sales["product"].isin(products))
].copy()


if filtered_sales.empty:
    st.warning("No sales records match your filters.")
    st.stop()


# Calculate revenue if it does not exist
if "revenue" not in filtered_sales.columns:
    filtered_sales["revenue"] = (
        filtered_sales["quantity"]
        * filtered_sales["price"]
    )


# Key performance indicators
total_revenue = filtered_sales["revenue"].sum()
total_orders = len(filtered_sales)
total_units = filtered_sales["quantity"].sum()
average_order_value = total_revenue / total_orders


st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₦{total_revenue:,.0f}",
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}",
)

col3.metric(
    "Units Sold",
    f"{total_units:,.0f}",
)

col4.metric(
    "Average Order Value",
    f"₦{average_order_value:,.0f}",
)


# Product performance
st.subheader("Product Performance")

product_revenue = (
    filtered_sales.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_revenue)


# Category performance
st.subheader("Category Performance")

category_revenue = (
    filtered_sales.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_revenue)


# Monthly revenue trend
st.subheader("Monthly Revenue Trend")

if "order_date" in filtered_sales.columns:
    dated_sales = filtered_sales.dropna(
        subset=["order_date"]
    ).copy()

    if not dated_sales.empty:
        dated_sales["month"] = (
            dated_sales["order_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = (
            dated_sales.groupby("month")["revenue"]
            .sum()
            .sort_index()
        )

        st.line_chart(monthly_revenue)

    else:
        st.info("No valid dates are available for this chart.")

else:
    st.info(
        "Monthly analysis requires an order_date column."
    )


# Sales records
st.subheader("Sales Records")

st.dataframe(
    filtered_sales,
    use_container_width=True,
)


# Download filtered data
csv_data = filtered_sales.to_csv(index=False)

st.download_button(
    label="Download Sales Data",
    data=csv_data,
    file_name="sales_report.csv",
    mime="text/csv",
)

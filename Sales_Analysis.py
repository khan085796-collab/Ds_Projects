import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Page 2 – Sales Analysis")
st.write("Analyze overall sales performance.")


# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Sales_data.csv", encoding="latin1")

    # Convert Order Date to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Create Year, Month and Quarter columns
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)

    return df


df = load_data()


# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("🔎 Filters")

# Date Filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)


# Region Filter
regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)


# Category Filter
categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)


# Segment Filter
segments = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)


# -----------------------------------
# APPLY FILTERS
# -----------------------------------

filtered_df = df[
    (df["Order Date"].dt.date >= date_range[0]) &
    (df["Order Date"].dt.date <= date_range[1]) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments))
]


# -----------------------------------
# KPI CARDS
# -----------------------------------

total_sales = filtered_df["Sales"].sum()

average_sales = filtered_df.groupby("Order ID")["Sales"].sum().mean()

maximum_order_sales = filtered_df.groupby("Order ID")["Sales"].sum().max()

minimum_order_sales = filtered_df.groupby("Order ID")["Sales"].sum().min()

number_of_orders = filtered_df["Order ID"].nunique()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📊 Avg Sales / Order", f"${average_sales:,.2f}")
col3.metric("⬆️ Maximum Order Sales", f"${maximum_order_sales:,.2f}")
col4.metric("⬇️ Minimum Order Sales", f"${minimum_order_sales:,.2f}")
col5.metric("🛒 Number of Orders", f"{number_of_orders:,}")


st.divider()


# -----------------------------------
# SALES BY MONTH
# -----------------------------------

st.subheader("📅 Sales by Month")

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reindex(month_order)
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Sales by Month"
)

st.plotly_chart(fig_month, use_container_width=True)


# -----------------------------------
# SALES BY YEAR
# -----------------------------------

st.subheader("📆 Sales by Year")

yearly_sales = (
    filtered_df.groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

fig_year = px.bar(
    yearly_sales,
    x="Year",
    y="Sales",
    title="Sales by Year"
)

st.plotly_chart(fig_year, use_container_width=True)


# -----------------------------------
# SALES BY QUARTER
# -----------------------------------

st.subheader("📈 Sales by Quarter")

quarter_order = ["Q1", "Q2", "Q3", "Q4"]

quarter_sales = (
    filtered_df.groupby("Quarter")["Sales"]
    .sum()
    .reindex(quarter_order)
    .reset_index()
)

fig_quarter = px.bar(
    quarter_sales,
    x="Quarter",
    y="Sales",
    title="Sales by Quarter"
)

st.plotly_chart(fig_quarter, use_container_width=True)


# -----------------------------------
# SALES BY REGION
# -----------------------------------

st.subheader("🌍 Sales by Region")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region"
)

st.plotly_chart(fig_region, use_container_width=True)


# -----------------------------------
# SALES BY CATEGORY
# -----------------------------------

st.subheader("📦 Sales by Category")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

st.plotly_chart(fig_category, use_container_width=True)


# -----------------------------------
# SALES DISTRIBUTION HISTOGRAM
# -----------------------------------

st.subheader("📊 Sales Distribution")

fig_histogram = px.histogram(
    filtered_df,
    x="Sales",
    nbins=30,
    title="Sales Distribution Histogram"
)

st.plotly_chart(fig_histogram, use_container_width=True)


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption("Sales Analysis Dashboard | Page 2")

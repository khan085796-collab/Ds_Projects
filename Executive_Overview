import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Overview")
st.write("Business Performance Dashboard")


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    file_path = Path(__file__).parent / "sales_data.csv"

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise pd.errors.EmptyDataError("CSV is empty")

    except (FileNotFoundError, pd.errors.EmptyDataError):

        data = {
            "Order ID": [
                1001, 1002, 1003, 1004,
                1005, 1006, 1007, 1008,
                1009, 1010, 1011, 1012
            ],

            "Order Date": [
                "2026-01-10",
                "2026-01-15",
                "2026-02-05",
                "2026-02-20",
                "2026-03-10",
                "2026-03-15",
                "2026-04-05",
                "2026-04-20",
                "2026-05-10",
                "2026-05-25",
                "2026-06-12",
                "2026-06-28"
            ],

            "Region": [
                "East", "West", "South", "North",
                "East", "West", "South", "North",
                "East", "West", "South", "North"
            ],

            "Category": [
                "Technology",
                "Furniture",
                "Office Supplies",
                "Technology",
                "Furniture",
                "Office Supplies",
                "Technology",
                "Furniture",
                "Office Supplies",
                "Technology",
                "Furniture",
                "Office Supplies"
            ],

            "Segment": [
                "Consumer",
                "Corporate",
                "Home Office",
                "Consumer",
                "Consumer",
                "Corporate",
                "Consumer",
                "Home Office",
                "Corporate",
                "Consumer",
                "Corporate",
                "Home Office"
            ],

            "Sales": [
                500, 700, 300, 900,
                600, 450, 1200, 800,
                550, 1500, 950, 400
            ],

            "Profit": [
                100, 150, 50, 250,
                120, 80, 300, 180,
                90, 400, 200, 70
            ],

            "Quantity": [
                2, 3, 5, 4,
                2, 6, 5, 4,
                7, 6, 3, 5
            ]
        }

        df = pd.DataFrame(data)

        # Create CSV automatically
        df.to_csv(file_path, index=False)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df


df = load_data()


# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("Filters")

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date)
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)


# -------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------

filtered_df = df.copy()

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date) &
        (filtered_df["Order Date"] <= end_date)
    ]

filtered_df = filtered_df[
    filtered_df["Region"].isin(region)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(category)
]

filtered_df = filtered_df[
    filtered_df["Segment"].isin(segment)
]


# -------------------------------------------------
# CHECK IF DATA EXISTS
# -------------------------------------------------

if filtered_df.empty:

    st.warning("No data available for the selected filters.")
    st.stop()


# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

profit_margin = (total_profit / total_sales) * 100


# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🛒 Total Orders", f"{total_orders}")
col4.metric("📦 Total Quantity", f"{total_quantity}")
col5.metric("📊 Profit Margin", f"{profit_margin:.2f}%")


st.divider()


# -------------------------------------------------
# MONTHLY SALES TREND
# -------------------------------------------------

filtered_df = filtered_df.copy()

filtered_df["Month"] = (
    filtered_df["Order Date"]
    .dt.strftime("%Y-%m")
)

monthly_sales = (
    filtered_df
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

fig_monthly_sales = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_monthly_sales,
    use_container_width=True
)


# -------------------------------------------------
# SALES BY REGION AND CATEGORY
# -------------------------------------------------

col1, col2 = st.columns(2)

region_sales = (
    filtered_df
    .groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

category_sales = (
    filtered_df
    .groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

with col1:

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


with col2:

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# -------------------------------------------------
# PROFIT BY CATEGORY AND SCATTER PLOT
# -------------------------------------------------

col1, col2 = st.columns(2)

category_profit = (
    filtered_df
    .groupby("Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

with col1:

    fig_profit = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


with col2:

    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Region", "Segment"],
        title="Sales vs Profit"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# -------------------------------------------------
# BUSINESS INSIGHTS
# -------------------------------------------------

st.divider()

st.subheader("🏆 Business Insights")

best_region = region_sales.iloc[0]["Region"]

best_category = category_sales.iloc[0]["Category"]

highest_sales_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax(),
    "Month"
]

monthly_profit = (
    filtered_df
    .groupby("Month", as_index=False)["Profit"]
    .sum()
)

highest_profit_month = monthly_profit.loc[
    monthly_profit["Profit"].idxmax(),
    "Month"
]


col1, col2, col3, col4 = st.columns(4)

col1.metric("🥇 Best Region", best_region)
col2.metric("🏆 Best Category", best_category)
col3.metric("📅 Highest Sales Month", highest_sales_month)
col4.metric("💰 Highest Profit Month", highest_profit_month)


st.divider()

st.caption("Business Performance Dashboard | Executive Overview")

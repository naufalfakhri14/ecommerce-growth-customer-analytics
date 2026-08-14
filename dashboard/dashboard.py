import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLOBAL STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f7fa;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Main text */
    body {
        color: #172033;
    }

    /* Markdown headings */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: #12345b !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #12345b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar inputs */
    section[data-testid="stSidebar"] input {
        color: #172033 !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce3eb;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 39, 71, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        color: #12345b !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #d1dbe6;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #dce3eb;
    }

    /* Insight cards */
    .insight-card {
        background-color: #ffffff;
        border: 1px solid #d9e2ec;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 15px 0 25px 0;
        box-shadow: 0 2px 6px rgba(15, 39, 71, 0.05);
    }

    .insight-title {
        color: #12345b !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #334155 !important;
        font-size: 14px;
        line-height: 1.6;
    }

    .insight-highlight {
        color: #12345b !important;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "dashboard/main_data.csv"
    )

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce"
    )

    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"],
        errors="coerce"
    )

    return df


df = load_data()


# =========================================================
# PREPARE CUSTOMER-LEVEL RFM
# =========================================================

rfm_customer = (
    df[
        [
            "customer_id",
            "Recency",
            "Frequency",
            "Monetary",
            "RFM_score",
            "customer_segment"
        ]
    ]
    .drop_duplicates("customer_id")
    .copy()
)


# =========================================================
# HEADER
# =========================================================

min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

st.title("E-Commerce Business Intelligence")

st.caption(
    "Sales Performance  |  Customer Experience  |  RFM Customer Segmentation"
)

st.info(
    f"Analysis period: {min_date.strftime('%B %Y')} – "
    f"{max_date.strftime('%B %Y')}  •  "
    "Olist E-Commerce Public Dataset"
)


# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.caption(
    "Use the filters below to explore the business performance."
)


# -------------------------
# Date Filter
# -------------------------

st.sidebar.subheader("Date Range")

date_range = st.sidebar.date_input(
    "Purchase Date",
    value=(
        min_date.date(),
        max_date.date()
    ),
    min_value=min_date.date(),
    max_value=max_date.date()
)


# -------------------------
# Customer Segment Filter
# -------------------------

st.sidebar.subheader("Customer Segment")

segment_options = sorted(
    rfm_customer["customer_segment"]
    .dropna()
    .unique()
    .tolist()
)

selected_segments = st.sidebar.multiselect(
    "Select segment",
    options=segment_options,
    default=segment_options
)


# -------------------------
# Delivery Filter
# -------------------------

st.sidebar.subheader("Delivery Category")

delivery_options = sorted(
    df["delivery_category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_delivery = st.sidebar.multiselect(
    "Select category",
    options=delivery_options,
    default=delivery_options
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# Date filter
if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (
            filtered_df["order_purchase_timestamp"].dt.date
            >= start_date
        )
        &
        (
            filtered_df["order_purchase_timestamp"].dt.date
            <= end_date
        )
    ]


# Customer segment filter
filtered_df = filtered_df[
    filtered_df["customer_segment"].isin(
        selected_segments
    )
]


# Delivery filter
filtered_df = filtered_df[
    filtered_df["delivery_category"]
    .astype(str)
    .isin(selected_delivery)
]


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "No data available for the selected filters. "
        "Please adjust the filters in the sidebar."
    )

    st.stop()


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

st.header("Executive Overview")

total_orders = filtered_df["order_id"].nunique()

total_sales = filtered_df["price"].sum()

average_review = filtered_df["review_score"].mean()

average_delivery = filtered_df["delivery_days"].mean()


kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}"
    )
    st.caption("Unique customer orders")

with kpi2:
    st.metric(
        label="Total Sales",
        value=f"R$ {total_sales:,.0f}"
    )
    st.caption("Total product sales value")

with kpi3:
    st.metric(
        label="Average Review",
        value=f"{average_review:.2f} / 5"
    )
    st.caption("Customer satisfaction score")

with kpi4:
    st.metric(
        label="Average Delivery",
        value=f"{average_delivery:.1f} days"
    )
    st.caption("Average delivery duration")

st.caption(
    f"Currently showing {len(filtered_df):,} records."
)


# =========================================================
# SALES PERFORMANCE
# =========================================================

st.header("Sales Performance")

sales_monthly = (
    filtered_df
    .groupby("year_month")
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("price", "sum")
    )
    .reset_index()
    .sort_values("year_month")
)


col1, col2 = st.columns(2)


# -------------------------
# Monthly Orders
# -------------------------

with col1:

    st.subheader("Monthly Order Volume")

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.lineplot(
        data=sales_monthly,
        x="year_month",
        y="total_orders",
        marker="o",
        linewidth=2,
        ax=ax
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")

    ax.tick_params(
        axis="x",
        rotation=45
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# -------------------------
# Monthly Sales
# -------------------------

with col2:

    st.subheader("Monthly Sales Value")

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.lineplot(
        data=sales_monthly,
        x="year_month",
        y="total_sales",
        marker="o",
        linewidth=2,
        ax=ax
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales (R$)")

    ax.tick_params(
        axis="x",
        rotation=45
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# =========================================================
# SALES INSIGHT
# =========================================================

highest_sales = sales_monthly.loc[
    sales_monthly["total_sales"].idxmax()
]

highest_orders = sales_monthly.loc[
    sales_monthly["total_orders"].idxmax()
]


st.markdown(
    f'''
    <div class="insight-card">
        <div class="insight-title">Key Sales Insight</div>
        <div class="insight-text">
            The highest monthly sales occurred in
            <span class="insight-highlight">{highest_sales['year_month']}</span>,
            reaching approximately
            <span class="insight-highlight">R$ {highest_sales['total_sales']:,.0f}</span>.
            The highest order volume occurred in
            <span class="insight-highlight">{highest_orders['year_month']}</span>,
            with
            <span class="insight-highlight">{highest_orders['total_orders']:,}</span>
            orders.
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)


# =========================================================
# CUSTOMER EXPERIENCE
# =========================================================

st.header("Customer Experience")


delivery_summary = (
    filtered_df
    .groupby(
        "delivery_category",
        observed=False
    )
    .agg(
        average_review=("review_score", "mean"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


# -------------------------
# Review by Delivery
# -------------------------

with col1:

    st.subheader(
        "Average Review by Delivery Category"
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.barplot(
        data=delivery_summary,
        x="delivery_category",
        y="average_review",
        ax=ax
    )

    ax.set_xlabel("Delivery Category")
    ax.set_ylabel("Average Review Score")

    ax.set_ylim(0, 5)

    ax.tick_params(
        axis="x",
        rotation=15
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# -------------------------
# Delivery vs Review
# -------------------------

with col2:

    st.subheader(
        "Delivery Time vs Review Score"
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.scatterplot(
        data=filtered_df,
        x="delivery_days",
        y="review_score",
        alpha=0.25,
        ax=ax
    )

    ax.set_xlabel("Delivery Days")
    ax.set_ylabel("Review Score")

    ax.set_yticks(
        [1, 2, 3, 4, 5]
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# =========================================================
# CUSTOMER EXPERIENCE INSIGHT
# =========================================================

best_delivery = delivery_summary.loc[
    delivery_summary["average_review"].idxmax()
]

worst_delivery = delivery_summary.loc[
    delivery_summary["average_review"].idxmin()
]


st.markdown(
    f'''
    <div class="insight-card">
        <div class="insight-title">Key Customer Experience Insight</div>
        <div class="insight-text">
            The
            <span class="insight-highlight">{best_delivery['delivery_category']}</span>
            category has the highest average review score at
            <span class="insight-highlight">{best_delivery['average_review']:.2f}</span>.
            Meanwhile,
            <span class="insight-highlight">{worst_delivery['delivery_category']}</span>
            has the lowest average score at
            <span class="insight-highlight">{worst_delivery['average_review']:.2f}</span>.
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)


# =========================================================
# RFM CUSTOMER INTELLIGENCE
# =========================================================

st.header("Customer Intelligence — RFM Analysis")


# Filter customer-level RFM based on selected customers
selected_customer_ids = (
    filtered_df["customer_id"]
    .dropna()
    .unique()
)

rfm_filtered = rfm_customer[
    rfm_customer["customer_id"].isin(
        selected_customer_ids
    )
].copy()


# =========================================================
# RFM SEGMENT DISTRIBUTION
# =========================================================

segment_summary = (
    rfm_filtered
    .groupby("customer_segment")
    .agg(
        customer_count=("customer_id", "nunique"),
        avg_recency=("Recency", "mean"),
        avg_frequency=("Frequency", "mean"),
        avg_monetary=("Monetary", "mean")
    )
    .reset_index()
    .sort_values(
        "customer_count",
        ascending=False
    )
)


col1, col2 = st.columns(2)


# -------------------------
# Segment Distribution
# -------------------------

with col1:

    st.subheader(
        "Customer Segment Distribution"
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.barplot(
        data=segment_summary,
        x="customer_segment",
        y="customer_count",
        ax=ax
    )

    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Customers")

    ax.tick_params(
        axis="x",
        rotation=20
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# -------------------------
# Recency vs Monetary
# -------------------------

with col2:

    st.subheader(
        "Recency vs Monetary Value"
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.scatterplot(
        data=rfm_filtered,
        x="Recency",
        y="Monetary",
        hue="customer_segment",
        alpha=0.55,
        ax=ax
    )

    ax.set_xlabel(
        "Recency (Days)"
    )

    ax.set_ylabel(
        "Monetary Value"
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        title="Customer Segment",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


# =========================================================
# RFM SUMMARY TABLE
# =========================================================

st.subheader("RFM Segment Summary")


display_rfm = segment_summary.copy()


display_rfm["avg_recency"] = (
    display_rfm["avg_recency"]
    .round(1)
)

display_rfm["avg_frequency"] = (
    display_rfm["avg_frequency"]
    .round(2)
)

display_rfm["avg_monetary"] = (
    display_rfm["avg_monetary"]
    .round(2)
)


display_rfm = display_rfm.rename(
    columns={
        "customer_segment": "Customer Segment",
        "customer_count": "Customer Count",
        "avg_recency": "Avg. Recency",
        "avg_frequency": "Avg. Frequency",
        "avg_monetary": "Avg. Monetary"
    }
)


st.dataframe(
    display_rfm,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RFM INSIGHT
# =========================================================

largest_segment = segment_summary.iloc[0]

highest_value_segment = segment_summary.loc[
    segment_summary["avg_monetary"].idxmax()
]

lowest_recency_segment = segment_summary.loc[
    segment_summary["avg_recency"].idxmin()
]


st.markdown(
    f'''
    <div class="insight-card">
        <div class="insight-title">Key RFM Insight</div>
        <div class="insight-text">
            <span class="insight-highlight">{largest_segment['customer_segment']}</span>
            is the largest customer segment with
            <span class="insight-highlight">{largest_segment['customer_count']:,}</span>
            customers.
            The segment with the highest average monetary value is
            <span class="insight-highlight">{highest_value_segment['customer_segment']}</span>
            at approximately
            <span class="insight-highlight">R$ {highest_value_segment['avg_monetary']:,.2f}</span>.
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "E-Commerce Public Dataset · Business Intelligence Dashboard"
)
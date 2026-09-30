
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# IT SUPPORT COST OPTIMIZATION - STREAMLIT DASHBOARD
# ============================================================

st.set_page_config(
    page_title="IT Support Cost Optimization",
    page_icon="🎧",
    layout="wide"
)

# -------------------- Styling --------------------

st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    color: #666;
    font-size: 17px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Load Data --------------------

BASE_DIR = Path(__file__).resolve().parent

# Original project cleaned file
DATA_PATH = BASE_DIR / "output" / "cleaned_customer_support_tickets.csv"

# Fallback in case the cleaned file is kept inside data/
if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR / "data" / "cleaned_customer_support_tickets.csv"

if not DATA_PATH.exists():
    st.error(
        "Cleaned dataset not found.\n\n"
        "Expected:\n"
        "output/cleaned_customer_support_tickets.csv"
    )
    st.stop()

df = pd.read_csv(DATA_PATH)

# Convert rating safely
if "Customer Satisfaction Rating" in df.columns:
    df["Customer Satisfaction Rating"] = pd.to_numeric(
        df["Customer Satisfaction Rating"], errors="coerce"
    )

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

filtered_df = df.copy()

def add_filter(column, label):
    global filtered_df
    if column in df.columns:
        options = sorted(df[column].dropna().unique().tolist())
        selected = st.sidebar.multiselect(
            label,
            options,
            default=options
        )
        if selected:
            filtered_df = filtered_df[
                filtered_df[column].isin(selected)
            ]

add_filter("Ticket Type", "Ticket Type")
add_filter("Ticket Status", "Ticket Status")
add_filter("Ticket Priority", "Ticket Priority")
add_filter("Ticket Channel", "Ticket Channel")
add_filter("Customer Gender", "Customer Gender")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎧 IT Support Cost Optimization Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of customer support workload, unresolved tickets, '
    'priority, channels and customer satisfaction.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# KPIs
# ============================================================

total = len(filtered_df)

closed = (
    (filtered_df["Ticket Status"] == "Closed").sum()
    if "Ticket Status" in filtered_df.columns else 0
)

open_tickets = (
    (filtered_df["Ticket Status"] == "Open").sum()
    if "Ticket Status" in filtered_df.columns else 0
)

pending = (
    (filtered_df["Ticket Status"] == "Pending Customer Response").sum()
    if "Ticket Status" in filtered_df.columns else 0
)

unresolved = open_tickets + pending
unresolved_pct = (unresolved / total * 100) if total else 0

avg_satisfaction = (
    filtered_df["Customer Satisfaction Rating"].mean()
    if "Customer Satisfaction Rating" in filtered_df.columns
    else 0
)

st.subheader("📌 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Tickets", f"{total:,}")
c2.metric("Closed Tickets", f"{closed:,}")
c3.metric("Open Tickets", f"{open_tickets:,}")
c4.metric("Unresolved %", f"{unresolved_pct:.1f}%")
c5.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/5")

st.divider()

# ============================================================
# TICKET TYPE + STATUS
# ============================================================

st.subheader("📊 Ticket Overview")

col1, col2 = st.columns(2)

with col1:
    type_counts = (
        filtered_df["Ticket Type"]
        .value_counts()
        .rename_axis("Ticket Type")
        .reset_index(name="Tickets")
    )

    fig = px.bar(
        type_counts,
        x="Tickets",
        y="Ticket Type",
        orientation="h",
        text="Tickets",
        title="Tickets by Ticket Type"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    status_counts = (
        filtered_df["Ticket Status"]
        .value_counts()
        .rename_axis("Ticket Status")
        .reset_index(name="Tickets")
    )

    fig = px.pie(
        status_counts,
        names="Ticket Status",
        values="Tickets",
        hole=0.45,
        title="Ticket Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PRIORITY + CHANNEL
# ============================================================

col1, col2 = st.columns(2)

with col1:
    priority_counts = (
        filtered_df["Ticket Priority"]
        .value_counts()
        .rename_axis("Priority")
        .reset_index(name="Tickets")
    )

    fig = px.bar(
        priority_counts,
        x="Priority",
        y="Tickets",
        text="Tickets",
        title="Tickets by Priority"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    channel_counts = (
        filtered_df["Ticket Channel"]
        .value_counts()
        .rename_axis("Channel")
        .reset_index(name="Tickets")
    )

    fig = px.pie(
        channel_counts,
        names="Channel",
        values="Tickets",
        hole=0.45,
        title="Tickets by Support Channel"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# UNRESOLVED ANALYSIS
# ============================================================

st.divider()
st.subheader("⚠️ Unresolved Ticket Analysis")

unresolved_df = filtered_df[
    filtered_df["Ticket Status"] != "Closed"
]

col1, col2 = st.columns(2)

with col1:
    unresolved_type = (
        unresolved_df["Ticket Type"]
        .value_counts()
        .rename_axis("Ticket Type")
        .reset_index(name="Unresolved Tickets")
    )

    fig = px.bar(
        unresolved_type,
        x="Unresolved Tickets",
        y="Ticket Type",
        orientation="h",
        text="Unresolved Tickets",
        title="Unresolved Tickets by Ticket Type"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    unresolved_priority = (
        unresolved_df["Ticket Priority"]
        .value_counts()
        .rename_axis("Priority")
        .reset_index(name="Unresolved Tickets")
    )

    fig = px.bar(
        unresolved_priority,
        x="Priority",
        y="Unresolved Tickets",
        text="Unresolved Tickets",
        title="Unresolved Tickets by Priority"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# SATISFACTION
# ============================================================

st.divider()
st.subheader("⭐ Customer Satisfaction Analysis")

rated = filtered_df.dropna(
    subset=["Customer Satisfaction Rating"]
)

col1, col2 = st.columns(2)

with col1:
    sat_type = (
        rated.groupby("Ticket Type")["Customer Satisfaction Rating"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        sat_type,
        x="Ticket Type",
        y="Customer Satisfaction Rating",
        text="Customer Satisfaction Rating",
        title="Average Satisfaction by Ticket Type"
    )
    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )
    fig.update_yaxes(range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    sat_priority = (
        rated.groupby("Ticket Priority")["Customer Satisfaction Rating"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        sat_priority,
        x="Ticket Priority",
        y="Customer Satisfaction Rating",
        text="Customer Satisfaction Rating",
        title="Average Satisfaction by Priority"
    )
    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )
    fig.update_yaxes(range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PRIORITY VS STATUS
# ============================================================

st.divider()
st.subheader("🔄 Priority vs Ticket Status")

priority_status = (
    filtered_df
    .groupby(["Ticket Priority", "Ticket Status"])
    .size()
    .reset_index(name="Tickets")
)

fig = px.bar(
    priority_status,
    x="Ticket Priority",
    y="Tickets",
    color="Ticket Status",
    barmode="stack",
    text="Tickets",
    title="Ticket Status Distribution by Priority"
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================
# KEY INSIGHTS
# ============================================================

st.divider()
st.subheader("💡 Key Business Insights")

type_counts = filtered_df["Ticket Type"].value_counts()
unresolved_type_counts = unresolved_df["Ticket Type"].value_counts()
unresolved_priority_counts = unresolved_df["Ticket Priority"].value_counts()

if not type_counts.empty:
    top_type = type_counts.idxmax()
    top_count = type_counts.max()
    st.info(
        f"📌 **Highest ticket volume:** {top_type} "
        f"({top_count:,} tickets)."
    )

if not unresolved_type_counts.empty:
    top_unresolved_type = unresolved_type_counts.idxmax()
    top_unresolved_count = unresolved_type_counts.max()
    st.warning(
        f"⚠️ **Highest unresolved workload:** {top_unresolved_type} "
        f"({top_unresolved_count:,} tickets)."
    )

if not unresolved_priority_counts.empty:
    top_unresolved_priority = unresolved_priority_counts.idxmax()
    top_unresolved_priority_count = unresolved_priority_counts.max()
    st.warning(
        f"🚨 **Largest unresolved priority workload:** "
        f"{top_unresolved_priority} "
        f"({top_unresolved_priority_count:,} tickets)."
    )

if not rated.empty:
    sat_by_type = (
        rated.groupby("Ticket Type")["Customer Satisfaction Rating"]
        .mean()
    )
    lowest_type = sat_by_type.idxmin()
    lowest_score = sat_by_type.min()

    st.info(
        f"⭐ **Lowest average satisfaction:** {lowest_type} "
        f"({lowest_score:.2f}/5)."
    )

# ============================================================
# DATA PREVIEW
# ============================================================

st.divider()

with st.expander("🔎 View Filtered Data"):
    st.write(f"Records shown: **{len(filtered_df):,}**")
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ============================================================
# PROJECT LIMITATION
# ============================================================

st.divider()

st.caption(
    "Note: The dataset does not contain direct monetary fields such as "
    "agent salary, handling cost or cost per ticket. Therefore, this "
    "dashboard uses workload and support-efficiency indicators for "
    "cost-optimization analysis rather than inventing monetary savings."
)

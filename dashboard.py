
import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Electricity Analytics Dashboard",
    page_icon="⚡",
    layout="wide"
)



# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>

/* Dashboard Background */
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* All Headings */
h1, h2, h3 {
    color: var(--text-color) !important;
    font-weight: 800;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background-color: var(--secondary-background-color);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.4);
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

/* Metric Labels */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: var(--text-color) !important;
}

/* Metric Values */
div[data-testid="stMetricValue"] {
    color: var(--primary-color) !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("electricity_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- HEADER ----------------
st.title("⚡ Electricity Consumption Analytics")
st.markdown(
    "### Daily Electricity Consumption Dashboard"
)
st.caption("Project ID: DA-018 | Energy Analytics | October 2026")

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard Controls")
st.sidebar.info("Select a date range to analyse electricity consumption.")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ---------------- FILTER DATA ----------------
if len(date_range) == 2:
    start_date, end_date = date_range

    data = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ].copy()
else:
    data = df.copy()

if data.empty:
    st.warning("No records found for the selected dates.")

else:

    # ---------------- CALCULATIONS ----------------
    total = data["Electricity_Consumption"].sum()
    average = data["Electricity_Consumption"].mean()
    highest = data["Electricity_Consumption"].max()
    lowest = data["Electricity_Consumption"].min()

    highest_day = data[
        data["Electricity_Consumption"] == highest
    ]

    lowest_day = data[
        data["Electricity_Consumption"] == lowest
    ]

    # ---------------- KPI CARDS ----------------
    st.subheader("📊 Consumption Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Consumption", f"{total:.2f} kWh")
    col2.metric("Daily Average", f"{average:.2f} kWh")
    col3.metric("Highest Usage", f"{highest:.2f} kWh")
    col4.metric("Lowest Usage", f"{lowest:.2f} kWh")

    st.divider()

    # ---------------- DAILY CHART ----------------
    st.subheader("📈 Daily Electricity Consumption")

    chart_data = data.set_index("Date")[
        ["Electricity_Consumption"]
    ]

    st.bar_chart(
        chart_data,
        color="#2585c7"
    )

    st.subheader("📉 Consumption Trend")

    st.line_chart(
        chart_data,
        color="#16a085"
    )

    st.divider()

    # ---------------- HIGHEST USAGE ----------------
    st.subheader("🏆 Highest Consumption Days")

    top_days = data.nlargest(
        5, "Electricity_Consumption"
    ).copy()

    top_days["Date"] = top_days["Date"].dt.strftime("%d %B %Y")

    st.dataframe(
        top_days,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- LOWEST USAGE ----------------
    st.subheader("🌱 Lowest Consumption Day")

    low_display = lowest_day.copy()
    low_display["Date"] = low_display["Date"].dt.strftime(
        "%d %B %Y"
    )

    st.dataframe(
        low_display,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- HIGHEST DAY HIGHLIGHT ----------------
    st.subheader("⭐ Peak Consumption Details")

    for _, row in highest_day.iterrows():
        st.success(
            f"Highest consumption was {row['Electricity_Consumption']} kWh "
            f"on {row['Date'].strftime('%d %B %Y')}."
        )

    # ---------------- COMPLETE RECORDS ----------------
    st.divider()

    st.subheader("📋 Complete Electricity Records")

    display_data = data.copy()
    display_data["Date"] = display_data["Date"].dt.strftime(
        "%d %B %Y"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- FOOTER ----------------
    st.divider()

    st.caption(
        "Electricity Consumption Pattern Analysis | DA-018 | "
        "Developed using Python, Pandas and Streamlit"
    )

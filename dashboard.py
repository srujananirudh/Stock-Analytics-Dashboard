import streamlit as st
import requests
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(layout="wide")

st.title("📊 Stock Dashboard")
st.markdown("### 📈 Financial Insights Dashboard")

# -------------------------------
# Fetch Data from API
# -------------------------------
url = "http://127.0.0.1:8000/data"
data = requests.get(url).json()

df = pd.DataFrame(data)

# Clean duplicates
df = df.drop_duplicates(subset=["company_name", "year"])

# -------------------------------
# Sidebar Filter
# -------------------------------
st.sidebar.header("Filters")
company = st.sidebar.selectbox("Select Company", df["company_name"].unique())

filtered_df = df[df["company_name"] == company]
filtered_df = filtered_df.sort_values(by="year")

# -------------------------------
# Top Metrics Section
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.image(filtered_df["company_logo"].iloc[0], width=120)

with col2:
    st.metric("Latest EPS", filtered_df["eps"].iloc[-1])

with col3:
    st.metric("Latest Profit", filtered_df["net_profit"].iloc[-1])

# -------------------------------
# 📊 Insights Section
# -------------------------------
st.subheader("📊 Key Insights")

latest = filtered_df.iloc[-1]

if len(filtered_df) > 1:
    previous = filtered_df.iloc[-2]

    profit_growth = latest["net_profit"] - previous["net_profit"]
    sales_growth = latest["sales"] - previous["sales"]

    if profit_growth > 0:
        st.success(f"Profit increased by {profit_growth}")
    else:
        st.error(f"Profit decreased by {profit_growth}")

    if sales_growth > 0:
        st.success(f"Sales increased by {sales_growth}")
    else:
        st.error(f"Sales decreased by {sales_growth}")
else:
    st.info("Not enough data for growth analysis")

# -------------------------------
# Charts Section
# -------------------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("EPS Trend")
    st.line_chart(filtered_df.set_index("year")[["eps"]])

with col5:
    st.subheader("Sales vs Profit")
    st.bar_chart(
        filtered_df.set_index("year")[["sales", "net_profit"]]
    )

# -------------------------------
# Top Companies (Improved)
# -------------------------------
st.subheader("Top Companies by Total Profit")

top10 = (
    df.groupby("company_name")["net_profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top10)

# -------------------------------
# Data Table
# -------------------------------
st.subheader("Detailed Data")
st.dataframe(filtered_df)
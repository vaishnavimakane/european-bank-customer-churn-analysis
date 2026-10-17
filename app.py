import streamlit as st
import pandas as pd
import plotly.express as px
import glob

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load the CSV file
csv_files = glob.glob("*.csv")

if not csv_files:
    st.error("CSV file not found in the project folder.")
    st.stop()

df = pd.read_csv(csv_files[0])
# Segment Filters
st.sidebar.header("Filters")
geography_filter = st.sidebar.multiselect(
    "Select Geography",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

age_filter = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

filtered_df = df[
    (df["Geography"].isin(geography_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(age_filter[0], age_filter[1]))]

st.title("🏦 Customer Churn Analysis Dashboard")
st.write("European Bank Customer Churn Analysis")
# Overall Churn Summary

total_customers = len(filtered_df)
churned_customers = filtered_df["Exited"].sum()
retained_customers = total_customers - churned_customers

if total_customers > 0:
    churn_rate = (churned_customers / total_customers) * 100
else:
    churn_rate = 0

st.subheader("Overall Churn Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Retained Customers", f"{retained_customers:,}")
col4.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
# Geography-wise Churn

st.subheader("Geography-wise Customer Churn")

geo_churn = (
   filtered_df.groupby("Geography")["Exited"]
    .mean()
    .reset_index()
)

geo_churn["Exited"] = geo_churn["Exited"] * 100

fig_geo = px.bar(
    geo_churn,
    x="Geography",
    y="Exited",
    text="Exited",
    title="Churn Rate by Geography",
    labels={"Exited": "Churn Rate (%)"}
)

fig_geo.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

st.plotly_chart(fig_geo, width="stretch")
# Age-wise Churn

st.subheader("Age-wise Customer Churn")

age_churn = (
    filtered_df.groupby("Age")["Exited"]
    .mean()
    .reset_index()
)

age_churn["Exited"] = age_churn["Exited"] * 100

fig_age = px.line(
    age_churn,
    x="Age",
    y="Exited",
    markers=True,
    title="Churn Rate by Age",
    labels={"Exited": "Churn Rate (%)"}
)

st.plotly_chart(fig_age, width="stretch")
# Tenure-wise Churn

st.subheader("Tenure-wise Customer Churn")

tenure_churn = (
    filtered_df.groupby("Tenure")["Exited"]
    .mean()
    .reset_index()
)

tenure_churn["Exited"] = tenure_churn["Exited"] * 100

fig_tenure = px.bar(
    tenure_churn,
    x="Tenure",
    y="Exited",
    text="Exited",
    title="Churn Rate by Tenure",
    labels={"Exited": "Churn Rate (%)"}
)

fig_tenure.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_tenure, width="stretch")
# High-Value Customer Churn

st.subheader("High-Value Customer Churn")

median_balance = df["Balance"].median()

filtered_df["Balance Segment"] = filtered_df["Balance"].apply(
    lambda x: "Zero-balance" if x == 0
    else ("Low-balance" if x <= median_balance else "High-balance")
)

high_value_churn = (
    filtered_df.groupby("Balance Segment")["Exited"]
    .mean()
    .reset_index()
)

high_value_churn["Exited"] = high_value_churn["Exited"] * 100

fig_high_value = px.bar(
    high_value_churn,
    x="Balance Segment",
    y="Exited",
    text="Exited",
    title="High-Value Customer Churn",
    labels={"Exited": "Churn Rate (%)"}
)

fig_high_value.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_high_value, width="stretch")
# Salary-wise Customer Churn

st.subheader("Salary-wise Customer Churn")

filtered_df["Salary Segment"] = pd.cut(
    filtered_df["EstimatedSalary"],
    bins=[-1, 50000, 100000, float("inf")],
    labels=["Low Salary", "Medium Salary", "High Salary"]
)

salary_churn = (
    filtered_df.groupby("Salary Segment", observed=False)["Exited"]
    .mean()
    .reset_index()
)

salary_churn["Exited"] = salary_churn["Exited"] * 100

fig_salary = px.bar(
    salary_churn,
    x="Salary Segment",
    y="Exited",
    text="Exited",
    title="Churn Rate by Salary Segment",
    labels={"Exited": "Churn Rate (%)"}
)

fig_salary.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_salary, width="stretch")
# Customer Explorer
st.subheader("🔎 Customer Explorer")

st.write(
    "Customers matching the selected Geography, Gender, and Age filters."
)

explorer_columns = [
    "CustomerId",
    "Surname",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited"
]

display_df = filtered_df[explorer_columns]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.caption(
    f"Showing {len(display_df):,} customers based on the selected filters."
)
# Key Insights
st.subheader("💡 Key Insights")

st.write(
    f"Based on the current filters, there are {len(filtered_df):,} customers in the selected segment."
)
st.write(
    f"The churn rate for the selected segment is {churn_rate:.2f}%."
)
st.write(
    f"Churned customers in the selected segment: {churned_customers:,}."
)
import streamlit as st
import pandas as pd
from pyathena import connect

conn = connect(
    s3_staging_dir="s3://aws-athena-query-results-pooja/",
    region_name="us-east-1"
)

st.set_page_config(page_title="AWS Dashboard", layout="wide")

st.title("AWS Resource Intelligence Dashboard")

# Sidebar
st.sidebar.header("Filters")

# Load Data
@st.cache_data
def load_data():
    query = """
    SELECT resource_type, COUNT(*) as total
    FROM aws_tracker.resources
    GROUP BY resource_type
    """
    return pd.read_sql(query, conn)

df = load_data()

# KPI
col1, col2 = st.columns(2)
col1.metric("Total Resource Types", len(df))
col2.metric("Total Resources", df["total"].sum())

# Chart
st.subheader("Resource Distribution")
st.bar_chart(df.set_index("resource_type"))

# Pie Chart
st.subheader("Resource Share")
st.pyplot(df.set_index("resource_type").plot.pie(y="total", autopct="%1.1f%%").figure)

# Table
st.subheader("Data")
st.dataframe(df)
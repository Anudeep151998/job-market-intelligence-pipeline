import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Job Market Intel", layout="wide")

def load_data():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'job_market.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Results")
    # Multi-select for locations
    locations = st.sidebar.multiselect("Select Locations", options=df['location'].unique(), default=[])
    # Slider for salary
    min_sal = st.sidebar.slider("Minimum Salary (£)", 0, int(df['salary_max'].max()), 20000)

    # Apply filters
    if locations:
        df = df[df['location'].isin(locations)]
    df = df[df['salary_max'] >= min_sal]

    # --- MAIN UI ---
    st.title("🌐 Job Market Intelligence Platform")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Listings", len(df))
    col2.metric("Avg Max Salary", f"£{int(df['salary_max'].mean()):,}")
    col3.metric("Unique Companies", df['company'].nunique())

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x="salary_min", title="Salary Distribution", nbins=20, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_cos = df['company'].value_counts().nlargest(10).reset_index()
        fig2 = px.bar(top_cos, x='count', y='company', orientation='h', title="Top 10 Hiring Companies")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Filtered Job Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.warning("Run the pipeline first to generate data!")
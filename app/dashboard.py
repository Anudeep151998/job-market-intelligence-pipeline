import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import subprocess
import sys

st.set_page_config(page_title="Job Market Intel", layout="wide")

# --- DATABASE PATH LOGIC ---
# This ensures it finds the 'data' folder regardless of if it's on Windows or Linux Cloud
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'job_market.db')

def run_pipeline():
    """Triggers the main pipeline script"""
    with st.spinner("Fetching live data from Adzuna... this may take a moment."):
        try:
            # Runs the run_pipeline.py located in your root directory
            pipeline_path = os.path.join(BASE_DIR, 'run_pipeline.py')
            subprocess.check_call([sys.executable, pipeline_path])
            st.success("Pipeline executed successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error running pipeline: {e}")

def load_data():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

# --- SIDEBAR ---
st.sidebar.header("Data Management")
if st.sidebar.button("🔄 Run Live Pipeline"):
    run_pipeline()

# --- DATA LOADING LOGIC ---
df = load_data()

if df is None or df.empty:
    st.title("🌐 Job Market Intelligence Platform")
    st.warning("⚠️ No data found in the cloud environment.")
    st.info("Click the **'Run Live Pipeline'** button in the sidebar to fetch data using your API keys.")
else:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Results")
    locations = st.sidebar.multiselect("Select Locations", options=df['location'].unique(), default=[])
    
    # Salary slider with safety check for empty data
    max_val = int(df['salary_max'].max()) if not df.empty else 100000
    min_sal = st.sidebar.slider("Minimum Salary (£)", 0, max_val, 20000)

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
import pandas as pd
import json
import os
from datetime import datetime
from logger_config import get_logger

# Initialize logger
logger = get_logger("TRANSFORM")

def transform_data():
    logger.info("✨ Starting High-Volume Transformation...")
    
    input_file = 'data/raw/raw_jobs.json'
    output_file = 'data/processed/clean_jobs.csv'
    
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} not found!")
        return

    # Load the big JSON
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['results'])
    
    if df.empty:
        logger.warning("The raw data file is empty. Nothing to transform.")
        return

    # --- DATA CLEANING & REFINEMENT ---
    
    # 1. Rename columns to match our 'Data Contract'
    df = df.rename(columns={'id': 'job_id', 'title': 'job_title'})
    
    # 2. Extract nested dictionary values (Company and Location)
    df['company'] = df['company'].apply(lambda x: x.get('display_name', 'N/A') if isinstance(x, dict) else 'N/A')
    df['location'] = df['location'].apply(lambda x: x.get('display_name', 'N/A') if isinstance(x, dict) else 'N/A')
    
    # 3. Numeric Standardization
    # Convert salaries to numbers and fill missing ones with 0
    df['salary_min'] = pd.to_numeric(df.get('salary_min'), errors='coerce').fillna(0)
    df['salary_max'] = pd.to_numeric(df.get('salary_max'), errors='coerce').fillna(0)

    # 4. Filter out "Junk" Data
    # In a real job, we only want high-quality data. 
    # Let's drop rows that have no title or no company.
    initial_count = len(df)
    df = df.dropna(subset=['job_title', 'company'])
    
    # 5. Metadata for Auditing
    df['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 6. Column Selection (Strict Schema)
    target_columns = ['job_id', 'job_title', 'company', 'location', 'salary_min', 'salary_max', 'processed_at']
    df = df[target_columns]

    # Save to Silver Layer
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv(output_file, index=False)
    
    logger.info(f"✅ Success! Processed {len(df)} jobs (Dropped {initial_count - len(df)} messy records).")

if __name__ == "__main__":
    transform_data()
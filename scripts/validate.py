import pandas as pd
import os
from logger_config import get_logger

logger = get_logger("VALIDATE")

def validate_data():
    logger.info("🔍 Running Automated Quality Checks...")
    input_file = 'data/processed/clean_jobs.csv'
    
    if not os.path.exists(input_file):
        logger.error("Clean CSV missing!")
        return False

    df = pd.read_csv(input_file)

    # CHECK 1: VOLUME CHECK
    if len(df) < 10:
        logger.error(f"❌ DATA QUALITY ISSUE: Only {len(df)} rows found. Expected > 10.")
        return False

    # CHECK 2: SCHEMA CHECK
    expected_cols = ['job_id', 'job_title', 'company', 'location', 'salary_min', 'salary_max', 'processed_at']
    if not all(col in df.columns for col in expected_cols):
        logger.error("❌ SCHEMA ERROR: Missing required columns.")
        return False

    # CHECK 3: NULL CHECK
    if df['job_id'].isnull().any():
        logger.error("❌ DATA INTEGRITY ERROR: Found NULL job IDs.")
        return False

    logger.info(f"✅ Quality Assurance Passed for {len(df)} records.")
    return True

if __name__ == "__main__":
    validate_data()
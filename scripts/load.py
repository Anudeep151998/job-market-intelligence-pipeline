import pandas as pd
import sqlite3
import os

def load_data():
    print("💾 Starting the 'Smart Load' process (Upsert)...")
    
    # Use absolute-style pathing to avoid "Database not found" errors
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_path, 'data', 'processed', 'clean_jobs.csv')
    db_file = os.path.join(base_path, 'data', 'job_market.db')

    if not os.path.exists(input_file):
        print(f"❌ Error: Clean CSV not found at {input_file}")
        return

    df = pd.read_csv(input_file)
    conn = sqlite3.connect(db_file)
    
    # --- SELF-HEALING SCHEMA LOGIC ---
    # Check if the table exists and has the right columns
    cursor = conn.execute("PRAGMA table_info(jobs)")
    columns = [info[1] for info in cursor.fetchall()]
    
    # If the table exists but is missing our new column, drop it to reset
    if columns and 'salary_min' not in columns:
        print("⚠️  Old Schema detected in data/job_market.db. Resetting table...")
        conn.execute("DROP TABLE jobs")

    # Now create the perfect schema for recruiters to see
    conn.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        job_title TEXT,
        company TEXT,
        location TEXT,
        salary_min REAL,
        salary_max REAL,
        processed_at TEXT
    )
    """)

    # Load to staging
    df.to_sql('staging_jobs', conn, if_exists='replace', index=False)

    # Move from staging to permanent using explicit column names
    conn.execute("""
    INSERT OR REPLACE INTO jobs (job_id, job_title, company, location, salary_min, salary_max, processed_at)
    SELECT job_id, job_title, company, location, salary_min, salary_max, processed_at FROM staging_jobs
    """)

    conn.execute("DROP TABLE staging_jobs")
    conn.commit()
    
    cursor = conn.execute("SELECT COUNT(*) FROM jobs")
    row_count = cursor.fetchone()[0]
    print(f"✅ Success! Total historical records in Database: {row_count}")
    conn.close()

if __name__ == "__main__":
    load_data()
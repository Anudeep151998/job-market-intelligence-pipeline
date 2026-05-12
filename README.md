# 🌐 Job Market Intelligence Pipeline (End-to-End ETL)

A production-grade Data Engineering pipeline that automates the collection, transformation, and visualization of global job market data.

## 🏗️ Architecture: The Medallion Design
This project follows the **Medallion Architecture**, ensuring data quality at every stage:
- **Bronze (Raw):** Multi-page ingestion from Adzuna API (JSON).
- **Silver (Processed):** Data cleaning, deduplication, and schema standardization (Pandas).
- **Gold (Analytics):** Relational storage (SQLite) powering an interactive dashboard.

## 🚀 Key Features
- **Pagination Logic:** Handles high-volume data extraction across multiple API pages.
- **Circuit Breaker Validation:** A custom data-quality layer that halts the pipeline if schema or volume thresholds aren't met.
- **Automated Orchestration:** A central master script to manage the full ETL lifecycle.
- **Interactive Analytics:** A Streamlit-based dashboard featuring salary distributions and market share insights.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Libraries:** Pandas, Plotly, Streamlit, Requests, Dotenv
- **Database:** SQLite3
- **DevOps:** Logging, Data Validation, Error Handling

## 🚦 How to Run
1. Clone the repo: `git clone [YOUR_REPO_URL]`
2. Install requirements: `pip install -r requirements.txt`
3. Add your API keys to a `.env` file.
4. Run the pipeline: `python run_pipeline.py`
5. Launch dashboard: `streamlit run app/dashboard.py`
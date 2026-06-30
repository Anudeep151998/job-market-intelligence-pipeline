# 🌐 Job Market Intelligence Pipeline (End-to-End ETL)
# Automated Job Market Intelligence Pipeline & Dashboard

An end-to-end ETL data pipeline designed to track, aggregate, and visualize real-time software engineering job market trends across the United Kingdom. A production-grade Data Engineering pipeline that automates the collection, transformation, and visualization of global job market data.

## 🏗️ Architecture: The Medallion Design
This project follows the **Medallion Architecture**, ensuring data quality at every stage:
- **Bronze (Raw):** Multi-page ingestion from Adzuna API (JSON) handling high-volume raw payloads.
- **Silver (Processed):** Data cleaning, programmatic deduplication, and strict schema standardization using Pandas.
- **Gold (Analytics):** Relational storage hosted on cloud PostgreSQL (Supabase) powering analytical aggregates.

## 🚀 Key Features
- **Pagination Logic:** Handles high-volume data extraction across multiple API pages seamlessly.
- **Circuit Breaker Validation:** A custom data-quality and testing layer that halts the pipeline execution safely if schema expectations or volume thresholds are not met.
- **Automated Orchestration:** A centralized master runner script to manage and log the full ETL lifecycle automatically.
- **Interactive Analytics:** A Streamlit-based dashboard featuring dynamic salary distributions, regional hiring concentrations, and market share insights.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Libraries:** Pandas, Plotly, Streamlit, Requests, SQLAlchemy, Dotenv
- **Database:** PostgreSQL (Supabase cloud instance)
- **DevOps/QA:** Logging, Data Quality Validation, Environment Isolation, Error Handling

## 🚦 How to Run
1. **Clone the repository:**
   ```bash
   git clone [YOUR_REPO_URL]
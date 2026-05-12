import requests
import json
import os
import time
from dotenv import load_dotenv
from logger_config import get_logger

# Initialize professional logger
logger = get_logger("EXTRACT")

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(pages=5):
    """
    Fetches multiple pages of job data (Pagination).
    Handling multiple API calls shows you can manage large data volumes.
    """
    logger.info("🚀 Starting Multi-Page Extraction...")
    
    if not APP_ID or not APP_KEY:
        logger.error("API keys missing in .env file!")
        return

    all_jobs = []
    
    # LOOP THROUGH PAGES (1 to 5)
    for page in range(1, pages + 1):
        # Adzuna uses the page number in the URL path
        base_url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"
        
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50, # Max results per page
            "what": "python developer",
            "content-type": "application/json"
        }

        try:
            logger.info(f"📡 Requesting Page {page}...")
            response = requests.get(base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                all_jobs.extend(results)
                logger.info(f"✅ Page {page} Success: Gathered {len(results)} jobs.")
            elif response.status_code == 401:
                logger.error("❌ 401 Unauthorized: Check your API Keys in .env")
                break # Stop the loop if keys are wrong
            else:
                logger.warning(f"⚠️ Page {page} returned status: {response.status_code}")
            
            # RATE LIMITING: Good engineers wait 1 sec between calls to avoid getting banned
            time.sleep(1)

        except Exception as e:
            logger.error(f"⚠️ Network error on page {page}: {e}")
            continue # Try the next page even if one fails

    # SAVE ALL DATA TO RAW FOLDER
    if all_jobs:
        os.makedirs('data/raw', exist_ok=True)
        file_path = "data/raw/raw_jobs.json"
        
        # Maintain the dictionary structure your transform script expects
        final_payload = {"results": all_jobs}
        
        with open(file_path, "w") as f:
            json.dump(final_payload, f, indent=4)
            
        logger.info(f"🔥 EXTRACTION COMPLETE: Total {len(all_jobs)} jobs archived.")
    else:
        logger.error("❌ No data collected. Pipeline halting.")

if __name__ == "__main__":
    # We pull 5 pages x 50 jobs = up to 250 data points for your database!
    fetch_jobs(pages=5)
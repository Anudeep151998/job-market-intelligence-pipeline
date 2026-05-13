import time
import subprocess
import sys
import schedule # You'll need to add 'schedule' to requirements.txt

def job():
    print("🚀 Automation: Starting daily job extraction...")
    subprocess.run([sys.executable, "run_pipeline.py"])
    print("✅ Automation: Job complete.")

# Schedule the job every day at 08:00 AM
schedule.every().day.at("08:00").do(job)

print("📡 Worker started: Monitoring for scheduled tasks...")

while True:
    schedule.run_pending()
    time.sleep(60) # Check every minute
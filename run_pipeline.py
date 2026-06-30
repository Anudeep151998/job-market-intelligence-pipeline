# TODO: Implement robust pagination loop to handle high-volume data extraction safely.
import subprocess
import sys
import os
import time

def run_script(script_path):
    """Executes a script and handles terminal encoding for Windows."""
    print(f"\n--- ⚙️  Executing: {script_path} ---")
    
    # Force UTF-8 encoding for Windows terminals to handle emojis
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Run the script
    result = subprocess.run(
        [sys.executable, script_path], 
        capture_output=True, 
        text=True, 
        env=env,
        encoding="utf-8"
    )
    
    if result.returncode == 0:
        print(f"✅ Success: {script_path}")
        if result.stdout:
            print(result.stdout.strip())
        return True
    else:
        print(f"❌ ERROR in {script_path}:")
        print(result.stderr)
        return False

def main():
    start_time = time.time()
    print("========================================")
    print("🚀 STARTING EXTRAORDINARY ETL PIPELINE")
    print("========================================")

    # The 4-step sequence to impress recruiters
    pipeline_steps = [
        "scripts/extract.py",
        "scripts/transform.py",
        "scripts/validate.py",  # The 'Circuit Breaker'
        "scripts/load.py"       # The 'Smart Upsert'
    ]

    for step in pipeline_steps:
        if not run_script(step):
            print("\n🚨 PIPELINE HALTED: Please fix the error above.")
            sys.exit(1)

    duration = round(time.time() - start_time, 2)
    print("\n" + "="*40)
    print(f"🏁 PIPELINE COMPLETE IN {duration}s")
    print("========================================")
    print("👉 View your data: streamlit run app/dashboard.py")

if __name__ == "__main__":
    main()
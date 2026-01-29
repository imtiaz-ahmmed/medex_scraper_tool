from scraper.runner import run_scraper, SCRAPE_STATUS
import threading
import time

def monitor_progress():
    while SCRAPE_STATUS["status"] != "Completed":
        print(f"PROGRESS: {SCRAPE_STATUS['percent']}% | {SCRAPE_STATUS['status']} | Rem: {SCRAPE_STATUS['estimated_remaining']}")
        time.sleep(1)

print("Starting verification scrape (Limit 2)...")

# Start monitor in background
t = threading.Thread(target=monitor_progress, daemon=True)
t.start()

try:
    # Test retrieving 'A' with limit 2
    rows = run_scraper(["A"], limit=2)
    
    print("\n✅ Scrape finished.")
    print(f"Total Rows: {len(rows)}")
    
    if len(rows) > 0:
        print("Sample Row Keys:", rows[0].keys())
        print("Sample Row:", rows[0])
        
        if "dosage_form" in rows[0] and rows[0]["dosage_form"] != "N/A":
            print("✅ Dosage Form captured.")
        else:
             print("❌ Dosage Form Missing/N/A.")
             
        if "pack_size" in rows[0] and "dosage_form" in rows[0]:
            print("✅ New fields present.")
        else:
            print("❌ New fields MISSING.")
    else:
        print("❌ No rows returned.")

except Exception as e:
    print(f"❌ Error: {e}")

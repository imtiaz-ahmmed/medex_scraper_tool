import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url = "https://medex.com.bd/generics/2040/acalabrutinib/brand-names"

print(f"Fetching {url}...")
try:
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")
    
    # Select first brand row
    row = soup.select_one("tr.brand-row")
    if row:
        print("✅ Found brand row.")
        print("Attributes:", row.attrs)
        print("HTML Content:")
        print(row.prettify())
        
        # Check for pack size in columns
        cols = row.select("td")
        for i, col in enumerate(cols):
            print(f"Column {i}: {col.get_text(strip=True)}")
    else:
        print("❌ No brand row found.")
        print("First 500 chars:", r.text[:500])

except Exception as e:
    print(f"Error: {e}")

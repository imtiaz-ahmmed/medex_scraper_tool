from scraper.base import get_soup
from scraper.generics import scrape_generics

print("Testing scraper.base connectivity...")
try:
    soup = get_soup("https://medex.com.bd/generics?alpha=A")
    print("✅ Connection successful.")
    title = soup.title.text.strip() if soup.title else "No Title"
    print(f"Title: {title}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

print("\nTesting scrape_generics...")
try:
    results = scrape_generics(["A"], limit=5, herbal=0)
    print(f"Found {len(results)} generics.")
    if len(results) > 0:
        print("✅ scrape_generics working.")
        print("Sample:", results[0])
    else:
        print("❌ scrape_generics returned 0 results. Selectors might still be wrong.")
except Exception as e:
    print(f"❌ scrape_generics failed: {e}")

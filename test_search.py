import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def test_search(term):
    # Try AJAX search first as seen in page source
    url = f"https://medex.com.bd/ajax/search?term={term}&type=generics"
    print(f"Testing AJAX Search: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        print("Response (first 500 chars):", r.text[:500])
        
        try:
            data = r.json()
            print("JSON valid. Items found:", len(data))
            if len(data) > 0:
                print("Sample:", data[0])
        except:
            print("Not JSON response.")
            
    except Exception as e:
        print(f"Error: {e}")

    # Fallback to standard search if AJAX fails
    print("\nTesting Standard Search URL...")
    url2 = f"https://medex.com.bd/search?search={term}&type=generics"
    try:
        r = requests.get(url2, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            results = soup.select("a.hoverable-block")
            print(f"Standard Search Results: {len(results)}")
            if results:
                print("First Result:", results[0].text.strip(), results[0]['href'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search("Napa") # Popular brand/generic to test
    test_search("Acalabrutinib")

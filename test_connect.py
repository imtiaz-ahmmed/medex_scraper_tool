import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1"
}
url = "https://medex.com.bd/generics?alpha=A"

try:
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        links = soup.select("a[href^='/generics/']")
        if len(links) > 0:
            print(f"RESULT: SUCCESS Found {len(links)} links")
        else:
            print("RESULT: FAILURE No links found (but status 200)")
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("Saved HTML to page_dump.html")

    else:
        print(f"RESULT: FAILURE Status {r.status_code}")
except Exception as e:
    print(f"RESULT: FAILURE Exception {e}")

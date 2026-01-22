import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://medex.com.bd"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PROGRESS_FILE = "progress.json"


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"completed_generics": []}
    return json.load(open(PROGRESS_FILE, encoding="utf-8"))


def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, "w", encoding="utf-8"), indent=2)


def get_all_generics():
    """
    Returns list of:
    (generic_id, generic_name, generic_url)
    """
    url = f"{BASE}/generics"
    soup = BeautifulSoup(
        requests.get(url, headers=HEADERS).text, "lxml"
    )

    generics = []

    for a in soup.select("a.hoverable-block"):
        name = a.select_one(".dcind-title").text.strip()
        href = a.get("href")

        # ✅ SAFE URL BUILD
        generic_url = urljoin(BASE, href)
        # example: https://medex.com.bd/generics/779/10-vitamin-6-mineral...

        parts = generic_url.rstrip("/").split("/")
        gid = parts[-2]  # generic id always here

        generics.append((gid, name, generic_url))

    return generics


def scrape_brand_list(generic_url, generic_name, rows):
    """
    Scrape brand-names page
    """
    brand_url = generic_url.rstrip("/") + "/brand-names"

    print("  → Brand URL:", brand_url)

    soup = BeautifulSoup(
        requests.get(brand_url, headers=HEADERS).text, "lxml"
    )

    for r in soup.select("tr.brand-row"):
        rows.append({
            "generic_name": generic_name,
            "brand_name": r.get("data-name"),
            "strength": r.get("data-strength"),
            "company": r.get("data-company"),
            "unit_price": r.get("data-price")
        })


def run_scraper():
    progress = load_progress()
    done = set(progress["completed_generics"])

    generics = get_all_generics()[:10]   # 🔬 TEST MODE
    rows = []

    for gid, gname, generic_url in generics:
        if gid in done:
            continue

        print("Scraping:", gname)
        scrape_brand_list(generic_url, gname, rows)

        progress["completed_generics"].append(gid)
        save_progress(progress)

        time.sleep(1)

    print("✅ Total brands scraped:", len(rows))
    return rows

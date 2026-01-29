import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://medex.com.bd"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1"
}
PROGRESS_FILE = "progress.json"

# Global Progress State
SCRAPE_STATUS = {
    "total": 0,
    "current": 0,
    "percent": 0,
    "status": "Idle",
    "estimated_remaining": "0s"
}

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"completed_generics": []}
    return json.load(open(PROGRESS_FILE, encoding="utf-8"))


def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, "w", encoding="utf-8"), indent=2)


def get_all_generics_by_alpha(alphas):
    """
    Returns list of (generic_id, generic_name, generic_url) for given alphabets
    """
    generics = []
    
    # Handle "ALL" or empty list
    targets = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if alphas and alphas != ["ALL"] and alphas != "ALL":
        targets = alphas

    print(f"Fetching generics for: {targets}")
    
    for ch in targets:
        url = f"{BASE}/generics?alpha={ch}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "lxml")
            
            # Using the fixed selector
            for a in soup.select("a[href*='/generics/']"):
                name = a.select_one(".dcind-title").text.strip()
                href = a.get("href")
                
                # SAFE URL BUILD
                full_url = urljoin(BASE, href) 
                
                parts = full_url.rstrip("/").split("/")
                # usually generics/ID/NAME...
                if "generics" in parts:
                    idx = parts.index("generics")
                    if len(parts) > idx + 1:
                        gid = parts[idx+1]
                        generics.append((gid, name, full_url))
        except Exception as e:
            print(f"Error fetching alpha {ch}: {e}")
            
    return generics


def scrape_brand_list(generic_url, generic_name, rows):
    """
    Scrape brand-names page including Pack Size and Price
    """
    brand_url = generic_url.rstrip("/") + "/brand-names"
    
    try:
        r = requests.get(brand_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")

        for r in soup.select("tr.brand-row"):
            # Base attributes from data-*
            b_name = r.get("data-name")
            strength = r.get("data-strength")
            company = r.get("data-company")
            
            col_data = [td.get_text(" ", strip=True) for td in r.select("td")]
            # Expected: [Brand, Dosage, Strength, Company, PackSize+Price]
            
            dosage_form = col_data[1] if len(col_data) > 1 else "N/A"
            strength = col_data[2] if len(col_data) > 2 else "N/A"
            company = col_data[3] if len(col_data) > 3 else "N/A"
            
            # Pack Size & Price column (Last column usually)
            pack_price_text = col_data[-1] if col_data else ""
            
            # Format in image: "Unit Price: ৳ 1,000.00 (1 x 30: ৳ 30,000.00)"
            # We want to perform smart extraction
            unit_price = r.get("data-price") or "N/A"
            pack_size = "N/A"
            
            if "(" in pack_price_text and ")" in pack_price_text:
                # Extract content inside parens as pack size info
                try:
                    pack_size = pack_price_text.split("(")[1].split(")")[0]
                except:
                    pack_size = pack_price_text
            elif "Pack Size:" in pack_price_text:
                 pack_size = pack_price_text.replace("Pack Size:", "").strip()

            rows.append({
                "generic_name": generic_name,
                "brand_name": b_name,
                "dosage_form": dosage_form,
                "strength": strength,
                "company": company,
                "pack_size": pack_size,
                "unit_price": unit_price
            })
            
    except Exception as e:
        print(f"Error scraping brands for {generic_name}: {e}")


def run_scraper(alphabets, limit=None):
    global SCRAPE_STATUS
    
    SCRAPE_STATUS["status"] = "Fetching Generics List..."
    SCRAPE_STATUS["percent"] = 0
    SCRAPE_STATUS["total"] = 0
    
    generics = get_all_generics_by_alpha(alphabets)
    
    if limit:
        try:
            generics = generics[:int(limit)]
        except:
            pass
        
    total = len(generics)
    SCRAPE_STATUS["total"] = total
    SCRAPE_STATUS["current"] = 0
    
    rows = []
    start_time = time.time()
    
    print(f"Starting scrape for {total} generics...")
    
    for i, (gid, gname, generic_url) in enumerate(generics):
        SCRAPE_STATUS["status"] = f"Scraping [{gname}]"
        
        scrape_brand_list(generic_url, gname, rows)
        
        # Update Progress
        current = i + 1
        SCRAPE_STATUS["current"] = current
        SCRAPE_STATUS["percent"] = int((current / total) * 100) if total > 0 else 0
        
        elapsed = time.time() - start_time
        if current > 0:
            avg_time = elapsed / current
            remaining = avg_time * (total - current)
            SCRAPE_STATUS["estimated_remaining"] = f"{int(remaining)}s"
        
        # time.sleep(0.5) # Polite delay (optional, can adjust)

    SCRAPE_STATUS["status"] = "Completed"
    SCRAPE_STATUS["percent"] = 100
    SCRAPE_STATUS["estimated_remaining"] = "0s"
    
    print(f"✅ Scrape Complete. Total rows: {len(rows)}")
    return rows


def search_generic(text):
    """
    Search for a generic by name. Returns list of {name, url, id}.
    """
    url = f"{BASE}/search?search={text}&type=generics"
    results = []
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        
        # Search results are usually a.hoverable-block
        for a in soup.select("a.hoverable-block"):
            name = a.select_one(".dcind-title").text.strip() if a.select_one(".dcind-title") else a.text.strip()
            href = a.get("href")
            
            # Simple validation
            if "generics" in href:
                full_url = urljoin(BASE, href)
                results.append({
                    "name": name,
                    "url": full_url
                })
    except Exception as e:
        print(f"Search error: {e}")
        
    return results

def scrape_single_generic(url, name):
    """
    Scrape a specific generic URL.
    """
    global SCRAPE_STATUS
    SCRAPE_STATUS["status"] = "Preparing..."
    SCRAPE_STATUS["percent"] = 0
    SCRAPE_STATUS["total"] = 1
    SCRAPE_STATUS["current"] = 0
    
    rows = []
    SCRAPE_STATUS["status"] = f"Scraping {name}..."
    
    scrape_brand_list(url, name, rows)
    
    SCRAPE_STATUS["current"] = 1
    SCRAPE_STATUS["percent"] = 100
    SCRAPE_STATUS["status"] = "Completed"
    
    return rows

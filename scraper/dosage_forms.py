from scraper.base import get_soup

def scrape_dosage_forms(limit):
    soup = get_soup("https://medex.com.bd/dosage-forms")
    rows = []

    for li in soup.select("li.list-group-item"):
        rows.append({
            "dosage_form": li.text.strip()
        })

        if len(rows) >= limit:
            break

    return rows

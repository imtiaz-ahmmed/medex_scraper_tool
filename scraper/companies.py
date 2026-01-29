from scraper.base import get_soup, abs_url

def scrape_companies(alphabets, limit, herbal):
    results = []
    count = 0

    for ch in (alphabets or list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
        url = f"https://medex.com.bd/companies?alpha={ch}"
        if herbal:
            url += "&herbal=1"

        soup = get_soup(url)
        for a in soup.select("a[href*='/companies/']"):
            results.append({
                "type": "Company",
                "alphabet": ch,
                "name": a.text.strip(),
                "url": abs_url(a["href"])
            })
            count += 1
            if limit and count >= limit:
                return results

    return results

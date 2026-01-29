from scraper.base import get_soup, abs_url

def scrape_generics(alphabets, limit, herbal):
    results = []
    count = 0

    for ch in (alphabets or list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
        url = f"https://medex.com.bd/generics?alpha={ch}"
        if herbal:
            url += "&herbal=1"

        soup = get_soup(url)
        for a in soup.select("a[href*='/generics/']"):
            name = a.text.strip()
            link = abs_url(a["href"])
            results.append({
                "type": "Generic",
                "alphabet": ch,
                "name": name,
                "url": link
            })
            count += 1
            if limit and count >= limit:
                return results

    return results

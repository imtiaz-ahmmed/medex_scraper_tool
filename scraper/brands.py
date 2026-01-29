from scraper.base import get_soup, abs_url, bn_url

def scrape_brands(alphabets, limit, herbal):
    results = []
    count = 0

    for ch in (alphabets or list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
        url = f"https://medex.com.bd/brands?alpha={ch}"
        if herbal:
            url += "&herbal=1"

        soup = get_soup(url)
        for a in soup.select("a[href*='/brands/']"):
            en = abs_url(a["href"])
            bn = bn_url(en)

            results.append({
                "type": "Brand",
                "alphabet": ch,
                "name": a.text.strip(),
                "url_en": en,
                "url_bn": bn
            })
            count += 1
            if limit and count >= limit:
                return results

    return results

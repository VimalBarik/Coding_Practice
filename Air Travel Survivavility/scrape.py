import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ASN-Scraper/1.0; +https://example.com)"
}

BASE_URL = "https://aviation-safety.net"

def get_total_pages(year):
    url = f"{BASE_URL}/database/year/{year}"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        nav = soup.find("div", class_="pagenumbers")
        if not nav:
            return 1
        pages = nav.find_all("a")
        numbers = [int(p.get_text()) for p in pages if p.get_text().isdigit()]
        return max(numbers) if numbers else 1
    except Exception as e:
        print(f"[!] Error getting page count for {year}: {e}")
        return 1

def scrape_page(year, page):
    url = f"{BASE_URL}/database/year/{year}/{page}"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", class_="hp")
        if not table:
            return []

        rows = table.find_all("tr", class_="list")
        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 6:
                continue
            data.append({
                "year": year,
                "date": cols[0].get_text(strip=True),
                "type": cols[1].get_text(strip=True),
                "registration": cols[2].get_text(strip=True),
                "operator": cols[3].get_text(strip=True),
                "fatalities": cols[4].get_text(strip=True),
                "location": cols[5].get_text(strip=True),
                "damage": cols[7].get_text(strip=True) if len(cols) > 7 else None
            })
        return data
    except Exception as e:
        print(f"[!] Error scraping {url}: {e}")
        return []

def scrape_all(start_year=1990, end_year=2025):
    all_data = []
    for year in range(start_year, end_year + 1):
        print(f"\n📆 Year: {year}")
        total_pages = get_total_pages(year)
        print(f"   → Total pages: {total_pages}")

        for page in range(1, total_pages + 1):
            print(f"     Scraping page {page}/{total_pages}...")
            page_data = scrape_page(year, page)
            all_data.extend(page_data)
            time.sleep(1)  # polite delay

    return pd.DataFrame(all_data)

# Run the scraper and export
df = scrape_all()
df.to_csv("asn_accidents_1990_2025.csv", index=False)
print(f"\n✅ Done. Total accidents scraped: {len(df)}")

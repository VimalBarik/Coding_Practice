import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
BASE_URL = "https://aviation-safety.net"

def extract_detail_data(detail_url):
    try:
        res = requests.get(BASE_URL + detail_url, headers=HEADERS)
        soup = BeautifulSoup(res.content, 'html.parser')
        rows = soup.select("table tr")
        data = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True).replace(":", "")
                value = cols[1].get_text(" ", strip=True)
                data[key] = value
        return data
    except Exception as e:
        print(f"Error fetching {detail_url}: {e}")
        return {}

def scrape_accidents(start_year=1990, end_year=2025):
    all_accidents = []
    for year in range(start_year, end_year + 1):
        page = 1
        while True:
            print(f"Scraping {year}, page {page}...")
            url = f"{BASE_URL}/database/year/{year}/{page}"
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                break
            soup = BeautifulSoup(res.content, 'html.parser')
            rows = soup.select("tr.list")
            if not rows:
                break

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 6:
                    continue
                date = cols[0].get_text(strip=True)
                detail_link = cols[0].find("a")
                type_ = cols[1].get_text(strip=True)
                reg = cols[2].get_text(strip=True)
                operator = cols[3].get_text(strip=True)
                fatalities = cols[4].get_text(strip=True)
                location = cols[5].get_text(strip=True)
                detail_url = detail_link['href'] if detail_link else None

                accident = {
                    "Date": date,
                    "Type": type_,
                    "Registration": reg,
                    "Operator": operator,
                    "Fatalities": fatalities,
                    "Location": location,
                    "Detail URL": BASE_URL + detail_url if detail_url else ""
                }

                if detail_url:
                    detail_data = extract_detail_data(detail_url)
                    accident.update(detail_data)

                all_accidents.append(accident)
                time.sleep(0.5)

            page += 1
            time.sleep(1)

    return pd.DataFrame(all_accidents)

if __name__ == "__main__":
    df = scrape_accidents(start_year=1990, end_year=2025)  # change range as needed
    df.to_csv("aviation_accidents_detailed.csv", index=False)
    print("Saved to aviation_accidents_detailed.csv")

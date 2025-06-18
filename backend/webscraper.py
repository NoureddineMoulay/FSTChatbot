import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_filiere(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}

    # Get all the boxes at the top (like Diplôme, Coordonnateur, etc.)
    infos_grid = soup.select_one("div.formation-detail-infos")
    if infos_grid:
        info_boxes = infos_grid.select("div.formation-detail-infos--box")
        for box in info_boxes:
            title_span = box.select_one(".formation-detail-infos--box-title .sub-title")
            value_span = box.select_one(".formation-detail-infos--box-title .title")
            if title_span and value_span:
                title = title_span.get_text(strip=True)
                value = value_span.get_text(strip=True)
                data[title] = value

    # Get the detail sections like Objectifs, Compétences, Débouchés, Modalités, etc.
    for title_tag in soup.select(".formation-detail-title"):
        section_title = title_tag.get_text(strip=True)
        section_content = []
        next_el = title_tag.find_next_sibling()
        while next_el and next_el.name != 'h4':
            if next_el.name == 'ul':
                section_content.extend([li.get_text(strip=True) for li in next_el.find_all("li")])
            elif next_el.name == 'div':
                text = next_el.get_text(strip=True)
                if text:
                    section_content.append(text)
            next_el = next_el.find_next_sibling()

        if section_content:
            data[section_title] = section_content

    # Get the Programme (accordion tables by semester)
    programme_data = {}
    accordion = soup.find("div", id="modules-accordion")
    if accordion:
        for item in accordion.find_all("div", class_="accordion-item"):
            sem_title = item.find("button").get_text(strip=True)
            table = item.find("table")
            if not table:
                continue
            rows = []
            for tr in table.find_all("tr"):
                row_data = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if row_data:
                    rows.append(row_data)
            programme_data[sem_title] = rows
    if programme_data:
        data["Programme"] = programme_data

    return data

def scrape_all_formations(base_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    page = 1
    all_data = []

    while True:
        url = f"{base_url}&page={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        formation_links = [a['href'] for a in soup.select('a.formations-content--item[href]')]
        if not formation_links:
            break

        for link in formation_links:
            print(f"Scraping {link}...")
            try:
                full_url = link if link.startswith("http") else f"https://www.uca.ma{link}"
                data = scrape_filiere(full_url)
                data["URL"] = full_url
                all_data.append(data)
                time.sleep(1)  # Be kind to the server
            except Exception as e:
                print(f"Error scraping {link}: {e}")

        page += 1

    return all_data

if __name__ == "__main__":
    base_url = "https://www.uca.ma/fr/formations/formation-initiale?etablissements%5B0%5D=113"
    all_formations = scrape_all_formations(base_url)
    with open("fstg_formations.json", "w", encoding="utf-8") as f:
        json.dump(all_formations, f, ensure_ascii=False, indent=2)
    print("Scraping all formations completed. Data saved to fstg_formations.json")

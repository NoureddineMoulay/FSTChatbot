import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.fstg-marrakech.ac.ma/FST/departements.html'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

departements = []

# Chaque département est dans une div de classe col-xs-12 col-sm-6 col-md-6
for dept_div in soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-6'):
    title_tag = dept_div.find('h4')
    chef_label = dept_div.find('h6')
    chef_name = dept_div.find('h5')

    # Rechercher le téléphone et l'email
    contact_info = dept_div.find('ul', class_='list-inline')
    phone = email = None
    if contact_info:
        li_tags = contact_info.find_all('li')
        for li in li_tags:
            icon = li.find('i')
            if icon and 'fa-phone' in icon.get('class', []):
                phone = li.find('a').get_text(strip=True)
            elif icon and 'fa-envelope-o' in icon.get('class', []):
                email = li.find('a').get_text(strip=True)

    if title_tag and chef_label and chef_name:
        departements.append({
            'departement': title_tag.get_text(strip=True),
            'chef_label': chef_label.get_text(strip=True),
            'chef_nom': chef_name.get_text(strip=True),
            'telephone': phone,
            'email': email
        })

with open('departements_fstg.json', 'w', encoding='utf-8') as f:
    json.dump(departements, f, ensure_ascii=False, indent=4)

print("Scraping terminé. Données sauvegardées dans 'departements_fstg.json'.")

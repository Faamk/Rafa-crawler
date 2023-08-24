import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://storage.googleapis.com/jus-challenges/challenge-crawler.html"

# Make an HTTP GET request to fetch the HTML content
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object for parsing
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the rows containing data
data_rows = soup.find_all('table', {'cellspacing': '0', 'cellpadding': '0'})

# Initialize a list to store extracted data
extracted_data = []

# Iterate through each row and extract relevant information
for row in data_rows:
    item = {}
    item['numero_processo'] = row.find('a').text.strip()

    try:
        item['ementa'] = " ".join(row.find('strong', string=lambda text: 'Ementa:' in text).find_next('div').text.split())
    except AttributeError:
        item['ementa'] = ""

    try:
        item['relator'] = row.find('strong', string=lambda text: 'Relator(a):' in text).next_sibling.strip()
    except AttributeError:
        item['relator'] = ""

    try:
        item['comarca'] = row.find('strong', string=lambda text: 'Comarca:' in text).next_sibling.strip()
    except AttributeError:
        item['comarca'] = ""

    try:
        item['orgao_julgador'] = row.find('strong', string=lambda text: 'Órgão julgador:' in text).next_sibling.strip()
    except AttributeError:
        item['orgao_julgador'] = ""

    try:
        item['data_julgamento'] = row.find('strong', string=lambda text: 'Data do julgamento:' in text).next_sibling.strip()
    except AttributeError:
        item['data_julgamento'] = ""

    try:
        item['classe_assunto'] = row.find('strong', string=lambda text: 'Classe/Assunto:' in text).next_sibling.strip()
    except AttributeError:
        item['classe_assunto'] = ""

    try:
        item['data_publicacao'] = row.find('strong', string=lambda text: 'Data de publicação:' in text).next_sibling.strip()
    except AttributeError:
        item['data_publicacao'] = ""

    extracted_data.append(item)

# Save the extracted data in JSON format
with open('extracted_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)

print("Data extraction and structuring completed.")

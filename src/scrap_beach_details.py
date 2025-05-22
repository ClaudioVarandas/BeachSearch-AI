import csv
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import re
from urllib.parse import urlparse, parse_qs

# Configuration
INPUT_CSV = './data/snirh_praias_infopraia_vwm.csv'  # Your input CSV file
OUTPUT_CSV = './data/scraped_beach_data_details.csv'  # New file with only codes and scraped data
BASE_URL = 'https://infoagua.apambiente.pt/pt/praias/praia-detalhe/'
DELAY = 1  # Seconds between requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_beach_data(codigo):
    """Scrape beach information from the website"""
    url = f"{BASE_URL}{codigo}"
    data = {'Código': codigo, 'URL': url}
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10,allow_redirects=False)
        response.raise_for_status()

        if response.status_code != 200:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract basic information
        name = soup.find('div', class_='page-title')
        data['Nome da praia'] = name.find('span').get_text(strip=True)
        
        # Extract information about the season
        info_container = soup.find('div', class_='main-container')
        left_col = info_container.find('div', class_='left-column')
        info = left_col.find('div', class_='info')
        info_title = info.find('div', class_='title').get_text(' ',strip=True)
        info_title_clean = re.sub(r'\s+', ' ', info_title).strip()

        info_status = info.find('div', class_='status').get_text(' ',strip=True)
        info_date = info.find('div', class_='date').get_text(' ',strip=True)
        info_date_clean = re.sub(r'\s+', ' ', info_date).strip()

        data['Informação epoca balnear'] = info_title_clean + ', estado : ' + info_status + ', calendario : de ' + info_date_clean.replace('-', 'a')


        # Extract water classification
        water_classification_container = soup.find('div', class_='beach-classification')
        water_classification_text = water_classification_container.find('div', class_='text').get_text(strip=True)
        data['Classificação da água'] = water_classification_text

        # Extract coordinates
        coordinates_container = soup.find('div', class_='header-additional-info')
        coordinates_url = coordinates_container.find('a', class_='button')['href']
        parsed_url = urlparse(coordinates_url)
        query_params = parse_qs(parsed_url.query)
        q_value = query_params.get('q', [None])[0]
        data['Coordenadas'] = q_value

        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {codigo}: {str(e)}")
        return None

def main():
    # Get all beach codes from CSV
    with open(INPUT_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        beach_codes = [row['Código da Praia'] for row in reader]
    
    # Prepare output fields
    fieldnames = [
        'Código',
        'URL',
        'Nome da praia',
        'Informação epoca balnear',
        'Classificação da água',
        'Coordenadas'
    ]
    
    # Scrape and save data
    with open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, codigo in enumerate(beach_codes, 1):
            print(f"Processing {i}/{len(beach_codes)}: {codigo}")
            
            beach_data = scrape_beach_data(codigo)
            if beach_data:
                writer.writerow(beach_data)
            
            time.sleep(DELAY)
    
    print(f"Scraping complete. Data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
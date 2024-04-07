import subprocess
import argparse
import shutil
import time

from bs4 import BeautifulSoup
import re
import requests


# Comprueba si python está disponible, si no, usa python3
python_bin = "python" if shutil.which("python") else "python3"

def invoke_scraper(mode, id, debug, delay):
    command = [python_bin, "./src/scraper.py", mode, str(id)]
    if debug:
        command.append("--debug")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el scraper: {e}")
    time.sleep(delay)

def date(mode, start_id, debug, delay):
    # Construye la url para la fecha indicada.
    base_url = "https://www.whakoom.com"
    url = f"{base_url}/newtitles/{start_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        print("Error al obtener la página:", response.status_code)
        return None
    
    # Encuentra todos los enlaces de los cómics de la fecha indicada
    comic_links = soup.find_all('a', href=re.compile(r"^/comics/"))

    # Extrae los ID de los enlaces
    comic_ids = [link['href'].split('/')[2] for link in comic_links]
    
    # Ejecuta el scraper para cada ID
    for i in comic_ids:
        invoke_scraper(mode, i, debug, delay)
    
def main(mode, start_id, end_id, debug, delay):
    if mode == 'ediciones':
        try:
            start_id = int(start_id)
            end_id = int(end_id) if end_id is not None else start_id  # If end_id is None, use start_id
        except ValueError:
            print("start_id y end_id deben ser números enteros.")
            return
        for id in range(start_id, end_id + 1):
            invoke_scraper(mode, id, debug, delay)
    elif mode == 'comics':
        invoke_scraper(mode, start_id, debug, delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape a Whakoom page.')
    parser.add_argument('mode', choices=['ediciones', 'comics'], help='The type of page to scrape.')
    parser.add_argument('start_id', help='The ID of the page to start scraping.')
    parser.add_argument('end_id', nargs='?', default=None, help='The ID of the page to end scraping. If not provided, it will be the same as start_id.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument('--delay', nargs='?', default=0, type=int, help='Time to wait between requests.')
    parser.add_argument('--date', action='store_true', help='Explore YYYYMM indicated in start_id, to get comics.')
    args = parser.parse_args()
    if args.date:
        # If date is provided, we will scrape comics
        args.mode = 'comics'
        date(args.mode, args.start_id, args.debug, args.delay)
    else:
        main(args.mode, args.start_id, args.end_id, args.debug, args.delay)
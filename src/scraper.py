import requests
import argparse
import json
import pymongo
from bs4 import BeautifulSoup

def connect_to_db():
    client = pymongo.MongoClient("mongodb://root:example@localhost:27018/")
    db = client["comics"]
    collection = db["comiteca"]
    return collection

def parse_args():
    parser = argparse.ArgumentParser(description='Scrape a Whakoom page.')
    parser.add_argument('page_type', choices=['ediciones', 'comics'], help='The type of page to scrape.')
    parser.add_argument('page_id', help='The ID of the page to scrape.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    return parser.parse_args()

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print("Error al obtener la página:", response.status_code)
        return None

def scrape_page(soup, page_type, url):
    # Obtener el título de la página
    title = soup.title.text.strip()

    # Obtener el número del artículo es el id, pero se puede extraer de la URL
    item_number = url.split("/")[-1]

    # Obtener la descripción del artículo
    description = soup.find("meta", {"name": "description"})["content"]

    # Encontrar todos los elementos <a> dentro de <p> dentro de <div class="tags">
    if page_type == 'ediciones':
        raw_authors_dom = soup.select('div.tags p a')
        if raw_authors_dom == []:
            raw_authors_dom = soup.select('div.authors.info-item p a')
    else:
        # Encontrar todos los elementos <a> dentro de <p> dentro de <div class="authors info-item">
        raw_authors_dom = soup.select('div.authors.info-item p a')
    
    # Extraer el texto de cada elemento y normalizarlo (eliminar espacios en blanco adicionales)
    authors = [author.get_text(strip=True) for author in raw_authors_dom]
    
    # Obtener la URL de la portada (cover)
    cover = soup.find("meta", property="og:image")["content"]

    # Obtener la fecha de publicación
    try:
        published_date_p = soup.select_one('p[itemprop="datePublished"]')['content']
    except:
        published_date_p = None
    publish_date = published_date_p


    # Obtener la calificación (rating)
    rating_element = soup.select_one('span.stars span.stars-bg span.stars-value')

    # Verificar si se encontró el elemento
    if rating_element:
        # Extraer el texto y convertirlo a un número
        rating = float(rating_element.text.strip())
    else:
        rating = None

    # Obtener el idioma y editor
    spans = soup.select('p.lang-pub span')
    lenguage = (spans[1].text) if len(spans) > 1 else None

    # Crear un diccionario con los datos obtenidos
    data = {
        "Titulo": title,
        "Numero de articulo": item_number,
        "Descripcion": description,
        "Autores": authors,
        "Rating:" : rating,
        "Fecha de publicacion": publish_date,
        "Portada": cover,
        "Idioma": lenguage
    }

    return data

def insert_data(collection, data, debug):
    if not debug:
        insert_result = collection.insert_one(data)
        if insert_result.acknowledged:
            print("Los datos se han insertado correctamente en MongoDB.")
        else:
            print("Error al insertar los datos en MongoDB.")

def main():
    args = parse_args()
    base_url = "https://www.whakoom.com"
    url = f"{base_url}/{args.page_type}/{args.page_id}"
    soup = fetch_page(url)
    if soup is not None:
        data = scrape_page(soup, args.page_type, url)
        print(json.dumps(data, indent=4))
        collection = connect_to_db()
        insert_data(collection, data, args.debug)

if __name__ == "__main__":
    main()
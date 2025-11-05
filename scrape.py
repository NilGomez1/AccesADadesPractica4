import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL_BASE = "http://books.toscrape.com/index.html"
NOMBRE_ARCHIVO_CSV = 'libros.csv'
DELIMITADOR_CSV = ';'


def obtener_datos_libros(url):
    print(f"Iniciando scraping en: {url}")
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return []

    soup = BeautifulSoup(respuesta.content, 'html.parser')
    libros = soup.find_all('article', class_='product_pod')
    datos_libros = []

    for libro in libros:
        titulo = libro.find('h3').find('a')['title']

        precio_str = libro.find('p', class_='price_color').text

        precio_limpio = re.sub(r'[^\d.]', '', precio_str)
        precio = float(precio_limpio)

        rating_tag = libro.find('p', class_='star-rating')
        rating_clase = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else 'N/A'

        datos_libros.append({
            'Titulo': titulo,
            'Precio': precio,
            'Rating_Clase': rating_clase
        })

    return datos_libros


datos_extraidos = obtener_datos_libros(URL_BASE)

if datos_extraidos:
    df_libros = pd.DataFrame(datos_extraidos)

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'N/A': 0}
    df_libros['Rating_Numerico'] = df_libros['Rating_Clase'].map(rating_map)

    df_libros.to_csv(NOMBRE_ARCHIVO_CSV, index=False, sep=DELIMITADOR_CSV, encoding='utf-8')

    print(f"\nDatos guardados exitosamente en '{NOMBRE_ARCHIVO_CSV}'.")
    print(f"Se ha usado el delimitador '{DELIMITADOR_CSV}' para separar las columnas.")
    print("\nPrimeras filas del DataFrame:")
    print(df_libros.head())
else:

    print("\nNo se extrajeron datos. Revisa la URL o los selectores HTML.")

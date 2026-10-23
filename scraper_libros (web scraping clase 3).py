#!/usr/bin/env python3  # Indica que el archivo puede ejecutarse como script de Python en sistemas Unix/Linux.
# -*- coding: utf-8 -*-  # Define la codificación del archivo para permitir caracteres en español.

"""  # Inicia la documentación general del programa.
Programa: scraper_libros.py  # Nombre sugerido para este script.
Objetivo: descargar información pública de libros desde Books to Scrape y generar archivos JSON y CSV.  # Explica el propósito del programa.
Uso útil: crear un catálogo de libros económicos, por ejemplo libros con precio menor o igual a 20 libras.  # Describe el fin práctico del resultado.
Sitio de práctica: https://books.toscrape.com/  # Indica la web pública usada para practicar scraping.
"""  # Finaliza la documentación general del programa.

import csv  # Importa el módulo estándar para escribir archivos CSV.
import json  # Importa el módulo estándar para escribir archivos JSON.
import time  # Importa el módulo estándar para pausar el programa entre solicitudes.
from pathlib import Path  # Importa Path para manejar rutas de archivos de forma clara.
from urllib.parse import urljoin  # Importa urljoin para construir URLs absolutas desde enlaces relativos.

import requests  # Importa requests para descargar el contenido HTML de la página web.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para analizar y extraer datos del HTML.

BASE_URL = "https://books.toscrape.com/"  # Define la URL principal del sitio web que se va a scrapear.
CATALOGUE_URL = urljoin(BASE_URL, "catalogue/")  # Define la URL base del catálogo donde están las páginas paginadas.
OUTPUT_JSON = Path("libros_economicos.json")  # Define el nombre del archivo JSON de salida.
OUTPUT_CSV = Path("libros_economicos.csv")  # Define el nombre del archivo CSV de salida.
MAX_PAGES = 3  # Define cuántas páginas del catálogo se van a descargar para evitar hacer demasiadas solicitudes.
PRICE_LIMIT = 20.00  # Define el precio máximo para considerar que un libro es económico.
REQUEST_PAUSE_SECONDS = 1  # Define una pausa entre solicitudes para ser respetuosos con el sitio web.


def descargar_html(url):  # Define una función para descargar el HTML de una URL.
    """Descarga una página web y devuelve su contenido HTML."""  # Documenta qué hace la función.
    headers = {  # Crea un diccionario de encabezados HTTP para identificar la solicitud.
        "User-Agent": "Mozilla/5.0 (compatible; ScraperEducativo/1.0)"  # Define un User-Agent simple y descriptivo.
    }  # Cierra el diccionario de encabezados.
    respuesta = requests.get(url, headers=headers, timeout=15)  # Realiza la solicitud GET con tiempo máximo de espera.
    respuesta.raise_for_status()  # Lanza un error si la respuesta HTTP indica fallo.
    return respuesta.text  # Devuelve el contenido HTML como texto.


def limpiar_precio(texto_precio):  # Define una función para convertir el precio de texto a número decimal.
    """Convierte un precio como '£51.77' en un número float como 51.77."""  # Documenta la transformación del precio.
    precio_limpio = texto_precio.replace("£", "").strip()  # Quita el símbolo de libra y espacios adicionales.
    return float(precio_limpio)  # Convierte el texto limpio a número decimal.


def convertir_rating_a_numero(clases):  # Define una función para convertir el rating textual a número.
    """Convierte clases CSS como 'Three' en un valor numérico como 3."""  # Documenta la conversión del rating.
    mapa_ratings = {  # Crea un diccionario para mapear palabras en inglés a números.
        "One": 1,  # Asocia la palabra One con el número 1.
        "Two": 2,  # Asocia la palabra Two con el número 2.
        "Three": 3,  # Asocia la palabra Three con el número 3.
        "Four": 4,  # Asocia la palabra Four con el número 4.
        "Five": 5,  # Asocia la palabra Five con el número 5.
    }  # Cierra el diccionario de ratings.
    for clase in clases:  # Recorre cada clase CSS encontrada en el elemento de rating.
        if clase in mapa_ratings:  # Verifica si la clase corresponde a un rating conocido.
            return mapa_ratings[clase]  # Devuelve el número asociado al rating.
    return None  # Devuelve None si no se encuentra ningún rating válido.


def extraer_libros_de_pagina(html, url_pagina):  # Define una función para extraer libros desde el HTML de una página.
    """Extrae título, precio, disponibilidad, rating y URL de cada libro listado."""  # Documenta los campos extraídos.
    soup = BeautifulSoup(html, "html.parser")  # Crea un objeto BeautifulSoup para analizar el HTML.
    tarjetas = soup.select("article.product_pod")  # Selecciona todas las tarjetas de libros de la página.
    libros = []  # Crea una lista vacía para guardar los libros extraídos.

    for tarjeta in tarjetas:  # Recorre cada tarjeta de libro encontrada.
        titulo = tarjeta.h3.a["title"].strip()  # Extrae y limpia el título completo del libro.
        precio_texto = tarjeta.select_one("p.price_color").get_text(strip=True)  # Extrae el precio como texto.
        precio = limpiar_precio(precio_texto)  # Convierte el precio textual a número decimal.
        disponibilidad = tarjeta.select_one("p.instock.availability").get_text(strip=True)  # Extrae la disponibilidad.
        rating_clases = tarjeta.select_one("p.star-rating").get("class", [])  # Obtiene las clases CSS del rating.
        rating = convertir_rating_a_numero(rating_clases)  # Convierte las clases CSS del rating a número.
        url_relativa = tarjeta.h3.a["href"]  # Extrae el enlace relativo del detalle del libro.
        url_libro = urljoin(url_pagina, url_relativa)  # Convierte el enlace relativo en URL absoluta.

        libro = {  # Crea un diccionario con los datos normalizados del libro.
            "titulo": titulo,  # Guarda el título del libro.
            "precio_gbp": precio,  # Guarda el precio en libras esterlinas como número.
            "disponibilidad": disponibilidad,  # Guarda el estado de disponibilidad.
            "rating_1_a_5": rating,  # Guarda el rating numérico entre 1 y 5.
            "url": url_libro,  # Guarda la URL absoluta del libro.
            "es_economico": precio <= PRICE_LIMIT,  # Marca si el libro cumple el criterio de precio económico.
        }  # Cierra el diccionario del libro.
        libros.append(libro)  # Agrega el diccionario del libro a la lista de resultados.

    return libros  # Devuelve la lista de libros extraídos de la página.


def obtener_url_pagina(numero_pagina):  # Define una función para construir la URL de cada página del catálogo.
    """Devuelve la URL correcta para la página solicitada del catálogo."""  # Documenta el objetivo de la función.
    if numero_pagina == 1:  # Verifica si se solicita la primera página.
        return urljoin(BASE_URL, "index.html")  # Devuelve la URL de la primera página.
    return urljoin(CATALOGUE_URL, f"page-{numero_pagina}.html")  # Devuelve la URL de una página paginada.


def guardar_json(libros, ruta_salida):  # Define una función para guardar los datos en formato JSON.
    """Guarda la lista de libros en un archivo JSON legible."""  # Documenta qué hace la función.
    with ruta_salida.open("w", encoding="utf-8") as archivo_json:  # Abre el archivo JSON en modo escritura con UTF-8.
        json.dump(libros, archivo_json, ensure_ascii=False, indent=4)  # Escribe datos con acentos y formato legible.


def guardar_csv(libros, ruta_salida):  # Define una función para guardar los datos en formato CSV.
    """Guarda la lista de libros en un archivo CSV compatible con planillas de cálculo."""  # Documenta qué hace la función.
    columnas = ["titulo", "precio_gbp", "disponibilidad", "rating_1_a_5", "url", "es_economico"]  # Define columnas del CSV.
    with ruta_salida.open("w", encoding="utf-8", newline="") as archivo_csv:  # Abre el CSV evitando líneas en blanco extra.
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)  # Crea un escritor CSV basado en diccionarios.
        escritor.writeheader()  # Escribe la fila de encabezados del CSV.
        escritor.writerows(libros)  # Escribe una fila por cada libro de la lista.


def main():  # Define la función principal del programa.
    """Ejecuta el scraping, filtra los datos útiles y genera JSON y CSV."""  # Documenta el flujo principal.
    todos_los_libros = []  # Crea una lista para acumular libros de todas las páginas.

    for numero_pagina in range(1, MAX_PAGES + 1):  # Recorre desde la página 1 hasta la cantidad máxima configurada.
        url_pagina = obtener_url_pagina(numero_pagina)  # Construye la URL de la página actual.
        print(f"Descargando página {numero_pagina}: {url_pagina}")  # Muestra en consola qué página se está descargando.
        html = descargar_html(url_pagina)  # Descarga el HTML de la página actual.
        libros_pagina = extraer_libros_de_pagina(html, url_pagina)  # Extrae los libros de esa página.
        todos_los_libros.extend(libros_pagina)  # Agrega los libros extraídos a la lista acumulada.
        time.sleep(REQUEST_PAUSE_SECONDS)  # Espera unos segundos antes de pedir otra página.

    libros_economicos = [  # Crea una nueva lista usando comprensión de listas.
        libro for libro in todos_los_libros if libro["es_economico"]  # Filtra únicamente libros con precio menor o igual al límite.
    ]  # Cierra la comprensión de listas.

    libros_economicos.sort(key=lambda libro: (libro["precio_gbp"], -(libro["rating_1_a_5"] or 0)))  # Ordena por precio y luego por mejor rating.
    guardar_json(libros_economicos, OUTPUT_JSON)  # Guarda los libros económicos en un archivo JSON.
    guardar_csv(libros_economicos, OUTPUT_CSV)  # Guarda los libros económicos en un archivo CSV.

    print(f"Libros analizados: {len(todos_los_libros)}")  # Muestra la cantidad total de libros analizados.
    print(f"Libros económicos encontrados: {len(libros_economicos)}")  # Muestra cuántos libros pasaron el filtro.
    print(f"Archivo JSON generado: {OUTPUT_JSON.resolve()}")  # Muestra la ruta absoluta del JSON creado.
    print(f"Archivo CSV generado: {OUTPUT_CSV.resolve()}")  # Muestra la ruta absoluta del CSV creado.


if __name__ == "__main__":  # Verifica que el archivo se esté ejecutando directamente y no importando.
    main()  # Ejecuta la función principal del programa.

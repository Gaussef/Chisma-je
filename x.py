import requests
from bs4 import BeautifulSoup
import re

# Encabezados para simular una solicitud desde un navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def obtener_proxies():
    # Solicitar al usuario que ingrese una lista de proxies
    proxies_input = input("Ingresa una lista de proxies (formato: ip:puerto, separados por comas): ")
    proxies_list = [proxy.strip() for proxy in proxies_input.split(",")]
    return proxies_list

def hacer_solicitud(url, proxy=None):
    # Configurar el proxy si está disponible
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    try:
        respuesta = requests.get(url, headers=HEADERS, proxies=proxies, timeout=10)
        respuesta.raise_for_status()
        return respuesta
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a {url} con proxy {proxy}: {e}")
        return None

def buscar_en_google(query, num_results=50, proxies=None):
    # URL de búsqueda de Google
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    if proxies:
        proxy = proxies.pop(0)  # Tomar la primera proxy de la lista
        proxies.append(proxy)  # Moverla al final para rotar
    else:
        proxy = None

    respuesta = hacer_solicitud(url, proxy)
    if not respuesta:
        return []

    # Analizar el contenido HTML
    soup = BeautifulSoup(respuesta.text, "html.parser")

    # Extraer enlaces de los resultados
    resultados = []
    for elemento in soup.find_all("div", class_="tF2Cxc"):  # Clase común para resultados
        enlace = elemento.find("a")["href"]
        resultados.append(enlace)

    return resultados

def tiene_captcha(url, proxy=None):
    respuesta = hacer_solicitud(url, proxy)
    if not respuesta:
        return False

    soup = BeautifulSoup(respuesta.text, "html.parser")

    # Buscar elementos comunes de CAPTCHA
    if soup.find("input", {"name": re.compile(r"captcha", re.IGNORECASE)}):
        return True
    if soup.find("div", {"class": re.compile(r"captcha", re.IGNORECASE)}):
        return True
    return False

def buscar_paginas_sin_captcha(query, num_results=50, proxies=None):
    # Buscar en Google
    resultados = buscar_en_google(query, num_results, proxies)
    if not resultados:
        print("No se encontraron resultados.")
        return

    # Filtrar páginas sin CAPTCHA
    for url in resultados:
        if proxies:
            proxy = proxies.pop(0)  # Tomar la primera proxy de la lista
            proxies.append(proxy)  # Moverla al final para rotar
        else:
            proxy = None

        if not tiene_captcha(url, proxy):
            print(f"Página sin CAPTCHA encontrada: {url}")

if __name__ == "__main__":
    # Solicitar proxies al usuario
    proxies = obtener_proxies()

    # Definir la consulta de búsqueda con operadores de Google
    query = "inurl:checkout"  # Cambia "palabra1" y "palabra2" por tus términos
    buscar_paginas_sin_captcha(query, proxies=proxies)
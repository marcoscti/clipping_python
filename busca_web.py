from urllib.parse import parse_qs, quote_plus, urlparse

import requests
from bs4 import BeautifulSoup


DUCKDUCKGO_URL = "https://duckduckgo.com/html/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}


def _extrair_url_ddg(href):
    if not href:
        return None

    if href.startswith("http://") or href.startswith("https://"):
        return href

    if href.startswith("/l/"):
        query = urlparse(href).query
        return parse_qs(query).get("uddg", [None])[0]

    return None


def buscar_noticias_web(palavras_chave, limite_por_palavra=5):
    noticias = []
    links_vistos = set()

    for palavra in palavras_chave:
        consulta = f"\"{palavra}\" noticia"
        url = f"{DUCKDUCKGO_URL}?q={quote_plus(consulta)}"

        try:
            resposta = requests.get(url, headers=HEADERS, timeout=10)
            resposta.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(resposta.text, "html.parser")
        resultados = soup.select(".result")
        total = 0

        for item in resultados:
            link_tag = item.select_one("a.result__a")
            if not link_tag:
                continue

            link = _extrair_url_ddg(link_tag.get("href"))
            if not link or link in links_vistos:
                continue

            titulo = link_tag.get_text(" ", strip=True)
            snippet_tag = item.select_one(".result__snippet")
            descricao = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

            noticias.append({
                "titulo": titulo,
                "link": link,
                "descricao": descricao,
            })
            links_vistos.add(link)
            total += 1

            if total >= limite_por_palavra:
                break

    return noticias

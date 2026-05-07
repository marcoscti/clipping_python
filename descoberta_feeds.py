from urllib.parse import parse_qs, quote_plus, urljoin, urlparse

import feedparser
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
CAMINHOS_COMUNS_FEED = (
    "/feed",
    "/rss",
    "/rss.xml",
    "/feed.xml",
    "/atom.xml",
)


def _extrair_url_resultado_ddg(href):
    if not href:
        return None

    if href.startswith("http://") or href.startswith("https://"):
        return href

    if href.startswith("/l/"):
        query = urlparse(href).query
        destino = parse_qs(query).get("uddg", [None])[0]
        return destino

    return None


def _validar_feed(url):
    try:
        feed = feedparser.parse(url)
    except Exception:
        return False

    return bool(feed.entries)


def _buscar_sites_por_termo(termo, limite_sites):
    consulta = f"{termo} noticias rss"
    url = f"{DUCKDUCKGO_URL}?q={quote_plus(consulta)}"

    try:
        resposta = requests.get(url, headers=HEADERS, timeout=10)
        resposta.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(resposta.text, "html.parser")
    links = soup.select("a.result__a")
    encontrados = []
    visitados = set()

    for link in links:
        destino = _extrair_url_resultado_ddg(link.get("href"))
        if not destino or destino in visitados:
            continue

        visitados.add(destino)
        encontrados.append(destino)

        if len(encontrados) >= limite_sites:
            break

    return encontrados


def _descobrir_feed_em_site(url_site):
    try:
        resposta = requests.get(url_site, headers=HEADERS, timeout=10)
        resposta.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(resposta.text, "html.parser")

    for tag in soup.find_all("link"):
        tipo = (tag.get("type") or "").lower()
        rel = " ".join(tag.get("rel") or [])
        href = tag.get("href")

        if "alternate" in rel and ("rss" in tipo or "atom" in tipo or "xml" in tipo):
            feed_url = urljoin(url_site, href)
            if _validar_feed(feed_url):
                return feed_url

    base = f"{urlparse(url_site).scheme}://{urlparse(url_site).netloc}"

    for caminho in CAMINHOS_COMUNS_FEED:
        feed_url = urljoin(base, caminho)
        if _validar_feed(feed_url):
            return feed_url

    return None


def descobrir_feeds(palavras_chave, limite_sites_por_palavra=5):
    feeds_encontrados = []
    vistos = set()

    for palavra in palavras_chave:
        sites = _buscar_sites_por_termo(palavra, limite_sites_por_palavra)
        for site in sites:
            feed_url = _descobrir_feed_em_site(site)
            if feed_url and feed_url not in vistos:
                vistos.add(feed_url)
                feeds_encontrados.append(feed_url)

    return feeds_encontrados

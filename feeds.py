import json
import requests
import feedparser
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

from config import (
    CONFIG_PATH,
    DESCOBRIR_FEEDS_AUTOMATICAMENTE,
    FEEDS,
    LIMITE_SITES_POR_PALAVRA,
    LIMITE_RESULTADOS_WEB_POR_PALAVRA,
    PALAVRAS_CHAVE,
    USAR_GOOGLE_NEWS_RSS,
    USAR_BUSCA_WEB_DIRETA,
)
from busca_web import buscar_noticias_web
from descoberta_feeds import descobrir_feeds
from google_news import gerar_feeds_google_news


def _resolver_link(url):
    """Resolve redirecionamentos (especialmente do Google News) para obter a URL original do site."""
    if url and "news.google.com" in url:
        try:
            # stream=True evita baixar o corpo da página, pegamos apenas o cabeçalho final
            response = requests.get(url, allow_redirects=True, timeout=5, stream=True)
            return response.url
        except Exception:
            return url
    return url


def _extrair_fonte(item, url_feed):
    fonte_item = getattr(item, "source", None)
    if fonte_item and isinstance(fonte_item, dict):
        titulo = fonte_item.get("title")
        if titulo:
            return titulo

    dominio = urlparse(getattr(item, "link", "")).netloc
    if dominio:
        return dominio

    return urlparse(url_feed).netloc


def _extrair_data_publicacao(item):
    data_str = (
        getattr(item, "published", None)
        or getattr(item, "updated", None)
        or getattr(item, "pubDate", None)
    )

    if data_str:
        try:
            dt = parsedate_to_datetime(data_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            return dt.astimezone(UTC)
        except (TypeError, ValueError):
            pass

    struct_data = (
        getattr(item, "published_parsed", None)
        or getattr(item, "updated_parsed", None)
    )
    if struct_data:
        return datetime(*struct_data[:6], tzinfo=UTC)

    return None


def buscar_feeds():
    # Carrega a configuração atualizada do disco para evitar cache
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}

    # Usa os valores do arquivo ou mantém os padrões das constantes importadas
    palavras_vivas = cfg.get("palavras_chave", PALAVRAS_CHAVE)
    feeds_vivos = list(cfg.get("feeds", FEEDS))
    descobrir_auto = cfg.get("descobrir_feeds_automaticamente", DESCOBRIR_FEEDS_AUTOMATICAMENTE)
    limite_sites = cfg.get("limite_sites_por_palavra", LIMITE_SITES_POR_PALAVRA)
    usar_google = cfg.get("usar_google_news_rss", USAR_GOOGLE_NEWS_RSS)
    usar_web = cfg.get("usar_busca_web_direta", USAR_BUSCA_WEB_DIRETA)
    limite_web = cfg.get("limite_resultados_web_por_palavra", LIMITE_RESULTADOS_WEB_POR_PALAVRA)

    noticias = []
    feeds = feeds_vivos

    if descobrir_auto:
        feeds_automaticos = descobrir_feeds(
            palavras_vivas,
            limite_sites_por_palavra=limite_sites
        )
        feeds.extend(feeds_automaticos)

    if usar_google:
        feeds.extend(gerar_feeds_google_news(palavras_vivas))

    feeds_unicos = list(dict.fromkeys(feeds))

    for url in feeds_unicos:
        feed = feedparser.parse(url)

        for item in feed.entries:
            noticias.append({
                "titulo": item.title,
                "link": _resolver_link(item.link),
                "descricao": getattr(item, "summary", ""),
                "fonte": _extrair_fonte(item, url),
                "data_publicacao": _extrair_data_publicacao(item),
            })

    if usar_web:
        noticias.extend(
            buscar_noticias_web(
                palavras_vivas,
                limite_por_palavra=limite_web
            )
        )

    noticias_unicas = []
    links_vistos = set()
    for noticia in noticias:
        link = noticia.get("link")
        if not link or link in links_vistos:
            continue
        links_vistos.add(link)
        noticias_unicas.append(noticia)

    return noticias_unicas

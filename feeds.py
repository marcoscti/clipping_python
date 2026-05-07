import feedparser
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

from config import (
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
    noticias = []
    feeds = list(FEEDS)

    if DESCOBRIR_FEEDS_AUTOMATICAMENTE:
        feeds_automaticos = descobrir_feeds(
            PALAVRAS_CHAVE,
            limite_sites_por_palavra=LIMITE_SITES_POR_PALAVRA
        )
        feeds.extend(feeds_automaticos)

    if USAR_GOOGLE_NEWS_RSS:
        feeds.extend(gerar_feeds_google_news(PALAVRAS_CHAVE))

    feeds_unicos = list(dict.fromkeys(feeds))

    for url in feeds_unicos:
        feed = feedparser.parse(url)

        for item in feed.entries:
            noticias.append({
                "titulo": item.title,
                "link": item.link,
                "descricao": getattr(item, "summary", ""),
                "fonte": _extrair_fonte(item, url),
                "data_publicacao": _extrair_data_publicacao(item),
            })

    if USAR_BUSCA_WEB_DIRETA:
        noticias.extend(
            buscar_noticias_web(
                PALAVRAS_CHAVE,
                limite_por_palavra=LIMITE_RESULTADOS_WEB_POR_PALAVRA
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

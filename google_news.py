from urllib.parse import quote_plus


def gerar_feeds_google_news(palavras_chave, regiao=None, idioma="pt-BR", pais="BR"):
    feeds = []

    for palavra in palavras_chave:
        consulta = palavra
        if regiao:
            consulta = f"{palavra} {regiao}"
        consulta = quote_plus(consulta)
        feeds.append(
            "https://news.google.com/rss/search"
            f"?q={consulta}&hl={idioma}&gl={pais}&ceid={pais}:pt-419"
        )

    return feeds

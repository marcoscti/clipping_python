import unicodedata
from datetime import UTC, datetime, timedelta

from bs4 import BeautifulSoup

from config import (
    DIAS_RETROATIVOS_MINIMOS,
    INCLUIR_NOTICIAS_SEM_DATA,
    LIMITE_POR_FONTE,
    PALAVRAS_CHAVE,
)


def _normalizar_texto(texto):
    texto_limpo = BeautifulSoup(texto or "", "html.parser").get_text(" ")
    texto_sem_acento = "".join(
        ch for ch in unicodedata.normalize("NFD", texto_limpo)
        if unicodedata.category(ch) != "Mn"
    )
    return texto_sem_acento.lower()


def _gerar_variacoes(palavra):
    base = _normalizar_texto(palavra).strip()
    variacoes = {base}

    if "-" in base:
        variacoes.add(base.replace("-", " "))
        variacoes.add(base.replace("-", ""))

    if " " in base:
        variacoes.add(base.replace(" ", "-"))
        variacoes.add(base.replace(" ", ""))

    return [v for v in variacoes if v]


def filtrar_noticias(noticias):
    resultados = []
    limite_data = datetime.now(UTC) - timedelta(days=DIAS_RETROATIVOS_MINIMOS)
    contador_por_fonte = {}

    for noticia in noticias:
        data_publicacao = noticia.get("data_publicacao")
        if data_publicacao is None and not INCLUIR_NOTICIAS_SEM_DATA:
            continue

        if data_publicacao is not None:
            if data_publicacao.tzinfo is None:
                data_publicacao = data_publicacao.replace(tzinfo=UTC)
            if data_publicacao < limite_data:
                continue

        texto = _normalizar_texto(
            noticia["titulo"] +
            " " +
            noticia["descricao"]
        )

        for palavra in PALAVRAS_CHAVE:
            variacoes = _gerar_variacoes(palavra)
            if any(variacao in texto for variacao in variacoes):
                fonte = noticia.get("fonte") or "fonte_desconhecida"
                if contador_por_fonte.get(fonte, 0) >= LIMITE_POR_FONTE:
                    break

                noticia["palavra"] = palavra
                resultados.append(noticia)
                contador_por_fonte[fonte] = contador_por_fonte.get(fonte, 0) + 1
                break

    return resultados

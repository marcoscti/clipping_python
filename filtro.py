import json
import unicodedata
from datetime import UTC, datetime, timedelta

from bs4 import BeautifulSoup

from config import CONFIG_PATH


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
    # Carrega a configuração do disco para garantir que alterações na UI sejam aplicadas imediatamente
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}

    dias_retro = cfg.get("dias_retroativos_minimos", 7)
    incluir_sem_data = cfg.get("incluir_noticias_sem_data", False)
    limite_fonte = cfg.get("limite_por_fonte", 5)
    palavras_chave = cfg.get("palavras_chave", [])
    regiao = cfg.get("regiao", "").strip()

    resultados = []
    limite_data = datetime.now(UTC) - timedelta(days=dias_retro)
    contador_por_fonte = {}

    for noticia in noticias:
        data_publicacao = noticia.get("data_publicacao")
        if data_publicacao is None and not incluir_sem_data:
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

        if regiao:
            texto_regiao = texto + " " + _normalizar_texto(noticia.get("fonte", ""))
            regiao_norm = _normalizar_texto(regiao)
            if not all(
                token
                for token in regiao_norm.split()
                if token and token in texto_regiao
            ):
                continue

        for palavra in palavras_chave:
            variacoes = _gerar_variacoes(palavra)
            if any(variacao in texto for variacao in variacoes):
                fonte = noticia.get("fonte") or "fonte_desconhecida"
                if contador_por_fonte.get(fonte, 0) >= limite_fonte:
                    break

                noticia["palavra"] = palavra
                resultados.append(noticia)
                contador_por_fonte[fonte] = contador_por_fonte.get(fonte, 0) + 1
                break

    return resultados

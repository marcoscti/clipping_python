import json
from pathlib import Path
import sys


BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "feeds": [
        "https://g1.globo.com/rss/g1/",
        "https://rss.cnnbrasil.com.br/rss/tecnologia",
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
    ],
    "palavras_chave": [
        "IgesDF",
        "IGES-DF",
        "Instituto de Gestão Estratégica de Saúde do DF",
        "Instituto de Gestão Estratégica de Saúde do Distrito Federal",
    ],
    "descobrir_feeds_automaticamente": True,
    "limite_sites_por_palavra": 5,
    "usar_busca_web_direta": False,
    "limite_resultados_web_por_palavra": 5,
    "usar_google_news_rss": True,
    "limite_por_fonte": 5,
    "dias_retroativos_minimos": 7,
    "incluir_noticias_sem_data": False,
    "abrir_dialogo_salvar_relatorio": True,
    "openai_api_key": "",
    "telegram_token": "",
    "telegram_chat_id": "",
}


def _carregar_arquivo():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(
            json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return dict(DEFAULT_CONFIG)

    try:
        conteudo = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)

    config = dict(DEFAULT_CONFIG)
    config.update(conteudo)
    return config


def salvar_configuracao(dados):
    config = dict(DEFAULT_CONFIG)
    config.update(dados)
    CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


_CONFIG = _carregar_arquivo()

FEEDS = _CONFIG["feeds"]
PALAVRAS_CHAVE = _CONFIG["palavras_chave"]
DESCOBRIR_FEEDS_AUTOMATICAMENTE = _CONFIG["descobrir_feeds_automaticamente"]
LIMITE_SITES_POR_PALAVRA = _CONFIG["limite_sites_por_palavra"]
USAR_BUSCA_WEB_DIRETA = _CONFIG["usar_busca_web_direta"]
LIMITE_RESULTADOS_WEB_POR_PALAVRA = _CONFIG["limite_resultados_web_por_palavra"]
USAR_GOOGLE_NEWS_RSS = _CONFIG["usar_google_news_rss"]
LIMITE_POR_FONTE = _CONFIG["limite_por_fonte"]
DIAS_RETROATIVOS_MINIMOS = _CONFIG["dias_retroativos_minimos"]
INCLUIR_NOTICIAS_SEM_DATA = _CONFIG["incluir_noticias_sem_data"]
ABRIR_DIALOGO_SALVAR_RELATORIO = _CONFIG["abrir_dialogo_salvar_relatorio"]
OPENAI_API_KEY = _CONFIG["openai_api_key"]
TELEGRAM_TOKEN = _CONFIG["telegram_token"]
TELEGRAM_CHAT_ID = _CONFIG["telegram_chat_id"]

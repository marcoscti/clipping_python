import json
from datetime import datetime
from feeds import buscar_feeds
from filtro import filtrar_noticias
from resumo_ia import gerar_resumo
from relatorio import gerar_relatorio
from telegram_bot import enviar_telegram
from config import CONFIG_PATH


def executar_clipping(status_callback=None):
    def notificar(mensagem):
        if status_callback:
            status_callback(mensagem)
        else:
            print(mensagem)

    notificar("Iniciando clipping...")
    
    # Carrega config para log de conferência
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            palavras = cfg.get("palavras_chave", [])
            notificar(f"Palavras-chave atuais: {', '.join(palavras[:3])}...")
    except: pass

    noticias = buscar_feeds()
    notificar(f"Total de notícias coletadas: {len(noticias)}")
    
    filtradas = filtrar_noticias(noticias)
    notificar(f"{len(filtradas)} notícias filtradas com sucesso.")

    lista_para_relatorio = []

    for noticia in filtradas:
        resumo = gerar_resumo(
            noticia["titulo"] +
            "\n" +
            noticia["descricao"]
        )

        # Acumula os dados para o Excel, já que não usamos mais SQLite
        dados_noticia = noticia.copy()
        dados_noticia["resumo"] = resumo
        dados_noticia["data_insercao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_para_relatorio.append(dados_noticia)

        mensagem = f"""
📰 {noticia['titulo']}

🔎 Palavra-chave:
{noticia['palavra']}

📌 Resumo:
{resumo}

🔗 {noticia['link']}
"""

        enviar_telegram(mensagem)

    if lista_para_relatorio:
        notificar("Gerando relatório Excel...")
        gerar_relatorio(lista_para_relatorio)
    else:
        notificar("Aviso: Nenhuma notícia condizente com os filtros foi encontrada.")
    notificar("Processo finalizado")


if __name__ == "__main__":
    executar_clipping()

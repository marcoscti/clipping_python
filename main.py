from feeds import buscar_feeds
from filtro import filtrar_noticias
from resumo_ia import gerar_resumo
from database import salvar_noticia
from relatorio import gerar_relatorio
from telegram_bot import enviar_telegram


def executar_clipping(status_callback=None):
    def notificar(mensagem):
        if status_callback:
            status_callback(mensagem)
        else:
            print(mensagem)

    notificar("Iniciando clipping...")
    noticias = buscar_feeds()
    filtradas = filtrar_noticias(noticias)
    notificar(f"{len(filtradas)} notícias encontradas")

    for noticia in filtradas:
        resumo = gerar_resumo(
            noticia["titulo"] +
            "\n" +
            noticia["descricao"]
        )

        salvar_noticia(
            noticia["titulo"],
            noticia["link"],
            resumo,
            noticia["palavra"],
            noticia.get("fonte"),
            noticia.get("data_publicacao"),
        )

        mensagem = f"""
📰 {noticia['titulo']}

🔎 Palavra-chave:
{noticia['palavra']}

📌 Resumo:
{resumo}

🔗 {noticia['link']}
"""

        enviar_telegram(mensagem)

    notificar("Gerando relatório...")
    gerar_relatorio()
    notificar("Processo finalizado")


if __name__ == "__main__":
    executar_clipping()

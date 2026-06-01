import json
import pandas as pd
from datetime import datetime
from tkinter import Tk, filedialog
from config import CONFIG_PATH

from app_icon import carregar_icone

def gerar_relatorio(noticias_brutas):
    """
    Recebe uma lista de notícias e gera uma planilha Excel (.xlsx).
    """
    if not noticias_brutas:
        print("Nenhuma notícia para exportar.")
        return

    noticias_processadas = []

    for item in noticias_brutas:
        # Extração segura de dados independente do formato
        titulo = item.get("titulo")
        link = item.get("link")
        resumo = item.get("resumo")
        palavra = item.get("palavra")
        fonte = item.get("fonte")
        data_pub = item.get("data_publicacao")
        data_ins = item.get("data_insercao", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Formatação de data de publicação
        data_pub_fmt = "-"
        if data_pub:
            try:
                if hasattr(data_pub, "strftime"):
                    data_pub_fmt = data_pub.strftime("%d/%m/%Y %H:%M")
                else:
                    data_pub_fmt = datetime.fromisoformat(str(data_pub).replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")
            except Exception:
                data_pub_fmt = str(data_pub)

        # Formata o link como uma fórmula de hiperlink do Excel para ser clicável
        link_excel = link
        if link and str(link).startswith("http"):
            # Escapa aspas duplas caso existam na URL para não quebrar a fórmula
            url_limpa = str(link).replace('"', '""')
            link_excel = f'=HYPERLINK("{url_limpa}", "{link}")'

        noticias_processadas.append({
            "Título": titulo,
            "Link": link_excel,
            "Resumo": resumo,
            "Palavra-Chave": palavra,
            "Fonte": fonte or "Não informada",
            "Data Publicação": data_pub_fmt,
            "Data Coleta": data_ins
        })

    df = pd.DataFrame(noticias_processadas)
    
    # Carrega a configuração atual para verificar se a IA está ativa
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            ia_ativa = bool(cfg.get("openai_api_key"))
    except Exception:
        ia_ativa = False

    # Remove a coluna de Resumo se a IA não estiver configurada
    if not ia_ativa and "Resumo" in df.columns:
        df = df.drop(columns=["Resumo"])

    # Nome conforme solicitado: dia-mes-ano-relatorio.xlsx
    nome_sugerido = datetime.now().strftime("%d-%m-%Y-relatorio.xlsx")

    try:
        root = Tk()
        carregar_icone(root)
        root.withdraw()
        root.attributes("-topmost", True) # Garante que a janela apareça na frente
        destino = filedialog.asksaveasfilename(
            title="Salvar relatório Excel",
            defaultextension=".xlsx",
            initialfile=nome_sugerido,
            filetypes=[("Planilha Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
        )
        root.destroy()

        if destino:
            df.to_excel(destino, index=False)
            print(f"Relatório salvo com sucesso em: {destino}")
    except Exception as e:
        print(f"Erro ao salvar arquivo Excel: {e}")
from jinja2 import Environment, FileSystemLoader
from database import listar_noticias
from pathlib import Path
from datetime import datetime
from shutil import copyfile
import sys
from tkinter import Tk, filedialog

from config import ABRIR_DIALOGO_SALVAR_RELATORIO

APP_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))

TEMPLATES_DIR = BUNDLE_DIR / "templates"
OUTPUT_DIR = APP_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


def gerar_relatorio():

    noticias_brutas = listar_noticias()
    noticias = []

    for titulo, link, resumo, palavra, fonte, data_publicacao, data_insercao in noticias_brutas:
        data_publicacao_formatada = "-"
        if data_publicacao:
            try:
                data_publicacao_formatada = datetime.fromisoformat(
                    data_publicacao.replace("Z", "+00:00")
                ).strftime("%d/%m/%Y %H:%M")
            except ValueError:
                data_publicacao_formatada = data_publicacao

        data_insercao_formatada = data_insercao
        if data_insercao:
            try:
                data_insercao_formatada = datetime.strptime(
                    data_insercao,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d/%m/%Y %H:%M")
            except ValueError:
                pass

        noticias.append({
            "titulo": titulo,
            "link": link,
            "resumo": resumo,
            "palavra": palavra,
            "fonte": fonte or "Fonte não informada",
            "data_publicacao": data_publicacao_formatada,
            "data_insercao": data_insercao_formatada or "-",
        })

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR)
    )

    template = env.get_template("relatorio.html")

    html = template.render(
        noticias=noticias
    )

    output_file = OUTPUT_DIR / "relatorio_final.html"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(html)

    print(f"Relatório gerado: {output_file}")

    if ABRIR_DIALOGO_SALVAR_RELATORIO:
        try:
            root = Tk()
            root.withdraw()
            destino = filedialog.asksaveasfilename(
                title="Salvar relatório HTML",
                defaultextension=".html",
                initialfile="relatorio_final.html",
                filetypes=[("Arquivo HTML", "*.html"), ("Todos os arquivos", "*.*")],
            )
            root.destroy()
            if destino:
                copyfile(output_file, destino)
                print(f"Relatório salvo também em: {destino}")
        except Exception:
            print("Não foi possível abrir o diálogo de salvar relatório.")
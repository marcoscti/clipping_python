import json
import tkinter as tk
from tkinter import messagebox

from config import CONFIG_PATH, DEFAULT_CONFIG, salvar_configuracao


def carregar_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)


def adicionar_item(listbox, entrada, nome_campo):
    valor = entrada.get().strip()
    if not valor:
        messagebox.showwarning("Campo vazio", f"Informe um valor para {nome_campo}.")
        return

    itens_atuais = listbox.get(0, tk.END)
    if valor in itens_atuais:
        messagebox.showwarning("Duplicado", f"Esse valor já existe em {nome_campo}.")
        return

    listbox.insert(tk.END, valor)
    entrada.delete(0, tk.END)


def remover_item(listbox, nome_campo):
    selecionados = listbox.curselection()
    if not selecionados:
        messagebox.showwarning(
            "Nenhum item selecionado",
            f"Selecione um item de {nome_campo} para remover.",
        )
        return

    for indice in reversed(selecionados):
        listbox.delete(indice)


def obter_itens_listbox(listbox):
    return [item.strip() for item in listbox.get(0, tk.END) if item.strip()]


def criar_interface(parent=None):
    config = carregar_config()
    if parent is None:
        root = tk.Tk()
    else:
        root = tk.Toplevel(parent)
        root.transient(parent)
        root.grab_set()
    root.title("Configuração do Clipping")
    root.geometry("820x730")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    listas_frame = tk.Frame(frame)
    listas_frame.pack(fill="both", expand=True, pady=(0, 12))

    palavras_frame = tk.LabelFrame(listas_frame, text="Palavras-chave")
    palavras_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))

    palavras_lista = tk.Listbox(
        palavras_frame, selectmode=tk.EXTENDED, height=12, exportselection=False
    )
    palavras_lista.pack(fill="both", expand=True, padx=8, pady=(8, 8))
    for palavra in config.get("palavras_chave", []):
        palavras_lista.insert(tk.END, palavra)

    palavras_controles = tk.Frame(palavras_frame)
    palavras_controles.pack(fill="x", padx=8, pady=(0, 8))

    palavras_entry = tk.Entry(palavras_controles)
    palavras_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    tk.Button(
        palavras_controles,
        text="Adicionar",
        command=lambda: adicionar_item(
            palavras_lista, palavras_entry, "palavras-chave"
        ),
    ).pack(side="left", padx=(0, 6))
    tk.Button(
        palavras_controles,
        text="Remover selecionadas",
        command=lambda: remover_item(palavras_lista, "palavras-chave"),
    ).pack(side="left")

    feeds_frame = tk.LabelFrame(listas_frame, text="Feeds")
    feeds_frame.pack(side="left", fill="both", expand=True, padx=(6, 0))

    feeds_lista = tk.Listbox(
        feeds_frame, selectmode=tk.EXTENDED, height=12, exportselection=False
    )
    feeds_lista.pack(fill="both", expand=True, padx=8, pady=(8, 8))
    for feed in config.get("feeds", []):
        feeds_lista.insert(tk.END, feed)

    feeds_controles = tk.Frame(feeds_frame)
    feeds_controles.pack(fill="x", padx=8, pady=(0, 8))

    feeds_entry = tk.Entry(feeds_controles)
    feeds_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    tk.Button(
        feeds_controles,
        text="Adicionar",
        command=lambda: adicionar_item(feeds_lista, feeds_entry, "feeds"),
    ).pack(side="left", padx=(0, 6))
    tk.Button(
        feeds_controles,
        text="Remover selecionados",
        command=lambda: remover_item(feeds_lista, "feeds"),
    ).pack(side="left")

    campos_numericos = {}
    for campo, label in [
        ("limite_por_fonte", "Limite por fonte"),
        ("dias_retroativos_minimos", "Dias retroativos mínimos"),
        ("limite_sites_por_palavra", "Limite de sites por palavra"),
    ]:
        tk.Label(frame, text=f"{label}:").pack(anchor="w")
        entrada = tk.Entry(frame)
        entrada.pack(fill="x", pady=(0, 10))
        entrada.insert(0, str(config.get(campo, DEFAULT_CONFIG[campo])))
        campos_numericos[campo] = entrada

    vars_bool = {}
    for campo, label in [
        ("descobrir_feeds_automaticamente", "Descobrir feeds automaticamente"),
        ("usar_google_news_rss", "Usar Google News RSS"),
        ("incluir_noticias_sem_data", "Incluir notícias sem data"),
        ("abrir_dialogo_salvar_relatorio", "Abrir diálogo para salvar relatório"),
    ]:
        var = tk.BooleanVar(value=bool(config.get(campo, DEFAULT_CONFIG[campo])))
        tk.Checkbutton(frame, text=label, variable=var).pack(anchor="w")
        vars_bool[campo] = var

    def salvar():
        try:
            dados = {
                "palavras_chave": obter_itens_listbox(palavras_lista),
                "feeds": obter_itens_listbox(feeds_lista),
                "limite_por_fonte": int(campos_numericos["limite_por_fonte"].get()),
                "dias_retroativos_minimos": int(
                    campos_numericos["dias_retroativos_minimos"].get()
                ),
                "limite_sites_por_palavra": int(
                    campos_numericos["limite_sites_por_palavra"].get()
                ),
                "descobrir_feeds_automaticamente": vars_bool[
                    "descobrir_feeds_automaticamente"
                ].get(),
                "usar_google_news_rss": vars_bool["usar_google_news_rss"].get(),
                "incluir_noticias_sem_data": vars_bool["incluir_noticias_sem_data"].get(),
                "abrir_dialogo_salvar_relatorio": vars_bool[
                    "abrir_dialogo_salvar_relatorio"
                ].get(),
                "usar_busca_web_direta": bool(
                    config.get("usar_busca_web_direta", DEFAULT_CONFIG["usar_busca_web_direta"])
                ),
                "limite_resultados_web_por_palavra": int(
                    config.get(
                        "limite_resultados_web_por_palavra",
                        DEFAULT_CONFIG["limite_resultados_web_por_palavra"],
                    )
                ),
                "openai_api_key": "",
                "telegram_token": "",
                "telegram_chat_id": "",
            }
        except ValueError:
            messagebox.showerror("Erro", "Campos numéricos devem ser números inteiros.")
            return

        salvar_configuracao(dados)
        messagebox.showinfo("Sucesso", f"Configuração salva em:\n{CONFIG_PATH}")
        root.destroy()

    tk.Button(frame, text="Salvar Configuração", command=salvar).pack(
        pady=16, anchor="e"
    )
    if parent is None:
        root.mainloop()
    else:
        parent.wait_window(root)


if __name__ == "__main__":
    criar_interface()

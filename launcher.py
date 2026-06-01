import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from queue import Empty, Queue
from threading import Thread

from app_icon import carregar_icone
from interface_config import criar_interface
from main import executar_clipping


def iniciar_app():
    root = tk.Tk()
    root.title("Clipping")
    carregar_icone(root)
    root.geometry("520x320")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Escolha uma opção",
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="center", pady=(0, 14))

    fila_status = Queue()

    def abrir_configuracao():
        criar_interface(parent=root)

    def atualizar_status(texto):
        status_label.config(text=texto)
        status_log.insert(tk.END, texto)
        status_log.see(tk.END)
        root.update_idletasks()

    def processar_fila():
        try:
            while True:
                tipo, conteudo = fila_status.get_nowait()
                if tipo == "status":
                    atualizar_status(conteudo)
                elif tipo == "erro":
                    barra_progresso.stop()
                    barra_progresso.pack_forget()
                    atualizar_status("Erro durante a execução.")
                    messagebox.showerror("Erro", f"Falha ao executar clipping:\n{conteudo}")
                    btn_configurar.config(state=tk.NORMAL)
                    btn_executar.config(state=tk.NORMAL)
                elif tipo == "fim":
                    barra_progresso.stop()
                    barra_progresso.pack_forget()
                    atualizar_status("Execução concluída.")
                    btn_configurar.config(state=tk.NORMAL)
                    btn_executar.config(state=tk.NORMAL)
        except Empty:
            pass
        finally:
            root.after(150, processar_fila)

    def executar_em_thread():
        try:
            executar_clipping(status_callback=lambda msg: fila_status.put(("status", msg)))
            fila_status.put(("fim", None))
        except Exception as erro:
            fila_status.put(("erro", str(erro)))

    def executar():
        btn_configurar.config(state=tk.DISABLED)
        btn_executar.config(state=tk.DISABLED)
        barra_progresso.pack(fill="x", pady=(0, 6))
        barra_progresso.start(12)
        atualizar_status("Executando clipping...")
        Thread(target=executar_em_thread, daemon=True).start()

    botoes = tk.Frame(frame)
    botoes.pack(fill="x", pady=(0, 6))

    btn_configurar = tk.Button(
        botoes,
        text="Configurar",
        height=2,
        command=abrir_configuracao,
    )
    btn_configurar.pack(side="left", fill="x", expand=True, padx=(0, 6))

    btn_executar = tk.Button(
        botoes,
        text="Executar clipping",
        height=2,
        command=executar,
    )
    btn_executar.pack(side="left", fill="x", expand=True, padx=(6, 0))

    status_label = tk.Label(
        frame,
        text="Pronto para iniciar.",
        anchor="w",
        justify="left",
    )
    status_label.pack(fill="x", pady=(10, 6))

    barra_progresso = ttk.Progressbar(frame, mode="indeterminate")
    barra_progresso.pack(fill="x", pady=(0, 6))
    barra_progresso.stop()
    barra_progresso.pack_forget()

    status_log = tk.Listbox(frame, height=7)
    status_log.pack(fill="both", expand=True, pady=(0, 10))

    processar_fila()
    root.mainloop()


if __name__ == "__main__":
    iniciar_app()

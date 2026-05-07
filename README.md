# Clipping Pessoal em Python

## Instalação

### Criar ambiente virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar

```bash
python main.py
```

## Configuração simplificada

As configurações agora ficam em `config.json`.

- Palavras-chave
- Feeds fixos
- Limites de coleta
- Chaves de integração (OpenAI/Telegram)

Você pode editar o arquivo manualmente ou abrir a interface gráfica:

```bash
python interface_config.py
```

## Relatório com opção "Salvar Como"

Ao final da execução, o sistema gera `output/relatorio_final.html` e abre um diálogo para você escolher outro local para salvar uma cópia do HTML.

Se quiser desativar essa janela, no `config.json` defina:

```json
"abrir_dialogo_salvar_relatorio": false
```

## Gerar executável (.exe)

Você pode distribuir para outras máquinas usando PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --name clipping_app main.py
```

O executável será gerado em `dist/clipping_app.exe`.

Para uso com interface de configuração, mantenha `config.json` no mesmo diretório do executável.

## Execução por duplo clique (.bat)

Foram adicionados scripts para facilitar uso pela equipe:

- `build_exe.bat`: instala dependências e gera o executável em `dist/`.
- `run_clipping.bat`: executa `dist/clipping_app.exe` se existir, senão roda `main.py`.
- `configurar_clipping.bat`: abre a interface gráfica de configuração.

@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo [ERRO] Ambiente virtual nao encontrado em venv\Scripts\python.exe
  pause
  exit /b 1
)

call "venv\Scripts\python.exe" interface_config.py
if errorlevel 1 (
  echo.
  echo [ERRO] Falha ao abrir interface de configuracao.
  pause
  exit /b 1
)

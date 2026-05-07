@echo off
setlocal
cd /d "%~dp0"

if exist "dist\clipping_app.exe" (
  echo Executando versao compilada...
  start "" "dist\clipping_app.exe"
  exit /b 0
)

if not exist "venv\Scripts\python.exe" (
  echo [ERRO] Nao encontrei venv\Scripts\python.exe nem dist\clipping_app.exe
  pause
  exit /b 1
)

echo Executando via Python...
call "venv\Scripts\python.exe" main.py
if errorlevel 1 (
  echo.
  echo [ERRO] A execucao retornou erro.
)
pause

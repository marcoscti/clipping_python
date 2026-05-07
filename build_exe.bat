@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo [ERRO] Ambiente virtual nao encontrado em venv\Scripts\python.exe
  echo Crie com: python -m venv venv
  pause
  exit /b 1
)

echo [1/3] Instalando dependencias...
call "venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :erro

echo [2/3] Instalando PyInstaller...
call "venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 goto :erro

if not exist "assets" mkdir "assets"

if not exist "assets\configurador.ico" (
  echo [ERRO] Icone do configurador nao encontrado: assets\configurador.ico
  exit /b 1
)

echo [3/4] Gerando executavel do clipping...
call "venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --icon "assets\configurador.ico" --name clipping_app --add-data "templates;templates" launcher.py
if errorlevel 1 goto :erro

echo [4/4] Gerando executavel do configurador...
call "venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --icon "assets\configurador.ico" --name configurador interface_config.py
if errorlevel 1 goto :erro

if not exist "dist\clipping_app.exe" (
  echo [ERRO] Nao foi possivel localizar dist\clipping_app.exe
  exit /b 1
)

if not exist "dist\configurador.exe" (
  echo [ERRO] Nao foi possivel localizar dist\configurador.exe
  exit /b 1
)

copy /Y "config.json" "dist\config.json" >nul
echo.
echo Build concluido com sucesso.
echo Executavel do clipping: dist\clipping_app.exe
echo Executavel do configurador: dist\configurador.exe
echo Config copiado para: dist\config.json

exit /b 0

:erro
echo.
echo [ERRO] Falha durante o processo de build.
exit /b 1

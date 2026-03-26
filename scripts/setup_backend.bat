@echo off
setlocal

echo ========================================
echo DICOM Gateway - Backend Setup
echo ========================================
echo.

cd /d C:\dicom_gateway\backend

if not exist ".venv" (
  echo Criando ambiente virtual...
  cmd /c python -m venv .venv
) else (
  echo Ambiente virtual ja existe.
)

if not exist ".venv\Scripts\python.exe" (
  echo Falha ao localizar o Python do ambiente virtual.
  exit /b 1
)

echo.
echo Atualizando pip...
cmd /c ".venv\Scripts\python.exe -m pip install --upgrade pip"
if errorlevel 1 exit /b 1

echo.
if not exist "requirements.txt" (
  echo Arquivo requirements.txt nao encontrado em C:\dicom_gateway\backend
  exit /b 1
)

echo Instalando dependencias travadas do requirements.txt...
cmd /c ".venv\Scripts\python.exe -m pip install -r requirements.txt"
if errorlevel 1 exit /b 1

echo.
echo Setup concluido.
echo Ambiente virtual: C:\dicom_gateway\backend\.venv
echo Requirements: C:\dicom_gateway\backend\requirements.txt

endlocal

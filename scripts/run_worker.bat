@echo off
setlocal

cd /d C:\dicom_gateway\backend

if not exist ".venv\Scripts\python.exe" (
  echo Ambiente virtual nao encontrado em C:\dicom_gateway\backend\.venv
  exit /b 1
)

if not exist ".env" (
  echo Arquivo .env nao encontrado em C:\dicom_gateway\backend
  echo Copie .env.example para .env e ajuste as configuracoes.
  exit /b 1
)

echo Iniciando Sender Worker...
cmd /c ".venv\Scripts\python.exe -m app.run_worker"

endlocal

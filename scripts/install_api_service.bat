@echo off
setlocal

set SERVICE_NAME=DICOMGatewayAPI
set NSSM_EXE=C:\tools\nssm\win64\nssm.exe
set PYTHON_EXE=C:\dicom_gateway\backend\.venv\Scripts\python.exe
set APP_DIR=C:\dicom_gateway\backend
set LOG_DIR=C:\dicom_gateway\logs

if not exist "%PYTHON_EXE%" (
  echo Python do ambiente virtual nao encontrado: %PYTHON_EXE%
  exit /b 1
)

if not exist "%NSSM_EXE%" (
  where nssm >nul 2>&1
  if errorlevel 1 (
    echo NSSM nao encontrado no PATH.
    exit /b 1
  )
  set NSSM_EXE=nssm
)

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

%NSSM_EXE% install %SERVICE_NAME% "%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
%NSSM_EXE% set %SERVICE_NAME% AppDirectory "%APP_DIR%"
%NSSM_EXE% set %SERVICE_NAME% AppStdout "%LOG_DIR%\api-service.out.log"
%NSSM_EXE% set %SERVICE_NAME% AppStderr "%LOG_DIR%\api-service.err.log"
%NSSM_EXE% set %SERVICE_NAME% Start SERVICE_AUTO_START

echo Servico %SERVICE_NAME% instalado.
endlocal

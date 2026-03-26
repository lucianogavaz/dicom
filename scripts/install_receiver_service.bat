@echo off
setlocal

set SERVICE_NAME=DICOMGatewayReceiver
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

%NSSM_EXE% install %SERVICE_NAME% "%PYTHON_EXE%" -m app.run_receiver
%NSSM_EXE% set %SERVICE_NAME% AppDirectory "%APP_DIR%"
%NSSM_EXE% set %SERVICE_NAME% AppStdout "%LOG_DIR%\receiver-service.out.log"
%NSSM_EXE% set %SERVICE_NAME% AppStderr "%LOG_DIR%\receiver-service.err.log"
%NSSM_EXE% set %SERVICE_NAME% Start SERVICE_AUTO_START

echo Servico %SERVICE_NAME% instalado.
endlocal

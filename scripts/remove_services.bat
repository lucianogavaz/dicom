@echo off
setlocal

set NSSM_EXE=C:\tools\nssm\win64\nssm.exe

if not exist "%NSSM_EXE%" (
  where nssm >nul 2>&1
  if errorlevel 1 (
    echo NSSM nao encontrado no PATH.
    exit /b 1
  )
  set NSSM_EXE=nssm
)

%NSSM_EXE% remove DICOMGatewayAPI confirm
%NSSM_EXE% remove DICOMGatewayReceiver confirm
%NSSM_EXE% remove DICOMGatewayWorker confirm

endlocal

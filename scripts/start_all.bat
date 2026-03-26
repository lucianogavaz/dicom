@echo off
setlocal

echo Iniciando API, Receiver e Worker em janelas separadas...

start "DICOM Gateway API" cmd /k "cd /d C:\dicom_gateway && scripts\run_api.bat"
start "DICOM Gateway Receiver" cmd /k "cd /d C:\dicom_gateway && scripts\run_receiver.bat"
start "DICOM Gateway Worker" cmd /k "cd /d C:\dicom_gateway && scripts\run_worker.bat"

endlocal

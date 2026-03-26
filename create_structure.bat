@echo off
setlocal

echo ========================================
echo DICOM Gateway - Create Folder Structure
echo ========================================
echo.

if not exist "backend" mkdir "backend"
if not exist "frontend" mkdir "frontend"
if not exist "storage" mkdir "storage"
if not exist "storage\incoming" mkdir "storage\incoming"
if not exist "storage\sent" mkdir "storage\sent"
if not exist "storage\failed" mkdir "storage\failed"
if not exist "logs" mkdir "logs"
if not exist "scripts" mkdir "scripts"
if not exist "docs" mkdir "docs"

echo Estrutura criada ou ja existente.
echo.
echo Pastas atuais:
dir /ad /b
echo.
echo Finished.

endlocal

@echo off
setlocal

set PSQL_EXE=C:\Program Files\PostgreSQL\16\bin\psql.exe

echo ========================================
echo DICOM Gateway - Create PostgreSQL Database
echo ========================================
echo.

if exist "%PSQL_EXE%" (
  set PSQL_CMD="%PSQL_EXE%"
) else (
  where psql >nul 2>&1
  if errorlevel 1 (
    echo psql nao encontrado no PATH.
    exit /b 1
  )
  set PSQL_CMD=psql
)

echo Este script cria o banco dicom_gateway no PostgreSQL local.
echo Ajuste usuario, host ou porta no comando abaixo se necessario.
echo.

cmd /c %PSQL_CMD% -U postgres -h localhost -p 5432 -f C:\dicom_gateway\scripts\create_postgres_db.sql

endlocal

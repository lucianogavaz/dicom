@echo off
setlocal

set GIT_EXE=C:\Program Files\Git\cmd\git.exe
set PSQL_EXE=C:\Program Files\PostgreSQL\16\bin\psql.exe
set NSSM_EXE=C:\tools\nssm\win64\nssm.exe

echo ========================================
echo DICOM Gateway - Environment Check
echo ========================================
echo.

where py >nul 2>&1 && (echo [OK] Python launcher encontrado) || (echo [MISSING] Python launcher nao encontrado)
where python >nul 2>&1 && (echo [OK] Python encontrado) || (echo [MISSING] Python nao encontrado)
where pip >nul 2>&1 && (echo [OK] Pip encontrado) || (echo [MISSING] Pip nao encontrado)
where node >nul 2>&1 && (echo [OK] Node.js encontrado) || (echo [MISSING] Node.js nao encontrado)
where npm.cmd >nul 2>&1 && (echo [OK] NPM encontrado) || (echo [MISSING] NPM nao encontrado)
if exist "%GIT_EXE%" (echo [OK] Git encontrado) else (where git >nul 2>&1 && (echo [OK] Git encontrado) || (echo [MISSING] Git nao encontrado))
if exist "%PSQL_EXE%" (echo [OK] PostgreSQL CLI encontrado) else (where psql >nul 2>&1 && (echo [OK] PostgreSQL CLI encontrado) || (echo [MISSING] PostgreSQL CLI nao encontrado))
if exist "%NSSM_EXE%" (echo [OK] NSSM encontrado) else (where nssm >nul 2>&1 && (echo [OK] NSSM encontrado) || (echo [MISSING] NSSM nao encontrado))

echo.
echo ========================================
echo Version Check
echo ========================================
echo.

echo [py --version]
cmd /c py --version 2>nul || echo   nao disponivel
echo.

echo [python --version]
cmd /c python --version 2>nul || echo   nao disponivel
echo.

echo [pip --version]
cmd /c pip --version 2>nul || echo   nao disponivel
echo.

echo [node --version]
cmd /c node --version 2>nul || echo   nao disponivel
echo.

echo [npm.cmd --version]
cmd /c npm.cmd --version 2>nul || echo   nao disponivel
echo.

echo [git --version]
if exist "%GIT_EXE%" (
  cmd /c ""%GIT_EXE%" --version" 2>nul || echo   nao disponivel
) else (
  cmd /c git --version 2>nul || echo   nao disponivel
)
echo.

echo [psql --version]
if exist "%PSQL_EXE%" (
  cmd /c ""%PSQL_EXE%" --version" 2>nul || echo   nao disponivel
) else (
  cmd /c psql --version 2>nul || echo   nao disponivel
)
echo.

echo [nssm version]
if exist "%NSSM_EXE%" (
  cmd /c ""%NSSM_EXE%" version" 2>nul || echo   nao disponivel
) else (
  cmd /c nssm version 2>nul || echo   nao disponivel
)
echo.

echo ========================================
echo Folder Check
echo ========================================
echo.

if exist "backend" (echo [OK] pasta "backend" existe) else (echo [MISSING] pasta "backend" nao existe)
if exist "frontend" (echo [OK] pasta "frontend" existe) else (echo [MISSING] pasta "frontend" nao existe)
if exist "storage" (echo [OK] pasta "storage" existe) else (echo [MISSING] pasta "storage" nao existe)
if exist "storage\incoming" (echo [OK] pasta "storage\incoming" existe) else (echo [MISSING] pasta "storage\incoming" nao existe)
if exist "storage\sent" (echo [OK] pasta "storage\sent" existe) else (echo [MISSING] pasta "storage\sent" nao existe)
if exist "storage\failed" (echo [OK] pasta "storage\failed" existe) else (echo [MISSING] pasta "storage\failed" nao existe)
if exist "logs" (echo [OK] pasta "logs" existe) else (echo [MISSING] pasta "logs" nao existe)
if exist "scripts" (echo [OK] pasta "scripts" existe) else (echo [MISSING] pasta "scripts" nao existe)
if exist "docs" (echo [OK] pasta "docs" existe) else (echo [MISSING] pasta "docs" nao existe)

echo.
echo Finished.
endlocal

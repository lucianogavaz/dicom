@echo off
setlocal

set GIT_EXE=C:\Program Files\Git\cmd\git.exe
set PSQL_EXE=C:\Program Files\PostgreSQL\16\bin\psql.exe
set NSSM_EXE=C:\tools\nssm\win64\nssm.exe
set VENV_PYTHON=C:\dicom_gateway\backend\.venv\Scripts\python.exe

echo ========================================
echo DICOM Gateway - Setup Validation
echo ========================================
echo.

echo [python --version]
if exist "%VENV_PYTHON%" (
  cmd /c ""%VENV_PYTHON%" --version" 2>nul || echo   nao disponivel
) else (
  cmd /c python --version 2>nul || echo   nao disponivel
)
echo.

echo [pip --version]
if exist "%VENV_PYTHON%" (
  cmd /c ""%VENV_PYTHON%" -m pip --version" 2>nul || echo   nao disponivel
) else (
  cmd /c pip --version 2>nul || echo   nao disponivel
)
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

echo [node --version]
cmd /c node --version 2>nul || echo   nao disponivel
echo.

echo [npm.cmd --version]
cmd /c npm.cmd --version 2>nul || echo   nao disponivel
echo.

echo ========================================
echo Python Package Check
echo ========================================
echo.

echo [fastapi]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import fastapi; print(fastapi.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import fastapi; print(fastapi.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [uvicorn]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import uvicorn; print(uvicorn.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import uvicorn; print(uvicorn.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [pydicom]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import pydicom; print(pydicom.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import pydicom; print(pydicom.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [pynetdicom]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import pynetdicom; print(pynetdicom.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import pynetdicom; print(pynetdicom.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [sqlalchemy]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import sqlalchemy; print(sqlalchemy.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import sqlalchemy; print(sqlalchemy.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [psycopg]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import psycopg; print(psycopg.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import psycopg; print(psycopg.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [alembic]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import alembic; print(alembic.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import alembic; print(alembic.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo [dotenv]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import dotenv; print(getattr(dotenv, '__version__', 'installed'))" 2>nul || echo   nao disponivel
) else (
  python -c "import dotenv; print(getattr(dotenv, '__version__', 'installed'))" 2>nul || echo   nao disponivel
)
echo.

echo [pydantic-settings]
if exist "%VENV_PYTHON%" (
  "%VENV_PYTHON%" -c "import pydantic_settings; print(pydantic_settings.__version__)" 2>nul || echo   nao disponivel
) else (
  python -c "import pydantic_settings; print(pydantic_settings.__version__)" 2>nul || echo   nao disponivel
)
echo.

echo Finished.
endlocal

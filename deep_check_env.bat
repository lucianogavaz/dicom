@echo off
setlocal

echo ========================================
echo DICOM Gateway - Deep Environment Check
echo ========================================
echo.

echo [PATH tools]
where python 2>nul
where py 2>nul
where pip 2>nul
where git 2>nul
where psql 2>nul
where nssm 2>nul
echo.

echo [Common installation folders]
if exist "C:\Program Files\Python*" dir /b "C:\Program Files" | findstr /i "Python"
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python" dir /b "C:\Users\%USERNAME%\AppData\Local\Programs\Python"
if exist "C:\Program Files\Git" echo C:\Program Files\Git
if exist "C:\Program Files\PostgreSQL" dir /b "C:\Program Files\PostgreSQL"
if exist "C:\tools" dir /b "C:\tools" | findstr /i "nssm"
echo.

echo [Executable search]
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" echo FOUND: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
if exist "C:\Program Files\Python312\python.exe" echo FOUND: C:\Program Files\Python312\python.exe
if exist "C:\Program Files\Git\cmd\git.exe" echo FOUND: C:\Program Files\Git\cmd\git.exe
if exist "C:\Program Files\PostgreSQL\16\bin\psql.exe" echo FOUND: C:\Program Files\PostgreSQL\16\bin\psql.exe
if exist "C:\Program Files\PostgreSQL\17\bin\psql.exe" echo FOUND: C:\Program Files\PostgreSQL\17\bin\psql.exe
if exist "C:\tools\nssm\nssm.exe" echo FOUND: C:\tools\nssm\nssm.exe
if exist "C:\tools\nssm\win64\nssm.exe" echo FOUND: C:\tools\nssm\win64\nssm.exe
echo.

echo [Port check]
netstat -ano | findstr ":5432"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":11112"
echo.

echo Finished.
endlocal

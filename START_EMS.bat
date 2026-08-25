@echo off
title Smart Employee Management System (Smart EMS)
color 0A
echo =======================================================================
echo     SMART EMPLOYEE MANAGEMENT SYSTEM (Smart EMS)
echo     Enterprise Workforce, HR, Operations and Analytics Platform
echo =======================================================================
echo.

cd /d "%~dp0"

:: Find python executable
set "PY_BIN="
where python >nul 2>&1 && set "PY_BIN=python"
if "%PY_BIN%"=="" (
    where py >nul 2>&1 && set "PY_BIN=py -3"
)
if "%PY_BIN%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY_BIN=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)

:: Check if port 8000 is already listening
netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Smart EMS Django Server is already active and running on port 8000.
) else (
    echo [STARTING] Launching Smart EMS Django Server on http://127.0.0.1:8000/ ...
    start "Smart EMS Django Server" %PY_BIN% manage.py runserver 127.0.0.1:8000
    timeout /t 3 /nobreak >nul
)

echo [LAUNCHING] Opening Smart EMS in your default web browser...
start "" "http://127.0.0.1:8000/"

echo.
echo =======================================================================
echo  Web URL   : http://127.0.0.1:8000/
echo.
echo  --- DEMO USER CREDENTIALS ---
echo  Administrator : aarav.sharma  / Admin@12345 (or: admin / Admin@12345)
echo  HR Manager    : priya.patel   / Admin@12345 (or: hrmanager / Admin@12345)
echo  Team Manager  : rajesh.kumar  / Admin@12345 (or: manager / Admin@12345)
echo  Staff Member  : sneha.iyer    / Admin@12345 (or: employee / Admin@12345)
echo =======================================================================
echo.
echo Note: The separate "Smart EMS Django Server" window will stay open to serve requests.
echo You can safely minimize it while using the web application.
echo.
echo Press any key to close this launcher window...
pause >nul

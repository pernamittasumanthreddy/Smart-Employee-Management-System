@echo off
title Smart Employee Management System Launcher
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

:: Check if server is already running on port 8000
netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL% neq 0 (
    start "Smart EMS Application Server" %PY_BIN% manage.py runserver 127.0.0.1:8000
    timeout /t 3 /nobreak >nul
)

:: Open web browser to application
start "" "http://127.0.0.1:8000/"
exit

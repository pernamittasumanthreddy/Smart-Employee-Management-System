@echo off
title Push Smart EMS with GitHub Token
color 0A
cd /d "%~dp0"

echo =======================================================================
echo    PUSH SMART EMS TO GITHUB VIA PERSONAL ACCESS TOKEN (PAT)
echo    Repository: https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
echo =======================================================================
echo.
echo If you have a GitHub Personal Access Token (or generate one from https://github.com/settings/tokens):
echo.
set /p GITHUB_TOKEN="Enter your GitHub Personal Access Token (PAT): "

if "%GITHUB_TOKEN%"=="" (
    echo.
    echo [ERROR] No token entered. Exiting...
    pause
    exit /b 1
)

echo.
echo [PUSHING] Uploading 50,000+ LOC to GitHub main branch...
git push https://%GITHUB_TOKEN%@github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git main -u

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================================
    echo    SUCCESS! Project successfully pushed to GitHub:
    echo    https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System
    echo =======================================================================
) else (
    echo.
    echo [ERROR] Push failed. Please check your token permissions (ensure 'repo' scope is checked).
)

echo.
pause

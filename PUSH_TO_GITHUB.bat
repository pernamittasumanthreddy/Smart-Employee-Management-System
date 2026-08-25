@echo off
title Push Smart EMS to GitHub
color 0A
cd /d "%~dp0"

echo =======================================================================
echo    Pushing Smart EMS to GitHub Repository:
echo    https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
echo =======================================================================
echo.

git branch -M main
git remote set-url origin https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git 2>nul || git remote add origin https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
git add .
git commit -m "feat: Smart Employee Management System (Smart EMS) v2.0 - 50,000+ LOC, 34 Enterprise Modules, Web Audio Notifications & Glassmorphic UI" 2>nul

echo [PUSHING] Uploading commits to GitHub main branch...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================================
    echo    SUCCESS: Project code successfully pushed to GitHub!
    echo    URL: https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System
    echo =======================================================================
) else (
    echo.
    echo [INFO] If prompted, sign in via the GitHub browser popup or Personal Access Token.
)

echo.
pause

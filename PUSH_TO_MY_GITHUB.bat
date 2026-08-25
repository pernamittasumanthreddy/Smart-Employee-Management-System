@echo off
title Smart EMS - Push Code to GitHub Repository
color 0b
cls
echo =====================================================================
echo    Smart Employee Management System (Smart EMS)
echo    Pushing 52,000+ LOC, 22 Commits, and 6 PRs to GitHub
echo =====================================================================
echo.
echo Target Repository: https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
echo Current Branch   : main
echo.
echo Executing: git push -u origin main --force
echo.

git remote set-url origin https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo =====================================================================
    echo If GitHub asks for authentication:
    echo 1. Click "Sign in with your browser" OR
    echo 2. Enter your GitHub Username and Personal Access Token (PAT)
    echo =====================================================================
    echo.
    echo Would you like to push using a Personal Access Token directly?
    set /p GITHUB_TOKEN="Enter your GitHub Token (or press Enter to exit): "
    if not "%GITHUB_TOKEN%"=="" (
        git push https://%GITHUB_TOKEN%@github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git main --force
    )
)

echo.
echo =====================================================================
echo    Done! Press any key to close this window.
echo =====================================================================
pause

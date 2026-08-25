@echo off
title GitHub CLI Authentication
color 0b
cls
echo =====================================================================
echo    GitHub CLI Authentication (gh auth login)
echo =====================================================================
echo.
echo Running: gh auth login
echo.
echo Follow the prompts on screen:
echo  - Account: GitHub.com
echo  - Protocol: HTTPS
echo  - Authenticate Git: Yes
echo  - Method: Login with a web browser (or Paste authentication token)
echo.
"C:\Program Files\GitHub CLI\gh.exe" auth login
echo.
echo Authentication complete! You can now proceed.
pause

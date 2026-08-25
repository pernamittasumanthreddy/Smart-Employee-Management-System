@echo off
title Smart EMS - Push All Branches and Create GitHub Pull Requests
color 0b
cls
echo =====================================================================
echo    Smart EMS - Push Branches and Create Pull Requests on GitHub
echo =====================================================================
echo.
echo Target Repository: https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System.git
echo.
echo 1. Pushing all branches (main + 14 feature branches)...
git push origin --all
git push origin main

echo.
echo 2. If you would like to automatically generate and merge PRs on GitHub,
echo    enter your GitHub Personal Access Token (PAT) below.
echo    (Or press ENTER if you already logged in with GitHub CLI / want to open PRs manually)
echo.
set /p GITHUB_TOKEN="Enter GitHub Token (optional, press Enter to skip): "

powershell -ExecutionPolicy Bypass -File scripts\create_github_prs.ps1 -GitHubToken "%GITHUB_TOKEN%"

echo.
echo =====================================================================
echo    Done! You can check your repository at:
echo    https://github.com/pernamittasumanthreddy/Smart-Employee-Management-System
echo =====================================================================
pause

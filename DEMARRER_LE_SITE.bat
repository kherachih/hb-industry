@echo off
title HB Industry Group - Terminal Site
echo ========================================================
echo    LANCEMENT DU SITE WEB - CLONE EXACT TERMINAL
echo ========================================================
echo.
echo Lancement du serveur local sur http://localhost:8080 ...
cd /d "%~dp0"
start http://localhost:8080/
python -m http.server 8080
pause

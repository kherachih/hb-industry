@echo off
title HB Industry Group - Serveur Web & Espace Admin
echo ========================================================
echo    HB INDUSTRY GROUP - SITE WEB & PORTAIL ADMIN
echo ========================================================
echo.
echo Lancement du serveur complet sur http://localhost:8080 ...
echo.
echo  - Site Public  : http://localhost:8080/
echo  - Espace Admin : http://localhost:8080/admin
echo  - Identifiants : admin / hbig2026
echo.
cd /d "%~dp0"
start http://localhost:8080/
python server.py
pause

@echo off
title AETHER GHOST OS - Dashboard Server
echo 💀😈🤫 AETHER GHOST OS - Dashboard Server 🤫😈💀
echo ==================================================
echo Starting local web server on port 8080...
echo.
echo Launching browser to http://localhost:8080/ghost_dashboard.html...
echo.
start "" "http://localhost:8080/ghost_dashboard.html"
python ghost_tools/server_daemon.py
echo.
pause

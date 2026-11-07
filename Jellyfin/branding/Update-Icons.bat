@echo off
title Omiflix Icon Installer
echo ========================================================
echo Updating Jellyfin Web Icons to Omiflix Custom Icons...
echo ========================================================

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [!] ERROR: Administrator rights required!
    echo Please right-click this file and select 'Run as Administrator'.
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"
python "replace_web_icons.py"

echo.
echo ========================================================
echo [SUCCESS] All Jellyfin server & web icons replaced!
echo Restart your Jellyfin app to see the new icons.
echo ========================================================
echo.
pause

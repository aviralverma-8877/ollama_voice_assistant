@echo off
REM Script to remove Ollama Voice Assistant firewall rule
REM Run this as Administrator

echo ======================================================================
echo   REMOVE FIREWALL RULE
echo ======================================================================
echo.
echo This script will remove the firewall rule for the web server.
echo.
echo ======================================================================
echo.

REM Check for admin rights
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] This script requires Administrator privileges
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Removing firewall rule...
echo.

netsh advfirewall firewall delete rule name="Ollama Voice Assistant Web Server"

if errorlevel 1 (
    echo [ERROR] Failed to remove firewall rule (may not exist)
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   SUCCESS
echo ======================================================================
echo.
echo Firewall rule removed successfully!
echo.
echo The web server will no longer accept connections from other devices.
echo.
echo ======================================================================
echo.
pause

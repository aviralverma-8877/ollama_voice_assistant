@echo off
REM Script to allow Ollama Voice Assistant web server through Windows Firewall
REM Run this as Administrator

echo ======================================================================
echo   WINDOWS FIREWALL CONFIGURATION
echo ======================================================================
echo.
echo This script will allow the Ollama Voice Assistant web server
echo to accept connections from other devices on your local network.
echo.
echo Port: 5000 (default)
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

echo [INFO] Adding firewall rule for port 5000...
echo.

REM Remove existing rule if it exists
netsh advfirewall firewall delete rule name="Ollama Voice Assistant Web Server" >nul 2>&1

REM Add new inbound rule
netsh advfirewall firewall add rule name="Ollama Voice Assistant Web Server" dir=in action=allow protocol=TCP localport=5000

if errorlevel 1 (
    echo [ERROR] Failed to add firewall rule
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   SUCCESS
echo ======================================================================
echo.
echo Firewall rule added successfully!
echo.
echo The web server (port 5000) can now accept connections from other
echo devices on your local network.
echo.
echo To remove this rule later, run: remove_firewall.bat
echo.
echo ======================================================================
echo.
pause

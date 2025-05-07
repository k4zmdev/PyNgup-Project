@echo off
title NGUP - Setup
color 0B

echo.
echo [---------------------------------------------------]
echo [             NGUP - Hash and Malware Scanner         ]
echo [                Developed by Kazam                 ]
echo [---------------------------------------------------]
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo Please install Python 3.8 or later from:
    echo https://www.python.org/downloads/
    pause
    exit /b
)

echo [+] Python Version:
echo [+] Pip Version:
pip --version

echo.
echo [+] Installing required Python modules...
python.exe -m pip install --upgrade pip
pip install requests colorama

if %errorlevel% neq 0 (
    echo [!] Failed to install required modules.
    pause
    exit /b
)

if exist updater.py (
    echo [+] Launching updater...
    python updater.py
) else if exist updater.exe (
    echo [+] Launching updater...
    start updater.py
) else (
    echo [!] No updater found. Skipping...
)

echo.
echo [+] Setup complete. You can now run NGUP manually.
pause

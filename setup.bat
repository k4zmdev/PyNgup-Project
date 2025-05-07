@echo off
title NGUP - Setup
color 0B

echo.
echo [---------------------------------------------------]
echo [             NGUP - Hash and Malware Scanner       ]
echo [                Developed by Kazam                 ]
echo [---------------------------------------------------]
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo Please install Python 3.12 or later from:
    echo https://www.python.org/downloads/
    pause
    exit /b
)

echo [+] Python Version:
python --version

echo [+] Pip Version:
pip --version

echo.
echo [+] Creating virtual environment in 'venv' folder...
python -m venv venv

if exist venv\Scripts\activate.bat (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] Failed to create virtual environment.
    pause
    exit /b
)

echo.
echo [+] Upgrading pip and installing required Python modules...
python -m pip install --upgrade pip
pip install requests colorama

if %errorlevel% neq 0 (
    echo [!] Failed to install required modules.
    pause
    exit /b
)

if exist updater.py (
    echo [+] Launching updater...
    python src/updater.py
) else if exist updater.py (
    echo [+] Launching updater...
    start updater.py
) else (
    echo [!] No updater found. Skipping...
)

echo.
echo [+] Setup complete. Virtual environment is ready in 'venv\'.
echo [+] To activate it manually later, run: venv\Scripts\activate
pause

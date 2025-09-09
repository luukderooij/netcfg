@echo off
setlocal enabledelayedexpansion

REM Naam van de virtuele omgeving
set VENV_DIR=.venv
set CACHE_FILE=.deps_cache.txt

REM Ga naar de directory van het script
cd /d "%~dp0"
echo [INFO] Huidige directory: %cd%

REM Controleer of virtuele omgeving bestaat, zo niet maak hem aan
if not exist %VENV_DIR% (
    echo [INFO] Virtuele omgeving wordt aangemaakt...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo [ERROR] Er ging iets mis bij het aanmaken van de virtuele omgeving.
        exit /b %errorlevel%
    )
)

REM Activeer de virtuele omgeving
call %VENV_DIR%\Scripts\activate

REM Controleer of cache bestaat en vergelijk met requirements.txt
if exist %CACHE_FILE% (
    fc requirements.txt %CACHE_FILE% >nul
    if errorlevel 1 (
        echo [INFO] Requirements zijn veranderd, opnieuw installeren...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo [ERROR] Er ging iets mis bij het installeren van dependencies.
            exit /b %errorlevel%
        )
        copy /y requirements.txt %CACHE_FILE% >nul
    ) else (
        echo [INFO] Requirements ongewijzigd, dependencies overslaan...
    )
) else (
    echo [INFO] Eerste keer installeren...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Er ging iets mis bij het installeren van dependencies.
        exit /b %errorlevel%
    )
    copy /y requirements.txt %CACHE_FILE% >nul
)

REM Start je applicatie
echo [INFO] Start applicatie...

python main.py
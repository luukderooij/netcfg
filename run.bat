@echo off
cd /d "%~dp0"

:: Controleer of de venv al bestaat, zo niet maak hem aan
if not exist .venv (
    echo 🔧 Virtuele omgeving wordt aangemaakt...
    python -m venv .venv
)

:: Activeer de virtuele omgeving
call venv\Scripts\activate.bat

:: Installeer de vereiste pakketten
echo 📦 Benodigde pakketten installeren...
pip install --upgrade pip
pip install wmi pywin32

:: Start je script
echo 🚀 Script starten...
python main.py

pause
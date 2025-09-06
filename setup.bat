@echo off
echo ================================
echo 🛡️  Cybersecurity Intelligence
echo    Application Setup Script
echo ================================
echo.

REM Check if Node.js is installed
echo [INFO] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 20.18.0 or later.
    echo Download from: https://nodejs.org/en/download/
    pause
    exit /b 1
)
echo [SUCCESS] Node.js is installed

REM Check if Python is installed
echo [INFO] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.12 or later.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed

REM Setup Backend
echo.
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy env.example .env
    echo [WARNING] Please edit .env file with your MongoDB connection string if needed
)

REM Run data ingestion
echo [INFO] Ingesting MITRE ATT&CK data...
python data_ingestion.py

echo [SUCCESS] Backend setup complete!

REM Setup Frontend
echo.
echo [INFO] Setting up frontend...
cd ..\frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install --legacy-peer-deps

echo [SUCCESS] Frontend setup complete!

echo.
echo ================================
echo 🎉 Setup completed successfully!
echo ================================
echo.
echo To start the application:
echo 1. Start MongoDB service
echo 2. Run: start.bat
echo.
echo Or manually:
echo - Backend: cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo - Frontend: cd frontend && npm start
echo.
pause


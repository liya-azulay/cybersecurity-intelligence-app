@echo off
echo ================================
echo 🛡️  Cybersecurity Intelligence
echo    Setup with nvm
echo ================================
echo.

REM Check if nvm is installed
echo [INFO] Checking nvm installation...
nvm version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] nvm is not installed or not in PATH.
    echo Please install nvm-windows first:
    echo 1. Download from: https://github.com/coreybutler/nvm-windows/releases
    echo 2. Run the installer as Administrator
    echo 3. Restart your computer
    echo 4. Run this script again
    pause
    exit /b 1
)

echo [SUCCESS] nvm is installed

REM Install and use Node.js 20.18.0
echo [INFO] Installing Node.js 20.18.0...
nvm install 20.18.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js 20.18.0
    pause
    exit /b 1
)

echo [INFO] Using Node.js 20.18.0...
nvm use 20.18.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to use Node.js 20.18.0
    pause
    exit /b 1
)

echo [SUCCESS] Node.js 20.18.0 is now active

REM Check Node.js and npm versions
echo [INFO] Checking versions...
node --version
npm --version

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
echo Node.js version: 
node --version
echo npm version:
npm --version
echo.
echo To start the application:
echo 1. Start MongoDB service
echo 2. Run: start-with-nvm.bat
echo.
echo Or manually:
echo - Backend: cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo - Frontend: cd frontend && npm start
echo.
pause


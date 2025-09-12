@echo off
echo ================================
echo 🛡️  Cybersecurity Intelligence
echo    Start with nvm
echo ================================
echo.

REM Use Node.js 20.18.0
echo [INFO] Using Node.js 20.18.0...
nvm use 20.18.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to use Node.js 20.18.0
    echo Please run setup-with-nvm.bat first
    pause
    exit /b 1
)

REM Check if MongoDB is running
echo [INFO] Checking MongoDB...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if %errorlevel% neq 0 (
    echo [WARNING] MongoDB is not running. Please start MongoDB service.
    echo You can start it manually or install MongoDB as a service.
    echo.
)

REM Start Backend
echo [INFO] Starting backend server...
cd backend
call venv\Scripts\activate.bat
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [INFO] Starting frontend server...
cd ..\frontend
start "Frontend Server" cmd /k "npm start"

echo.
echo ================================
echo 🎉 Application started!
echo ================================
echo.
echo Node.js version:
node --version
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🧪 API Health Check: http://localhost:8000/api/v1/health
echo.
echo Press any key to exit...
pause >nul


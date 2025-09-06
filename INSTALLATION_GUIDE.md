# 🛡️ Cybersecurity Intelligence App - Installation Guide

## 📋 Prerequisites

Before starting the installation, make sure you have the following installed:

### 1. Node.js 20.18.0+

- **Download**: https://nodejs.org/en/download/
- **Alternative**: Use nvm (Node Version Manager)
  ```bash
  # Install nvm first, then:
  nvm install 20.18.0
  nvm use 20.18.0
  ```

### 2. Python 3.12+

- **Download**: https://www.python.org/downloads/
- **Important**: Make sure to check "Add Python to PATH" during installation

### 3. MongoDB

- **Option 1 - Local Installation**: https://www.mongodb.com/try/download/community
- **Option 2 - MongoDB Atlas (Cloud)**: https://www.mongodb.com/atlas
- **Option 3 - Docker**: `docker run -d -p 27017:27017 --name mongodb mongo:latest`

## 🚀 Quick Installation (Windows)

### Method 1: Automated Setup

1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the project directory
3. Run the setup script:
   ```cmd
   setup.bat
   ```
4. Start the application:
   ```cmd
   start.bat
   ```

### Method 2: Manual Setup

#### Backend Setup

```cmd
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
copy env.example .env

# Load MITRE ATT&CK data
python data_ingestion.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```cmd
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start frontend server
npm start
```

## 🐧 Linux/macOS Installation

### Prerequisites Check

```bash
# Check Node.js version
node --version  # Should be 20.18.0+

# Check Python version
python3 --version  # Should be 3.12+

# Check if MongoDB is installed
mongod --version
```

### Setup Script

```bash
# Make the script executable
chmod +x start.sh

# Run the setup
./start.sh
```

### Manual Setup (Linux/macOS)

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env
python data_ingestion.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in new terminal)
cd frontend
nvm use  # Use Node.js 20.18.0
npm install --legacy-peer-deps
npm start
```

## 🔧 Configuration

### MongoDB Configuration

1. **Local MongoDB**: Default connection string is `mongodb://localhost:27017`
2. **MongoDB Atlas**: Update the connection string in `backend/.env`
3. **Custom MongoDB**: Modify the connection string in `backend/.env`

### Environment Variables

Edit `backend/.env` file:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=cybersecurity_intelligence
```

## 🧪 Testing the Installation

### Backend Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Frontend Access

Open your browser and go to: http://localhost:3000

### API Documentation

Visit: http://localhost:8000/docs

## 🚨 Troubleshooting

### Common Issues

#### 1. Node.js Version Issues

```bash
# If you get "Unsupported URL Type 'npm:'" error
nvm use 20.18.0
node --version  # Should show v20.18.0
```

#### 2. Python Dependencies Issues

```bash
# Clear pip cache and reinstall
pip cache purge
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. MongoDB Connection Issues

```bash
# Check if MongoDB is running
# Windows:
net start MongoDB

# Linux/macOS:
sudo systemctl start mongod
# or
brew services start mongodb-community
```

#### 4. Port Already in Use

```bash
# Kill processes on ports 3000 and 8000
# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Linux/macOS:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

#### 5. npm Install Fails

```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

## 📊 Application URLs

After successful installation:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🎯 Next Steps

1. **Explore the Dashboard**: Navigate to the main dashboard to see attack pattern statistics
2. **Search Functionality**: Use the search bar to find specific attack patterns
3. **View Details**: Click on any attack pattern to see detailed information
4. **API Testing**: Use the Swagger documentation at `/docs` to test API endpoints

## 📞 Getting Help

If you encounter issues not covered in this guide:

1. Check the [Issues](https://github.com/shiran1989/magshimim-cyber-homework/issues) page
2. Create a new issue with:
   - Your operating system
   - Node.js version (`node --version`)
   - Python version (`python --version`)
   - Error message and steps to reproduce

## 🎉 Success!

If everything is working correctly, you should see:

- Backend server running on port 8000
- Frontend server running on port 3000
- MongoDB connection established
- MITRE ATT&CK data loaded successfully

Enjoy exploring the Cybersecurity Intelligence Application! 🛡️

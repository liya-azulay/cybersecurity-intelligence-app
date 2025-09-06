# 🚀 התקנה מהירה - Cybersecurity Intelligence App

## ⚠️ בעיה עם הטרמינל

יש בעיה עם הטרמינל הנוכחי (מוסיף תו "ב" לפני פקודות).
השתמש בהוראות הבאות להתקנה ידנית:

## 📋 דרישות מוקדמות

### 1. Node.js 20.18.0+

- **הורדה**: https://nodejs.org/en/download/
- **בדיקה**: פתח Command Prompt חדש והקלד `node -v`

### 2. Python 3.12+

- **הורדה**: https://www.python.org/downloads/
- **חשוב**: סמן "Add Python to PATH" במהלך ההתקנה
- **בדיקה**: פתח Command Prompt חדש והקלד `python -V`

### 3. MongoDB

- **הורדה**: https://www.mongodb.com/try/download/community
- **או**: MongoDB Atlas (cloud) - https://www.mongodb.com/atlas

## 🚀 התקנה מהירה

### שלב 1: פתח Command Prompt חדש

1. לחץ `Win + R`
2. הקלד `cmd` ולחץ Enter
3. נווט לתיקיית הפרויקט:
   ```cmd
   cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"
   ```

### שלב 2: הרץ התקנה אוטומטית

```cmd
setup.bat
```

### שלב 3: הפעל את האפליקציה

```cmd
start.bat
```

## 🔧 התקנה ידנית (אם הסקריפט לא עובד)

### Backend Setup

```cmd
# נווט לתיקיית backend
cd backend

# צור virtual environment
python -m venv venv

# הפעל virtual environment
venv\Scripts\activate

# עדכן pip
python -m pip install --upgrade pip

# התקן dependencies
pip install -r requirements.txt

# העתק קובץ סביבה
copy env.example .env

# טען נתוני MITRE ATT&CK
python data_ingestion.py

# הפעל שרת backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (טרמינל חדש)

פתח Command Prompt חדש:

```cmd
# נווט לתיקיית הפרויקט
cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"

# נווט לתיקיית frontend
cd frontend

# התקן dependencies
npm install --legacy-peer-deps

# הפעל שרת frontend
npm start
```

## 🌐 גישה לאפליקציה

אחרי ההתקנה:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 פתרון בעיות

### אם Node.js לא נמצא:

1. הורד והתקן Node.js מ: https://nodejs.org/
2. הפעל מחדש את המחשב
3. פתח Command Prompt חדש

### אם Python לא נמצא:

1. הורד והתקן Python מ: https://www.python.org/
2. ודא שסימנת "Add Python to PATH"
3. הפעל מחדש את המחשב

### אם MongoDB לא רץ:

1. התקן MongoDB מ: https://www.mongodb.com/try/download/community
2. הפעל את השירות:
   ```cmd
   net start MongoDB
   ```

### אם פורטים תפוסים:

```cmd
# בדוק מה רץ על פורט 3000
netstat -ano | findstr :3000

# בדוק מה רץ על פורט 8000
netstat -ano | findstr :8000

# הרוג תהליך (החלף <PID> במספר התהליך)
taskkill /PID <PID> /F
```

## 🎉 הצלחה!

אם הכל עובד, תראה:

- שרת backend רץ על פורט 8000
- שרת frontend רץ על פורט 3000
- חיבור ל-MongoDB מוצלח
- נתוני MITRE ATT&CK נטענו

תהנה מהאפליקציה! 🛡️

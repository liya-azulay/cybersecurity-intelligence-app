# 🚀 הפעלת הפרויקט - Cybersecurity Intelligence App

## ⚠️ בעיה עם הטרמינל

יש בעיה עם הטרמינל הנוכחי (מוסיף תו "ב" לפני פקודות).
השתמש בהוראות הבאות להפעלה ידנית:

## 📋 דרישות מוקדמות

- **Node.js 20.18.0+** ✅ (יש לך v22.19.0)
- **Python 3.12+** ✅ (יש לך Python 3.13.7)
- **MongoDB** ❓ (צריך לבדוק)

## 🚀 הפעלה ידנית

### שלב 1: פתח Command Prompt חדש

1. לחץ `Win + R`
2. הקלד `cmd` ולחץ Enter
3. נווט לתיקיית הפרויקט:
   ```cmd
   cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"
   ```

### שלב 2: הפעל MongoDB

```cmd
# נסה להפעיל את השירות
net start MongoDB

# או התקן MongoDB אם לא מותקן
# הורד מ: https://www.mongodb.com/try/download/community
```

### שלב 3: הפעל Backend

```cmd
# נווט לתיקיית backend
cd backend

# הפעל virtual environment
venv\Scripts\activate

# הפעל שרת backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### שלב 4: הפעל Frontend (טרמינל חדש)

פתח Command Prompt חדש:

```cmd
# נווט לתיקיית הפרויקט
cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"

# נווט לתיקיית frontend
cd frontend

# התקן dependencies (אם עדיין לא התקנת)
npm install --legacy-peer-deps

# הפעל שרת frontend
npm start
```

## 🌐 גישה לאפליקציה

אחרי ההפעלה:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 פתרון בעיות

### אם MongoDB לא רץ:

```cmd
# בדוק אם השירות קיים
sc query MongoDB

# הפעל את השירות
net start MongoDB

# או התקן MongoDB
# הורד מ: https://www.mongodb.com/try/download/community
```

### אם Backend לא עובד:

```cmd
# בדוק שה-virtual environment פעיל
venv\Scripts\activate

# התקן dependencies
pip install -r requirements.txt

# הפעל שרת
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### אם Frontend לא עובד:

```cmd
# התקן dependencies
npm install --legacy-peer-deps

# הפעל שרת
npm start
```

## 🎯 הפעלה מהירה

### אפשרות 1: שימוש בסקריפטים

```cmd
# התקנה
setup.bat

# הפעלה
start.bat
```

### אפשרות 2: הפעלה ידנית

```cmd
# Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (טרמינל חדש)
cd frontend
npm start
```

## 🎉 הצלחה!

אם הכל עובד, תראה:

- שרת backend רץ על פורט 8000
- שרת frontend רץ על פורט 3000
- חיבור ל-MongoDB מוצלח
- נתוני MITRE ATT&CK נטענו

תהנה מהאפליקציה! 🛡️

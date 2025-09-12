# 🚀 התקנת nvm (Node Version Manager) עבור Windows

## ⚠️ בעיה עם הטרמינל

יש בעיה עם הטרמינל הנוכחי (מוסיף תו "ב" לפני פקודות).
השתמש בהוראות הבאות להתקנת nvm ידנית:

## 📥 התקנת nvm-windows

### שלב 1: הורדת nvm-windows

1. פתח דפדפן וגש ל: https://github.com/coreybutler/nvm-windows/releases
2. הורד את הקובץ `nvm-setup.exe` מהגרסה האחרונה
3. או השתמש בקישור ישיר: https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe

### שלב 2: התקנת nvm

1. הרץ את הקובץ `nvm-setup.exe` כמנהל
2. עקוב אחר הוראות ההתקנה
3. הפעל מחדש את המחשב

### שלב 3: בדיקת ההתקנה

פתח Command Prompt חדש והקלד:

```cmd
nvm version
```

## 🔧 שימוש ב-nvm

### התקנת Node.js 20.18.0

```cmd
# התקן את הגרסה הנדרשת
nvm install 20.18.0

# השתמש בגרסה זו
nvm use 20.18.0

# בדוק שהגרסה נכונה
node -v
npm -v
```

### רשימת גרסאות מותקנות

```cmd
nvm list
```

### החלפת גרסאות

```cmd
# השתמש בגרסה ספציפית
nvm use 20.18.0

# השתמש בגרסה האחרונה
nvm use latest
```

## 🛠️ התקנת הפרויקט עם nvm

### שלב 1: הגדרת Node.js

```cmd
# נווט לתיקיית הפרויקט
cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"

# השתמש בגרסה הנדרשת
nvm use 20.18.0
```

### שלב 2: התקנת Frontend

```cmd
# נווט לתיקיית frontend
cd frontend

# התקן dependencies
npm install --legacy-peer-deps

# הפעל שרת frontend
npm start
```

### שלב 3: התקנת Backend (טרמינל חדש)

פתח Command Prompt חדש:

```cmd
# נווט לתיקיית הפרויקט
cd "C:\Users\LIYA\Downloads\RafaelProject\magshimim-cyber-homework"

# נווט לתיקיית backend
cd backend

# צור virtual environment
python -m venv venv

# הפעל virtual environment
venv\Scripts\activate

# התקן dependencies
pip install -r requirements.txt

# העתק קובץ סביבה
copy env.example .env

# טען נתוני MITRE ATT&CK
python data_ingestion.py

# הפעל שרת backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 פתרון בעיות

### אם nvm לא נמצא אחרי ההתקנה:

1. הפעל מחדש את המחשב
2. פתח Command Prompt חדש
3. בדוק שה-PATH מכיל את nvm

### אם Node.js לא מתקין:

```cmd
# נקה cache
nvm cache clean

# נסה שוב
nvm install 20.18.0
```

### אם npm לא עובד:

```cmd
# בדוק שהגרסה נכונה
nvm use 20.18.0

# בדוק npm
npm -v
```

## 📚 קישורים שימושיים

- **nvm-windows**: https://github.com/coreybutler/nvm-windows
- **Node.js**: https://nodejs.org/
- **npm**: https://www.npmjs.com/

## 🎯 יתרונות nvm

1. **ניהול גרסאות**: החלפה קלה בין גרסאות Node.js
2. **פרויקטים מרובים**: כל פרויקט יכול להשתמש בגרסה שונה
3. **התקנה מהירה**: התקנה של גרסאות חדשות בקלות
4. **ניהול dependencies**: כל גרסה עם dependencies נפרדים

## 🎉 הצלחה!

אחרי ההתקנה תוכל:

- להשתמש ב-Node.js 20.18.0 לפרויקט זה
- להחליף בין גרסאות בקלות
- לנהל פרויקטים עם גרסאות שונות

תהנה מ-nvm! 🚀

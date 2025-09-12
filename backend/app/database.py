# Import necessary libraries
# os = access to environment variables (addresses, passwords)
# motor = library for async connection to MongoDB
# AsyncIOMotorClient = async MongoDB client
# pymongo = library for sync connection to MongoDB (for scripts)
# MongoClient = sync MongoDB client
# typing = define types
# logging = write log messages
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# Database class - class for managing database connection
# class = template for creating objects
# Optional[AsyncIOMotorClient] = can be AsyncIOMotorClient or None
class Database:
    client: Optional[AsyncIOMotorClient] = None  # async client
    database = None  # the database itself


# create global instance of Database
# db = single instance (singleton) that the whole application uses
db = Database()


# function to get database connection
async def get_database() -> AsyncIOMotorClient:
    """Get database connection"""
    # async = async function (doesn't block)
    # -> AsyncIOMotorClient = function returns AsyncIOMotorClient
    return db.database


# function to connect to MongoDB database
async def connect_to_mongo():
    """Create database connection"""
    try:
        # get MongoDB address from environment variables
        # os.getenv = gets environment variable or default value
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "cybersecurity_intelligence")
        
        # create async MongoDB client
        db.client = AsyncIOMotorClient(mongodb_url)
        # select database
        db.database = db.client[database_name]
        
        # test connection - send ping command
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB at {mongodb_url}")
        logger.info(f"Using database: {database_name}")
        
        # create indexes for faster search
        await create_search_indexes()
        
    except Exception as e:
        # if there's an error, write to log and throw it
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


# פונקציה לסגירת החיבור למסד הנתונים
async def close_mongo_connection():
    """Close database connection"""
    # בדיקה אם יש חיבור פעיל
    if db.client:
        db.client.close()  # סגירת החיבור
        logger.info("Disconnected from MongoDB")


# פונקציה ליצירת אינדקסים לחיפוש מהיר
# אינדקס = רשימה מסודרת שמאפשרת חיפוש מהיר
async def create_search_indexes():
    """Create indexes for better search performance"""
    try:
        # בחירת הקולקציה (טבלה) attack_patterns
        collection = db.database.attack_patterns
        
        # יצירת אינדקס טקסט לחיפוש בכל השדות
        # text index = מאפשר חיפוש בכל השדות בבת אחת
        await collection.create_index([
            ("name", "text"),  # חיפוש בשם
            ("description", "text"),  # חיפוש בתיאור
            ("x_mitre_platforms", "text"),  # חיפוש בפלטפורמות
            ("x_mitre_detection", "text"),  # חיפוש בשיטות זיהוי
            ("phase_name", "text"),  # חיפוש בשלב
            ("external_id", "text")  # חיפוש ב-ID חיצוני
        ])
        
        # יצירת אינדקסים נפרדים לכל שדה (לחיפוש regex)
        # אינדקס נפרד = חיפוש מהיר יותר בשדה ספציפי
        await collection.create_index("name")
        await collection.create_index("description")
        await collection.create_index("x_mitre_platforms")
        await collection.create_index("x_mitre_detection")
        await collection.create_index("phase_name")
        await collection.create_index("external_id")
        await collection.create_index("kill_chain_phases.phase_name")  # שדה בתוך אובייקט
        await collection.create_index("external_references.source_name")
        await collection.create_index("external_references.external_id")
        
        # אינדקסים לשדות נוספים של MITRE
        await collection.create_index("x_mitre_domains")
        await collection.create_index("x_mitre_data_sources")
        await collection.create_index("x_mitre_version")
        await collection.create_index("x_mitre_is_subtechnique")
        await collection.create_index("x_mitre_deprecated")
        await collection.create_index("created")
        await collection.create_index("modified")
        
        # אינדקסים מורכבים לחיפושים נפוצים
        # compound index = אינדקס על כמה שדות יחד
        await collection.create_index([("x_mitre_platforms", 1), ("phase_name", 1)])
        await collection.create_index([("x_mitre_domains", 1), ("x_mitre_platforms", 1)])
        await collection.create_index([("x_mitre_is_subtechnique", 1), ("x_mitre_deprecated", 1)])
        
        logger.info("Search indexes created successfully")
    except Exception as e:
        # אם יש שגיאה, כתוב אזהרה (לא עצור את האפליקציה)
        logger.warning(f"Failed to create search indexes: {e}")


# פונקציה לקבלת חיבור סינכרוני למסד הנתונים
# סינכרוני = חוסם עד שהפעולה מסתיימת (לסקריפטים)
def get_sync_database():
    """Get synchronous database connection for data ingestion"""
    # קבלת כתובת MongoDB ממשתני הסביבה
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "cybersecurity_intelligence")
    
    # יצירת לקוח MongoDB סינכרוני (לא async)
    client = MongoClient(mongodb_url)
    # החזרת מסד הנתונים
    return client[database_name]

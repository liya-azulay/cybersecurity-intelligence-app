# Import necessary libraries
# FastAPI = framework for building fast APIs
# CORS = allows frontend (React) to connect to backend (Python)
# logging = for writing log messages (track what happens)
# os = access to environment variables (addresses, passwords)
# dotenv = load environment variables from .env file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import router
from app.bot_router import bot_router

# Load environment variables from .env file
# Environment variables = settings we don't want to write in code (addresses, passwords)
load_dotenv()

# Configure logging - setup logging system
# INFO = level of detail for messages (INFO, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app - create main application
# FastAPI = framework that allows building APIs fast and easy
# title, description, version = information about the API (appears in documentation)
app = FastAPI(
    title="Cybersecurity Intelligence API",
    description="API for managing MITRE ATT&CK attack patterns",
    version="1.0.0"
)

# Add CORS middleware - add CORS middleware
# CORS = Cross-Origin Resource Sharing
# allows frontend (React on port 3000) to connect to backend (Python on port 8000)
# allow_origins = which addresses are allowed to connect
# allow_credentials = whether cookies are allowed
# allow_methods = which HTTP methods are allowed (GET, POST, PUT, DELETE)
# allow_headers = which headers are allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - add routers to application
# router = group of endpoints (API addresses)
# prefix = prefix for all addresses (all endpoints will start with /api/v1)
app.include_router(router, prefix="/api/v1")
app.include_router(bot_router, prefix="/api/v1")


# Event handlers - handle application events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    # @app.on_event("startup") = function that runs when application starts
    # async = function that can wait (doesn't block the server)
    try:
        # connect to MongoDB database
        await connect_to_mongo()
        logger.info("Application startup completed")
    except Exception as e:
        # if there's an error, write to log and stop the application
        logger.error(f"Failed to start application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    # @app.on_event("shutdown") = function that runs when application closes
    try:
        # close database connection
        await close_mongo_connection()
        logger.info("Application shutdown completed")
    except Exception as e:
        # if there's an error, write to log
        logger.error(f"Error during shutdown: {e}")


# Root endpoint - basic endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    # @app.get("/") = endpoint that receives GET requests to base address
    # when someone goes to http://localhost:8000/ they get this response
    return {
        "message": "Cybersecurity Intelligence API",
        "version": "1.0.0",
        "docs": "/docs"  # link to automatic documentation
    }


# Main execution - main application run
if __name__ == "__main__":
    # if file runs directly (not imported), run the server
    import uvicorn
    # uvicorn = fast ASGI server for Python
    uvicorn.run(
        "app.main:app",  # application location (file:object)
        host=os.getenv("API_HOST", "0.0.0.0"),  # server address (0.0.0.0 = all addresses)
        port=int(os.getenv("API_PORT", 8000)),  # server port (8000)
        reload=True  # automatic reload when code changes
    )

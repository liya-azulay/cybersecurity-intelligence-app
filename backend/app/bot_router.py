from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from .bot.models import BotRequest, BotResponse, BotStats
from .bot.cyber_bot import CyberBot

logger = logging.getLogger(__name__)

# Create router for bot endpoints
bot_router = APIRouter(prefix="/bot", tags=["Cyber Bot"])

# Global bot instance
cyber_bot = CyberBot()


@bot_router.post("/chat", response_model=BotResponse)
async def chat_with_bot(request: BotRequest):
    """
    Chat with the cyber bot
    
    This endpoint allows users to send messages to the cyber bot
    and receive intelligent responses about cybersecurity topics.
    
    Supported commands:
    - Search attack patterns: "search process injection"
    - Check hashes: "check md5 5d41402abc4b2a76b9719d911017c592"
    - Get statistics: "stats"
    - Get help: "help"
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = await cyber_bot.process_message(request)
        return response
        
    except Exception as e:
        logger.error(f"Error in bot chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@bot_router.get("/stats", response_model=BotStats)
async def get_bot_stats():
    """
    Get cyber bot statistics
    
    Returns information about bot performance, command usage,
    and overall statistics.
    """
    try:
        stats = cyber_bot.get_bot_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting bot stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@bot_router.get("/health")
async def bot_health_check():
    """
    Health check for the cyber bot
    
    Returns the current status of the bot service.
    """
    try:
        stats = cyber_bot.get_bot_stats()
        return {
            "status": "healthy",
            "message": "Cyber Bot is running",
            "uptime": stats.uptime,
            "total_commands": stats.total_commands,
            "success_rate": (stats.successful_commands / max(1, stats.total_commands)) * 100
        }
        
    except Exception as e:
        logger.error(f"Error in bot health check: {e}")
        return {
            "status": "unhealthy",
            "message": f"Bot error: {str(e)}",
            "uptime": "0:00:00",
            "total_commands": 0,
            "success_rate": 0
        }


@bot_router.get("/commands")
async def get_available_commands():
    """
    Get list of available bot commands
    
    Returns a list of all supported commands and their usage examples.
    """
    try:
        commands = {
            "database_search": {
                "description": "Search attack patterns in the database",
                "examples": [
                    "search process injection",
                    "find Windows attacks",
                    "show me persistence techniques",
                    "what are the attack patterns for malware"
                ]
            },
            "virustotal_check": {
                "description": "Check file hashes against VirusTotal",
                "examples": [
                    "check md5 5d41402abc4b2a76b9719d911017c592",
                    "scan sha1 aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
                    "analyze sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "is md5 5d41402abc4b2a76b9719d911017c592 malicious"
                ]
            },
            "statistics": {
                "description": "Get database and bot statistics",
                "examples": [
                    "stats",
                    "statistics",
                    "how many attack patterns",
                    "database stats"
                ]
            },
            "help": {
                "description": "Get help and command information",
                "examples": [
                    "help",
                    "commands",
                    "what can you do"
                ]
            }
        }
        
        return {
            "available_commands": commands,
            "total_commands": len(commands),
            "bot_version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Error getting available commands: {e}")
        raise HTTPException(status_code=500, detail=str(e))

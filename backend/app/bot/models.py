from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class BotCommandType(str, Enum):
    """Types of bot commands"""
    SEARCH_DB = "search_db"
    CHECK_VIRUSTOTAL = "check_virustotal"
    ANALYZE_HASH = "analyze_hash"
    GET_STATS = "get_stats"
    HELP = "help"
    UNKNOWN = "unknown"


class BotRequest(BaseModel):
    """Request model for bot commands"""
    message: str = Field(..., description="User message/command")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")


class BotResponse(BaseModel):
    """Response model for bot commands"""
    success: bool = Field(..., description="Whether the command was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")
    command_type: BotCommandType = Field(..., description="Type of command executed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class VirusTotalResult(BaseModel):
    """VirusTotal API result"""
    hash_value: str = Field(..., description="Hash value checked")
    is_malicious: bool = Field(..., description="Whether the hash is detected as malicious")
    detection_count: int = Field(0, description="Number of engines that detected it")
    total_engines: int = Field(0, description="Total number of engines")
    scan_date: Optional[str] = Field(None, description="Date of last scan")
    permalink: Optional[str] = Field(None, description="Link to VirusTotal report")


class SearchResult(BaseModel):
    """Search result from database"""
    pattern_id: str = Field(..., description="Attack pattern ID")
    name: str = Field(..., description="Attack pattern name")
    description: str = Field(..., description="Attack pattern description")
    platforms: List[str] = Field(default_factory=list, description="Affected platforms")
    phase: str = Field(..., description="Attack phase")
    detection: str = Field(..., description="Detection methods")


class BotStats(BaseModel):
    """Bot statistics"""
    total_commands: int = Field(0, description="Total commands processed")
    successful_commands: int = Field(0, description="Successful commands")
    failed_commands: int = Field(0, description="Failed commands")
    most_used_commands: Dict[str, int] = Field(default_factory=dict, description="Command usage stats")
    uptime: str = Field(..., description="Bot uptime")

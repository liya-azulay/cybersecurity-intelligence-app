import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .models import (
    BotRequest, BotResponse, BotCommandType, 
    SearchResult, VirusTotalResult, BotStats
)
from .command_parser import CommandParser
from .virustotal_client import VirusTotalClient
from ..services import AttackPatternService
from ..database import get_database

logger = logging.getLogger(__name__)


class CyberBot:
    """Main Cyber Bot class for handling security intelligence tasks"""
    
    def __init__(self):
        self.command_parser = CommandParser()
        self.start_time = datetime.now()
        self.stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "command_usage": {}
        }
    
    async def process_message(self, request: BotRequest) -> BotResponse:
        """
        Process user message and return appropriate response
        
        Args:
            request: Bot request with user message
            
        Returns:
            BotResponse with command result
        """
        try:
            self.stats["total_commands"] += 1
            
            # Parse the command
            command_type, params = self.command_parser.parse_command(request)
            
            # Update command usage stats
            self.stats["command_usage"][command_type.value] = \
                self.stats["command_usage"].get(command_type.value, 0) + 1
            
            # Execute the command
            if command_type == BotCommandType.SEARCH_DB:
                response = await self._handle_database_search(params)
            elif command_type == BotCommandType.CHECK_VIRUSTOTAL:
                response = await self._handle_virustotal_check(params)
            elif command_type == BotCommandType.GET_STATS:
                response = await self._handle_get_stats(params)
            elif command_type == BotCommandType.HELP:
                response = await self._handle_help(params)
            else:
                response = await self._handle_unknown_command(params)
            
            self.stats["successful_commands"] += 1
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.stats["failed_commands"] += 1
            
            return BotResponse(
                success=False,
                message=f"❌ Error processing command: {str(e)}",
                command_type=BotCommandType.UNKNOWN,
                data={"error": str(e)}
            )
    
    async def _handle_database_search(self, params: Dict[str, Any]) -> BotResponse:
        """Handle database search commands"""
        try:
            # Check if it's a specific pattern ID request
            pattern_id = params.get("pattern_id")
            if pattern_id:
                return await self._handle_specific_pattern(pattern_id)
            
            query = params.get("query", "")
            if not query:
                return BotResponse(
                    success=False,
                    message="❌ Please provide a search query",
                    command_type=BotCommandType.SEARCH_DB
                )
            
            # Get database connection
            database = await get_database()
            service = AttackPatternService(database)
            
            # Search for patterns
            patterns, total = await service.search_patterns(query, limit=10, offset=0)
            
            if not patterns:
                return BotResponse(
                    success=True,
                    message=f"🔍 No attack patterns found for: '{query}'",
                    command_type=BotCommandType.SEARCH_DB,
                    data={"total": 0, "results": []}
                )
            
            # Format results
            search_results = []
            for pattern in patterns:
                search_results.append(SearchResult(
                    pattern_id=pattern.get("id", "Unknown"),
                    name=pattern.get("name", "Unknown"),
                    description=pattern.get("description", "No description")[:200] + "...",
                    platforms=pattern.get("x_mitre_platforms", []),
                    phase=pattern.get("phase_name", "Unknown"),
                    detection=pattern.get("x_mitre_detection", "No detection info")[:100] + "..."
                ))
            
            # Create response message
            message = f"🔍 **Search Results for:** '{query}'\n"
            message += f"**Found:** {len(search_results)} patterns (showing first 10 of {total})\n\n"
            
            for i, result in enumerate(search_results, 1):  # Show ALL results
                message += f"**{i}. {result.name}** (`{result.pattern_id}`)\n"
                message += f"   **Phase:** {result.phase}\n"
                message += f"   **Platforms:** {', '.join(result.platforms)}\n"
                message += f"   **Description:** {result.description}\n\n"
            
            if len(search_results) >= 10:  # If we hit the limit
                message += f"💡 **Tip:** Showing first 10 results. Use more specific search terms for better results!\n"
                message += f"🔍 **For details:** Ask about a specific pattern (e.g., 'show me T1055')"
            
            return BotResponse(
                success=True,
                message=message,
                command_type=BotCommandType.SEARCH_DB,
                data={
                    "total": total,
                    "results": [result.dict() for result in search_results]
                }
            )
            
        except Exception as e:
            logger.error(f"Error in database search: {e}")
            return BotResponse(
                success=False,
                message=f"❌ Error searching database: {str(e)}",
                command_type=BotCommandType.SEARCH_DB
            )
    
    async def _handle_specific_pattern(self, pattern_id: str) -> BotResponse:
        """Handle requests for specific pattern details"""
        try:
            # Get database connection
            database = await get_database()
            service = AttackPatternService(database)
            
            # Search for the specific pattern
            patterns, total = await service.search_patterns(pattern_id, limit=1, offset=0)
            
            if not patterns:
                return BotResponse(
                    success=False,
                    message=f"❌ Pattern '{pattern_id}' not found in database",
                    command_type=BotCommandType.SEARCH_DB
                )
            
            pattern = patterns[0]
            
            # Create detailed response
            message = f"""🔍 **Pattern Details: {pattern.get('name', 'Unknown')}**

**ID:** `{pattern.get('id', 'Unknown')}`
**Phase:** {pattern.get('phase_name', 'Unknown')}
**Platforms:** {', '.join(pattern.get('x_mitre_platforms', []))}

**Description:**
{pattern.get('description', 'No description available')}

**Detection:**
{pattern.get('x_mitre_detection', 'No detection information available')}

**External References:**
"""
            
            # Add external references if available
            external_refs = pattern.get('external_references', [])
            if external_refs:
                for ref in external_refs[:3]:  # Show first 3 references
                    source = ref.get('source_name', 'Unknown')
                    url = ref.get('url', '')
                    if url:
                        message += f"• [{source}]({url})\n"
            else:
                message += "No external references available\n"
            
            message += f"\n💡 **Tip:** Use this pattern ID in your security analysis!"
            
            return BotResponse(
                success=True,
                message=message,
                command_type=BotCommandType.SEARCH_DB,
                data={"pattern": pattern}
            )
            
        except Exception as e:
            logger.error(f"Error getting pattern details: {e}")
            return BotResponse(
                success=False,
                message=f"❌ Error getting pattern details: {str(e)}",
                command_type=BotCommandType.SEARCH_DB
            )
    
    async def _handle_virustotal_check(self, params: Dict[str, Any]) -> BotResponse:
        """Handle VirusTotal hash check commands"""
        try:
            if "error" in params:
                return BotResponse(
                    success=False,
                    message=f"❌ {params['error']}",
                    command_type=BotCommandType.CHECK_VIRUSTOTAL
                )
            
            hash_type = params.get("hash_type", "md5")
            hash_value = params.get("hash_value", "")
            
            if not hash_value:
                return BotResponse(
                    success=False,
                    message="❌ Please provide a hash value to check",
                    command_type=BotCommandType.CHECK_VIRUSTOTAL
                )
            
            # Check hash with VirusTotal
            async with VirusTotalClient() as vt_client:
                result = await vt_client.check_hash(hash_value, hash_type)
                message = vt_client.format_result_message(result)
            
            return BotResponse(
                success=True,
                message=message,
                command_type=BotCommandType.CHECK_VIRUSTOTAL,
                data=result.dict()
            )
            
        except Exception as e:
            logger.error(f"Error in VirusTotal check: {e}")
            return BotResponse(
                success=False,
                message=f"❌ Error checking hash with VirusTotal: {str(e)}",
                command_type=BotCommandType.CHECK_VIRUSTOTAL
            )
    
    async def _handle_get_stats(self, params: Dict[str, Any]) -> BotResponse:
        """Handle statistics commands"""
        try:
            # Get database stats
            database = await get_database()
            service = AttackPatternService(database)
            
            # Get total patterns count
            _, total_patterns = await service.get_all_patterns(limit=1, offset=0)
            
            # Get phase distribution
            phase_stats = await database.attack_patterns.aggregate([
                {"$group": {"_id": "$phase_name", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]).to_list(length=None)
            
            # Get platform distribution
            platform_stats = await database.attack_patterns.aggregate([
                {"$unwind": "$x_mitre_platforms"},
                {"$group": {"_id": "$x_mitre_platforms", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]).to_list(length=None)
            
            # Calculate uptime
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds
            
            # Create stats message
            message = f"""
📊 **Cyber Bot Statistics**

**Database:**
• Total Attack Patterns: {total_patterns:,}
• Bot Uptime: {uptime_str}

**Top Attack Phases:**
"""
            
            for stat in phase_stats[:5]:
                message += f"• {stat['_id']}: {stat['count']:,}\n"
            
            message += "\n**Top Platforms:**\n"
            for stat in platform_stats[:5]:
                message += f"• {stat['_id']}: {stat['count']:,}\n"
            
            message += f"\n**Bot Performance:**\n"
            message += f"• Commands Processed: {self.stats['total_commands']}\n"
            message += f"• Success Rate: {(self.stats['successful_commands'] / max(1, self.stats['total_commands'])) * 100:.1f}%\n"
            
            return BotResponse(
                success=True,
                message=message.strip(),
                command_type=BotCommandType.GET_STATS,
                data={
                    "total_patterns": total_patterns,
                    "phase_stats": phase_stats,
                    "platform_stats": platform_stats,
                    "bot_stats": self.stats,
                    "uptime": uptime_str
                }
            )
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return BotResponse(
                success=False,
                message=f"❌ Error getting statistics: {str(e)}",
                command_type=BotCommandType.GET_STATS
            )
    
    async def _handle_help(self, params: Dict[str, Any]) -> BotResponse:
        """Handle help commands"""
        help_message = self.command_parser.get_help_message()
        
        return BotResponse(
            success=True,
            message=help_message,
            command_type=BotCommandType.HELP,
            data={"help_type": "general"}
        )
    
    async def _handle_unknown_command(self, params: Dict[str, Any]) -> BotResponse:
        """Handle unknown commands"""
        message = params.get("message", "")
        
        response_message = f"""
❓ **Unknown Command:** "{message}"

I didn't understand that command. Here are some things I can help you with:

🔍 **Search attack patterns** - Try: `search process injection`
🛡️ **Check hashes** - Try: `check md5 5d41402abc4b2a76b9719d911017c592`
📊 **Get statistics** - Try: `stats`
❓ **Get help** - Try: `help`

Type `help` for a complete list of commands!
        """.strip()
        
        return BotResponse(
            success=False,
            message=response_message,
            command_type=BotCommandType.UNKNOWN,
            data={"original_message": message}
        )
    
    def get_bot_stats(self) -> BotStats:
        """Get current bot statistics"""
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]
        
        return BotStats(
            total_commands=self.stats["total_commands"],
            successful_commands=self.stats["successful_commands"],
            failed_commands=self.stats["failed_commands"],
            most_used_commands=self.stats["command_usage"],
            uptime=uptime_str
        )

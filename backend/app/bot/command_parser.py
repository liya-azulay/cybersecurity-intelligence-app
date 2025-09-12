import re
import logging
from typing import Tuple, Optional, Dict, Any
from .models import BotCommandType, BotRequest

logger = logging.getLogger(__name__)


class CommandParser:
    """Parser for bot commands using natural language processing"""
    
    def __init__(self):
        # Command patterns for different types of requests
        self.patterns = {
            BotCommandType.SEARCH_DB: [
                r"search\s+(?:for\s+)?(.+)",
                r"find\s+(?:attack\s+)?(?:patterns?\s+)?(?:for\s+)?(.+)",
                r"look\s+(?:for\s+)?(.+)",
                r"show\s+(?:me\s+)?(?:attack\s+)?(?:patterns?\s+)?(?:for\s+)?(.+)",
                r"what\s+(?:are\s+)?(?:the\s+)?(?:attack\s+)?(?:patterns?\s+)?(?:for\s+)?(.+)",
                r"list\s+(?:attack\s+)?(?:patterns?\s+)?(?:for\s+)?(.+)",
            ],
            BotCommandType.CHECK_VIRUSTOTAL: [
                r"check\s+(?:the\s+)?(?:hash\s+)?(md5|sha1|sha256)\s+([a-fA-F0-9]+)",
                r"scan\s+(?:the\s+)?(?:hash\s+)?(md5|sha1|sha256)\s+([a-fA-F0-9]+)",
                r"analyze\s+(?:the\s+)?(?:hash\s+)?(md5|sha1|sha256)\s+([a-fA-F0-9]+)",
                r"is\s+(?:the\s+)?(?:hash\s+)?(md5|sha1|sha256)\s+([a-fA-F0-9]+)\s+(?:malicious|bad|virus)",
                r"virustotal\s+(?:check\s+)?(?:the\s+)?(?:hash\s+)?(md5|sha1|sha256)\s+([a-fA-F0-9]+)",
            ],
            BotCommandType.GET_STATS: [
                r"stats?",
                r"statistics?",
                r"show\s+(?:me\s+)?(?:the\s+)?stats?",
                r"how\s+many\s+(?:attack\s+)?patterns?",
                r"count\s+(?:attack\s+)?patterns?",
                r"database\s+stats?",
            ],
            BotCommandType.HELP: [
                r"help",
                r"commands?",
                r"what\s+can\s+you\s+do",
                r"how\s+to\s+use",
                r"usage",
            ],
            BotCommandType.SEARCH_DB: [
                r"show\s+(?:me\s+)?(?:details?\s+)?(?:about\s+)?(?:pattern\s+)?(T\d{4}(?:\.\d{3})?)",
                r"details?\s+(?:for\s+)?(?:pattern\s+)?(T\d{4}(?:\.\d{3})?)",
                r"info\s+(?:about\s+)?(?:pattern\s+)?(T\d{4}(?:\.\d{3})?)",
                r"tell\s+(?:me\s+)?(?:about\s+)?(?:pattern\s+)?(T\d{4}(?:\.\d{3})?)",
            ]
        }
        
        # Hash validation patterns
        self.hash_patterns = {
            "md5": r"^[a-fA-F0-9]{32}$",
            "sha1": r"^[a-fA-F0-9]{40}$",
            "sha256": r"^[a-fA-F0-9]{64}$"
        }
    
    def parse_command(self, request: BotRequest) -> Tuple[BotCommandType, Dict[str, Any]]:
        """
        Parse user message and extract command type and parameters
        
        Args:
            request: Bot request containing user message
            
        Returns:
            Tuple of (command_type, parameters)
        """
        message = request.message.lower().strip()
        
        # Try to match each command type
        for command_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    params = self._extract_parameters(command_type, match, message)
                    logger.info(f"Parsed command: {command_type} with params: {params}")
                    return command_type, params
        
        # If no specific command matched, try to extract search terms
        search_terms = self._extract_search_terms(message)
        if search_terms:
            return BotCommandType.SEARCH_DB, {"query": search_terms}
        
        return BotCommandType.UNKNOWN, {"message": message}
    
    def _extract_parameters(self, command_type: BotCommandType, match: re.Match, message: str) -> Dict[str, Any]:
        """Extract parameters based on command type"""
        params = {}
        
        if command_type == BotCommandType.SEARCH_DB:
            # Check if it's a specific pattern ID request
            if match.groups() and re.match(r"T\d{4}(?:\.\d{3})?", match.group(1)):
                params["pattern_id"] = match.group(1).strip()
            else:
                # Extract search query from the match
                query = match.group(1).strip()
                params["query"] = query
            
        elif command_type == BotCommandType.CHECK_VIRUSTOTAL:
            # Extract hash type and value
            hash_type = match.group(1).lower()
            hash_value = match.group(2).lower()
            
            # Validate hash format
            if self._validate_hash(hash_type, hash_value):
                params["hash_type"] = hash_type
                params["hash_value"] = hash_value
            else:
                params["error"] = f"Invalid {hash_type} hash format"
                
        elif command_type == BotCommandType.GET_STATS:
            params["stats_type"] = "general"
            
        elif command_type == BotCommandType.HELP:
            params["help_type"] = "general"
        
        return params
    
    def _extract_search_terms(self, message: str) -> Optional[str]:
        """Extract potential search terms from unstructured message"""
        # Remove common stop words and extract meaningful terms
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "what", "how", "when", "where", "why"
        }
        
        words = message.split()
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        if meaningful_words:
            return " ".join(meaningful_words)
        
        return None
    
    def _validate_hash(self, hash_type: str, hash_value: str) -> bool:
        """Validate hash format"""
        if hash_type not in self.hash_patterns:
            return False
        
        pattern = self.hash_patterns[hash_type]
        return bool(re.match(pattern, hash_value))
    
    def get_help_message(self) -> str:
        """Get help message with available commands"""
        return """
🤖 **Cyber Bot Commands:**

**Database Search:**
- `search [query]` - Search attack patterns in database
- `find [query]` - Find attack patterns
- `show me [query]` - Display attack patterns
- `what are the attack patterns for [query]`
- `show me T1055` - Get details for specific pattern ID
- `details for T1055` - Get detailed information about a pattern

**VirusTotal Integration:**
- `check md5 [hash]` - Check MD5 hash on VirusTotal
- `scan sha1 [hash]` - Scan SHA1 hash
- `analyze sha256 [hash]` - Analyze SHA256 hash
- `is md5 [hash] malicious` - Check if hash is malicious

**Statistics:**
- `stats` - Show database statistics
- `how many attack patterns` - Count attack patterns

**Help:**
- `help` - Show this help message
- `commands` - List available commands

**Examples:**
- `search process injection`
- `check md5 5d41402abc4b2a76b9719d911017c592`
- `find Windows attacks`
- `stats`
        """.strip()

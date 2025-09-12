import aiohttp
import logging
import os
from typing import Optional, Dict, Any
from .models import VirusTotalResult

logger = logging.getLogger(__name__)


class VirusTotalClient:
    """Client for VirusTotal API integration"""
    
    def __init__(self):
        self.api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.base_url = "https://www.virustotal.com/vtapi/v2"
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def check_hash(self, hash_value: str, hash_type: str = "md5") -> VirusTotalResult:
        """
        Check hash against VirusTotal database
        
        Args:
            hash_value: Hash to check
            hash_type: Type of hash (md5, sha1, sha256)
            
        Returns:
            VirusTotalResult with scan results
        """
        if not self.api_key:
            logger.warning("VirusTotal API key not configured")
            return VirusTotalResult(
                hash_value=hash_value,
                is_malicious=False,
                detection_count=0,
                total_engines=0,
                scan_date=None,
                permalink=None
            )
        
        try:
            # Normalize hash type for VirusTotal API
            vt_hash_type = self._normalize_hash_type(hash_type)
            
            url = f"{self.base_url}/file/report"
            params = {
                "apikey": self.api_key,
                "resource": hash_value
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_virustotal_response(data, hash_value)
                elif response.status == 204:
                    # Rate limit exceeded
                    logger.warning("VirusTotal rate limit exceeded")
                    return VirusTotalResult(
                        hash_value=hash_value,
                        is_malicious=False,
                        detection_count=0,
                        total_engines=0,
                        scan_date=None,
                        permalink=None
                    )
                else:
                    logger.error(f"VirusTotal API error: {response.status}")
                    return VirusTotalResult(
                        hash_value=hash_value,
                        is_malicious=False,
                        detection_count=0,
                        total_engines=0,
                        scan_date=None,
                        permalink=None
                    )
                    
        except Exception as e:
            logger.error(f"Error checking hash with VirusTotal: {e}")
            return VirusTotalResult(
                hash_value=hash_value,
                is_malicious=False,
                detection_count=0,
                total_engines=0,
                scan_date=None,
                permalink=None
            )
    
    def _normalize_hash_type(self, hash_type: str) -> str:
        """Normalize hash type for VirusTotal API"""
        hash_type = hash_type.lower()
        if hash_type in ["md5", "sha1", "sha256"]:
            return hash_type
        return "md5"  # Default fallback
    
    def _parse_virustotal_response(self, data: Dict[str, Any], hash_value: str) -> VirusTotalResult:
        """Parse VirusTotal API response"""
        try:
            response_code = data.get("response_code", 0)
            
            if response_code == 0:
                # Hash not found in VirusTotal
                return VirusTotalResult(
                    hash_value=hash_value,
                    is_malicious=False,
                    detection_count=0,
                    total_engines=0,
                    scan_date=None,
                    permalink=data.get("permalink")
                )
            
            scans = data.get("scans", {})
            total_engines = len(scans)
            detection_count = sum(1 for scan in scans.values() if scan.get("detected", False))
            
            # Consider malicious if more than 0 engines detect it
            is_malicious = detection_count > 0
            
            return VirusTotalResult(
                hash_value=hash_value,
                is_malicious=is_malicious,
                detection_count=detection_count,
                total_engines=total_engines,
                scan_date=data.get("scan_date"),
                permalink=data.get("permalink")
            )
            
        except Exception as e:
            logger.error(f"Error parsing VirusTotal response: {e}")
            return VirusTotalResult(
                hash_value=hash_value,
                is_malicious=False,
                detection_count=0,
                total_engines=0,
                scan_date=None,
                permalink=None
            )
    
    async def get_file_info(self, hash_value: str) -> Dict[str, Any]:
        """
        Get additional file information from VirusTotal
        
        Args:
            hash_value: Hash to get info for
            
        Returns:
            Dictionary with file information
        """
        if not self.api_key:
            return {}
        
        try:
            url = f"{self.base_url}/file/report"
            params = {
                "apikey": self.api_key,
                "resource": hash_value
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "file_name": data.get("filename", "Unknown"),
                        "file_size": data.get("size", 0),
                        "file_type": data.get("type", "Unknown"),
                        "submission_date": data.get("scan_date"),
                        "first_seen": data.get("first_seen"),
                        "last_seen": data.get("last_seen"),
                        "tags": data.get("tags", []),
                        "additional_info": data.get("additional_info", {})
                    }
                else:
                    logger.error(f"VirusTotal file info error: {response.status}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting file info from VirusTotal: {e}")
            return {}
    
    def format_result_message(self, result: VirusTotalResult) -> str:
        """Format VirusTotal result into a user-friendly message"""
        if result.total_engines == 0:
            return f"🔍 **Hash Analysis:** `{result.hash_value}`\n❌ Hash not found in VirusTotal database"
        
        status_emoji = "🚨" if result.is_malicious else "✅"
        status_text = "MALICIOUS" if result.is_malicious else "CLEAN"
        
        detection_rate = (result.detection_count / result.total_engines) * 100
        
        message = f"""
{status_emoji} **Hash Analysis:** `{result.hash_value}`
**Status:** {status_text}
**Detection:** {result.detection_count}/{result.total_engines} engines ({detection_rate:.1f}%)
**Scan Date:** {result.scan_date or 'Unknown'}
        """.strip()
        
        if result.permalink:
            message += f"\n**Report:** {result.permalink}"
        
        return message

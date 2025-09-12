# Import necessary libraries
# pydantic = library for data validation and checking
# BaseModel = base for creating models (data templates)
# Field = define fields with descriptions and default values
# typing = define types (List, Optional)
# datetime = work with dates
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# AttackPattern class - model for attack patterns
# class = template for creating objects
# BaseModel = inherits from Pydantic (gets automatic validation)
class AttackPattern(BaseModel):
    """Model for MITRE ATT&CK attack patterns"""
    # id: str = required field (str = string/text)
    # Field(...) = required field (dots mean it's required)
    id: str = Field(..., description="Unique identifier for the attack")
    name: str = Field(..., description="Name of the attack")
    description: str = Field(..., description="Description of the attack")
    
    # List[str] = list of strings
    # default_factory=list = default value (empty list)
    x_mitre_platforms: List[str] = Field(default_factory=list, description="Vulnerable platforms")
    
    # default="NA" = default value if not provided
    x_mitre_detection: str = Field(default="NA", description="Detection methods")
    phase_name: str = Field(default="NA", description="Attack phase")
    external_id: str = Field(..., description="External ID from MITRE")
    
    # List[dict] = list of dictionaries (JSON objects)
    kill_chain_phases: List[dict] = Field(default_factory=list, description="Kill chain phases")
    external_references: List[dict] = Field(default_factory=list, description="External references")
    
    # dates
    created_at: str = Field(default="N/A", description="Creation date")
    modified_at: str = Field(default="N/A", description="Last modification date")

    # Config class = additional model settings
    class Config:
        pass


# AttackPatternResponse class - model for response (what server returns)
# this is a separate model because sometimes we want to return fewer fields or different fields
class AttackPatternResponse(BaseModel):
    """Response model for attack patterns"""
    # all fields returned to user
    id: str
    name: str
    description: str
    x_mitre_platforms: List[str]
    x_mitre_detection: str
    phase_name: str
    external_id: str
    kill_chain_phases: List[dict]
    external_references: List[dict]
    created_at: str
    modified_at: str


# SearchRequest class - model for search request
# this is what user sends when searching
class SearchRequest(BaseModel):
    """Request model for search functionality"""
    # query = what user is searching for (required)
    query: str = Field(..., description="Search query")
    
    # limit = how many results to return (default: 50)
    limit: int = Field(default=50, description="Maximum number of results")
    
    # offset = how many results to skip (for next page)
    offset: int = Field(default=0, description="Number of results to skip")


# SearchResponse class - model for search response
# this is what server returns after search
class SearchResponse(BaseModel):
    """Response model for search results"""
    # results = list of attack patterns we found
    results: List[AttackPatternResponse]
    
    # total = how many results there are in total
    total: int
    
    # limit = how many we requested
    limit: int
    
    # offset = where we started
    offset: int

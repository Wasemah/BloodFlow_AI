"""
Communication Schema (comm_schema.py)

Pydantic models for the Communication Agent.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CommResult(BaseModel):
    """Result of the communication workflow."""
    
    status: str = Field(
        ...,
        description="Success or failure",
        example="success"
    )
    
    message: str = Field(
        ...,
        description="Human-readable result message",
        example="Donor Fatema accepted the request"
    )
    
    accepted_donor: Optional[str] = Field(
        None,
        description="Name of the donor who accepted",
        example="Fatema"
    )
    
    attempts: int = Field(
        default=0,
        description="Number of donors contacted",
        example=2
    )
    
    declined_donors: List[str] = Field(
        default_factory=list,
        description="Names of donors who declined",
        example=["Rahim", "Karim"]
    )
    
    workflow_time: float = Field(
        default=0.0,
        description="Total time taken in seconds",
        example=1.23
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the communication completed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Donor Fatema accepted the request",
                "accepted_donor": "Fatema",
                "attempts": 2,
                "declined_donors": ["Rahim"],
                "workflow_time": 1.23,
                "timestamp": "2026-07-04T10:30:00"
            }
        }

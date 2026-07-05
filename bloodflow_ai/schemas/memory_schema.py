"""
Memory Schema

Pydantic model for donor memory tracking.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DonorMemory(BaseModel):
    """
    Memory record for a single donor.
    
    Tracks:
    - When they were last contacted
    - Their response (accepted, declined, ignored)
    - When they are eligible to be contacted again
    - Which workflow triggered the contact
    """
    
    donor_id: int = Field(..., description="Unique donor ID")
    
    last_contacted: Optional[datetime] = Field(
        None,
        description="Timestamp of last contact"
    )
    
    accepted: bool = Field(
        default=False,
        description="Did the donor accept?"
    )
    
    declined: bool = Field(
        default=False,
        description="Did the donor decline?"
    )
    
    ignored: bool = Field(
        default=False,
        description="Did the donor ignore the request?"
    )
    
    cooldown_until: Optional[datetime] = Field(
        None,
        description="Donor cannot be contacted until this time"
    )
    
    workflow_id: Optional[str] = Field(
        None,
        description="ID of the workflow that contacted the donor"
    )
    
    last_response: Optional[str] = Field(
        None,
        description="Raw response string for debugging"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "donor_id": 1,
                "last_contacted": "2026-07-04T10:30:00",
                "accepted": True,
                "declined": False,
                "ignored": False,
                "cooldown_until": "2026-07-04T11:30:00",
                "workflow_id": "wf_001",
                "last_response": "accepted"
            }
        }

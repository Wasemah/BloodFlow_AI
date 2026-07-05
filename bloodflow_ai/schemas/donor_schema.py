"""
Donor Schema

Pydantic model for blood donors.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Donor(BaseModel):
    """Structured donor information."""
    
    id: int = Field(..., description="Unique donor ID", example=1)
    name: str = Field(..., description="Donor's full name", example="Rahim")
    blood_group: str = Field(..., description="Blood group", example="O-")
    age: int = Field(..., description="Donor's age", ge=18, le=65, example=25)
    location: str = Field(..., description="City or area", example="Dhaka")
    phone: str = Field(..., description="Contact number", example="01712345678")
    last_donation: Optional[str] = Field(None, description="Last donation date")
    available: bool = Field(default=True, description="Currently available to donate")
    response_rate: float = Field(default=0.5, description="Historical response rate (0-1)")
    preferred_time: str = Field(default="Any", description="Preferred contact time")
    status: str = Field(default="Active", description="Active, Inactive, Blacklisted")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Rahim",
                "blood_group": "O-",
                "age": 25,
                "location": "Dhaka",
                "phone": "01712345678",
                "last_donation": "2026-01-15",
                "available": True,
                "response_rate": 0.8,
                "preferred_time": "Evening",
                "status": "Active"
            }
        }

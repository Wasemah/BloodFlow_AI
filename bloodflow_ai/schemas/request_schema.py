"""
Request Schema

Pydantic model for hospital blood requests.
"""

from pydantic import BaseModel, Field
from typing import Optional


class HospitalRequest(BaseModel):
    """Structured request from a hospital for blood donation."""
    
    blood_group: str = Field(
        ...,
        description="Blood group requested (e.g., O-, A+, B-)",
        example="O-"
    )
    
    hospital: str = Field(
        ...,
        description="Name of the requesting hospital",
        example="Square Hospital"
    )
    
    urgency: str = Field(
        default="Normal",
        description="Urgency level: Critical, High, Normal",
        example="Critical"
    )
    
    deadline: str = Field(
        default="As soon as possible",
        description="Time by which blood is needed",
        example="8 PM"
    )
    
    units: int = Field(
        default=1,
        description="Number of blood units requested",
        ge=1,
        le=10,
        example=1
    )
    
    raw_input: str = Field(
        ...,
        description="Original raw text from hospital",
        example="Need O- blood at Square Hospital before 8 PM"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "blood_group": "O-",
                "hospital": "Square Hospital",
                "urgency": "Critical",
                "deadline": "8 PM",
                "units": 1,
                "raw_input": "Need O- blood at Square Hospital before 8 PM"
            }
        }

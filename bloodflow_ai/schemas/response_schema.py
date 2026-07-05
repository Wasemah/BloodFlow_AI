"""
Response Schema

Pydantic model for workflow responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class WorkflowResponse(BaseModel):
    """Final response from the orchestration workflow."""
    
    status: str = Field(..., description="Success or failure")
    message: str = Field(..., description="Human-readable message")
    donor_contacted: Optional[str] = Field(None, description="Name of contacted donor")
    request: Optional[Dict[str, Any]] = Field(None, description="Original request details")
    donors_considered: int = Field(default=0, description="Number of donors evaluated")
    
    # Phase 10: Metrics
    workflow_id: Optional[str] = Field(None, description="Unique workflow identifier")
    total_duration: float = Field(default=0.0, description="Total workflow duration in seconds")
    attempts: int = Field(default=0, description="Total attempts made")
    
    # Phase 12: Explainability
    explanation: Optional[Dict[str, Any]] = Field(None, description="AI decision explanation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Donor notified successfully",
                "donor_contacted": "Rahim",
                "request": {"blood_group": "O-", "hospital": "Square Hospital"},
                "donors_considered": 5,
                "workflow_id": "wf_20260704_143000_12345",
                "total_duration": 5.23,
                "attempts": 2,
                "explanation": {
                    "donor": "Rahim",
                    "reasoning": "Rahim was selected because...",
                    "breakdown": {"Blood Compatibility": 40, "Availability": 20}
                }
            }
        }
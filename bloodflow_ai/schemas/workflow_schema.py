"""
Workflow Schema

Pydantic models for workflow tracking and metrics.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class WorkflowMetrics(BaseModel):
    """Detailed metrics for a workflow execution."""
    
    # Timing metrics
    total_duration_ms: float = Field(default=0.0)
    triage_duration_ms: float = Field(default=0.0)
    matching_duration_ms: float = Field(default=0.0)
    communication_duration_ms: float = Field(default=0.0)
    
    # Matching metrics
    donors_compatible: int = Field(default=0)
    donors_eligible: int = Field(default=0)
    donors_ranked: int = Field(default=0)
    donors_considered: int = Field(default=0)
    
    # Communication metrics
    attempts: int = Field(default=0)
    donors_declined: List[str] = Field(default_factory=list)
    donor_accepted: Optional[str] = Field(None)
    
    # Performance metrics
    acceptance_rate: float = Field(default=0.0)
    retry_count: int = Field(default=0)
    
    # Workflow metadata
    workflow_id: str = Field(...)
    status: str = Field(default="running")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None)


class WorkflowContext(BaseModel):
    """Context and metrics for a single workflow execution."""
    
    workflow_id: str = Field(..., description="Unique workflow identifier")
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = Field(None)
    
    # Timing metrics (in seconds)
    total_duration: float = Field(default=0.0)
    triage_duration: float = Field(default=0.0)
    matching_duration: float = Field(default=0.0)
    communication_duration: float = Field(default=0.0)
    
    # Agent results
    triage_result: Optional[dict] = Field(None)
    matching_result: Optional[dict] = Field(None)
    communication_result: Optional[dict] = Field(None)
    
    # Communication metrics
    donors_contacted: int = Field(default=0)
    donors_declined: List[str] = Field(default_factory=list)
    donor_accepted: Optional[str] = Field(None)
    attempts: int = Field(default=0)
    
    # Status
    status: str = Field(default="running")
    error: Optional[str] = Field(None)
    
    # Input
    raw_input: str = Field(default="")
    
    # Enhanced metrics
    metrics: Optional[WorkflowMetrics] = Field(None)
    
    def to_metrics(self) -> WorkflowMetrics:
        """Convert to WorkflowMetrics."""
        return WorkflowMetrics(
            total_duration_ms=self.total_duration * 1000,
            triage_duration_ms=self.triage_duration * 1000,
            matching_duration_ms=self.matching_duration * 1000,
            communication_duration_ms=self.communication_duration * 1000,
            donors_compatible=self.matching_result.get("compatible", 0) if self.matching_result else 0,
            donors_eligible=self.matching_result.get("eligible", 0) if self.matching_result else 0,
            donors_ranked=self.matching_result.get("ranked", 0) if self.matching_result else 0,
            donors_considered=self.donors_contacted,
            attempts=self.attempts,
            donors_declined=self.donors_declined,
            donor_accepted=self.donor_accepted,
            acceptance_rate=(1 / max(1, self.attempts)) if self.donor_accepted else 0.0,
            retry_count=0,
            workflow_id=self.workflow_id,
            status=self.status,
            started_at=self.start_time,
            completed_at=self.end_time
        )
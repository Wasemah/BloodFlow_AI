"""
Workflow State

Represents live workflow progress for the frontend.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class WorkflowStage:
    """A single stage in the workflow."""
    
    name: str
    status: str  # pending, active, completed, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration": self.duration,
            "details": self.details
        }


@dataclass
class WorkflowState:
    """Complete workflow state for frontend."""
    
    workflow_id: str
    status: str  # pending, running, completed, failed
    current_stage: Optional[str] = None
    completed_stages: List[WorkflowStage] = field(default_factory=list)
    remaining_stages: List[str] = field(default_factory=list)
    progress: float = 0.0  # 0.0 to 1.0
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "status": self.status,
            "current_stage": self.current_stage,
            "completed_stages": [s.to_dict() for s in self.completed_stages],
            "remaining_stages": self.remaining_stages,
            "progress": self.progress,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }


class WorkflowStateManager:
    """
    Manages workflow state for frontend consumption.
    
    Receives workflow events and builds a live state object.
    """
    
    # Stage order for workflow
    STAGES = [
        "Emergency Triage",
        "Donor Matching",
        "Memory Check",
        "Communication",
        "Workflow Complete"
    ]
    
    def __init__(self):
        self._states: Dict[str, WorkflowState] = {}
        self._event_bus = None
    
    def set_event_bus(self, event_bus) -> None:
        """Set the event bus and subscribe to events."""
        self._event_bus = event_bus
        self._event_bus.subscribe_all(self._on_event)
        print("[WorkflowState] ✅ Subscribed to event bus")
    
    def _on_event(self, event: Dict[str, Any]) -> None:
        """Handle incoming events."""
        workflow_id = event.get("workflow_id")
        if not workflow_id:
            return
        
        event_type = event.get("event_type", "")
        data = event.get("data", {})
        timestamp = event.get("timestamp")
        
        # Initialize state if not exists
        if workflow_id not in self._states:
            self._states[workflow_id] = WorkflowState(
                workflow_id=workflow_id,
                status="running",
                started_at=timestamp,
                updated_at=timestamp,
                remaining_stages=self.STAGES.copy()
            )
        
        state = self._states[workflow_id]
        state.updated_at = timestamp
        
        # Handle specific events
        if event_type == "WorkflowStarted":
            state.current_stage = "Emergency Triage"
            state.progress = 0.1
            state.metadata["input"] = data.get("input", "")
        
        elif event_type == "TriageCompleted":
            stage = WorkflowStage(
                name="Emergency Triage",
                status="completed",
                completed_at=timestamp,
                details={"blood_group": data.get("blood_group")}
            )
            state.completed_stages.append(stage)
            state.current_stage = "Donor Matching"
            state.progress = 0.3
            if "Emergency Triage" in state.remaining_stages:
                state.remaining_stages.remove("Emergency Triage")
        
        elif event_type == "MatchingCompleted":
            stage = WorkflowStage(
                name="Donor Matching",
                status="completed",
                completed_at=timestamp,
                details={"donors_found": data.get("donors_found", 0)}
            )
            state.completed_stages.append(stage)
            state.current_stage = "Memory Check"
            state.progress = 0.5
            if "Donor Matching" in state.remaining_stages:
                state.remaining_stages.remove("Donor Matching")
        
        elif event_type == "MemoryCheckCompleted":
            stage = WorkflowStage(
                name="Memory Check",
                status="completed",
                completed_at=timestamp
            )
            state.completed_stages.append(stage)
            state.current_stage = "Communication"
            state.progress = 0.7
            if "Memory Check" in state.remaining_stages:
                state.remaining_stages.remove("Memory Check")
        
        elif event_type == "CommunicationStarted":
            if "Communication" in state.remaining_stages:
                state.remaining_stages.remove("Communication")
        
        elif event_type == "WorkflowCompleted":
            stage = WorkflowStage(
                name="Workflow Complete",
                status="completed",
                completed_at=timestamp,
                details={"donor": data.get("donor", "None")}
            )
            state.completed_stages.append(stage)
            state.current_stage = None
            state.progress = 1.0
            state.status = "completed"
            if "Workflow Complete" in state.remaining_stages:
                state.remaining_stages.remove("Workflow Complete")
            state.metadata["outcome"] = data.get("status", "unknown")
            state.metadata["donor"] = data.get("donor", "None")
        
        elif event_type == "WorkflowFailed":
            state.status = "failed"
            state.metadata["error"] = data.get("error", "Unknown error")
            state.progress = state.progress  # Keep current progress
    
    def get_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow state as dictionary."""
        state = self._states.get(workflow_id)
        if state:
            return state.to_dict()
        return None
    
    def get_current_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current stage and progress for a workflow."""
        state = self._states.get(workflow_id)
        if state:
            return {
                "workflow_id": workflow_id,
                "status": state.status,
                "current_stage": state.current_stage,
                "progress": state.progress,
                "updated_at": state.updated_at
            }
        return None
    
    def list_workflows(self) -> List[str]:
        """List all workflow IDs."""
        return list(self._states.keys())
    
    def clear(self) -> None:
        """Clear all states."""
        self._states.clear()
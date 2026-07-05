"""
Workflow Context

Manages workflow state, timing, and metrics.
"""

import time
from typing import Optional, List, Any
from datetime import datetime
from bloodflow_ai.schemas.workflow_schema import WorkflowContext


class WorkflowContextManager:
    """Manages workflow state and collects metrics."""
    
    def __init__(self, workflow_id: str, raw_input: str = ""):
        self.context = WorkflowContext(
            workflow_id=workflow_id,
            raw_input=raw_input
        )
        self._timers = {}
    
    def start_timer(self, name: str) -> None:
        """Start a timer for a specific phase."""
        self._timers[name] = time.time()
    
    def stop_timer(self, name: str) -> float:
        """Stop a timer and record the duration."""
        if name in self._timers:
            duration = time.time() - self._timers[name]
            setattr(self.context, f"{name}_duration", duration)
            del self._timers[name]
            return duration
        return 0.0
    
    def complete(self, status: str = "success", error: str = None) -> None:
        """Mark the workflow as complete."""
        self.context.end_time = datetime.now()
        self.context.total_duration = (self.context.end_time - self.context.start_time).total_seconds()
        self.context.status = status
        if error:
            self.context.error = error
    
    def get_context(self) -> WorkflowContext:
        """Get the current workflow context."""
        return self.context
    
    def log_event(self, agent: str, event: str, details: str = "") -> None:
        """Log a workflow event."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{agent}] {event}")
        if details:
            print(f"   → {details}")
    
    def __repr__(self) -> str:
        return f"<WorkflowContextManager: {self.context.workflow_id}>"

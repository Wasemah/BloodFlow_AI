"""
Timeline Builder

Transforms workflow events into chronological execution history.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class TimelineBuilder:
    """
    Builds a chronological timeline from workflow events.
    
    Consumes events from the EventBus and structures them for display.
    """
    
    def __init__(self):
        self._timelines: Dict[str, List[Dict[str, Any]]] = {}
    
    def add_event(self, event: Dict[str, Any]) -> None:
        """
        Add an event to the timeline.
        
        Args:
            event: Event dict from EventBus
        """
        workflow_id = event.get("workflow_id")
        if not workflow_id:
            return
        
        if workflow_id not in self._timelines:
            self._timelines[workflow_id] = []
        
        # Format for display
        timeline_event = {
            "id": event.get("id"),
            "event_type": event.get("event_type"),
            "timestamp": event.get("timestamp"),
            "time": self._format_time(event.get("timestamp")),
            "agent": event.get("data", {}).get("agent", "Unknown"),
            "status": event.get("data", {}).get("status", "Unknown"),
            "details": event.get("data", {}).get("details", ""),
            "duration": event.get("data", {}).get("duration", 0),
            "metadata": event.get("data", {})
        }
        
        self._timelines[workflow_id].append(timeline_event)
    
    def get_timeline(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get the full timeline for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Chronological list of events
        """
        return self._timelines.get(workflow_id, [])
    
    def get_summary(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get a summary of the timeline.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Dict with start, end, duration, and event count
        """
        timeline = self.get_timeline(workflow_id)
        if not timeline:
            return {
                "workflow_id": workflow_id,
                "event_count": 0,
                "start_time": None,
                "end_time": None,
                "duration": 0
            }
        
        start = timeline[0]["timestamp"]
        end = timeline[-1]["timestamp"]
        
        return {
            "workflow_id": workflow_id,
            "event_count": len(timeline),
            "start_time": start,
            "end_time": end,
            "duration": self._calculate_duration(start, end)
        }
    
    def _format_time(self, timestamp: Optional[str]) -> str:
        """Format timestamp for display."""
        if not timestamp:
            return ""
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%H:%M:%S")
        except:
            return timestamp
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration in seconds."""
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            return (end_dt - start_dt).total_seconds()
        except:
            return 0.0
    
    def clear(self) -> None:
        """Clear all timelines."""
        self._timelines.clear()
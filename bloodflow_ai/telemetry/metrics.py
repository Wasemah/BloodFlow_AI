"""
Metrics Engine

Calculates workflow performance metrics from events.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class MetricsEngine:
    """
    Calculates workflow metrics from event data.
    
    Metrics:
    - Total duration
    - Agent latencies
    - Matching time
    - Communication time
    - Memory lookup time
    - Donors considered
    - Retries
    - Acceptance rate
    """
    
    def __init__(self):
        self._metrics: Dict[str, Dict[str, Any]] = {}
    
    def process_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a list of events and calculate metrics.
        
        Args:
            events: List of events for a workflow
            
        Returns:
            Dict of metrics
        """
        if not events:
            return {}
        
        workflow_id = events[0].get("workflow_id", "unknown")
        
        metrics = {
            "workflow_id": workflow_id,
            "total_duration": 0.0,
            "agent_latencies": {},
            "matching_time": 0.0,
            "communication_time": 0.0,
            "memory_lookup_time": 0.0,
            "donors_considered": 0,
            "retries": 0,
            "acceptance_rate": 0.0,
            "event_count": len(events)
        }
        
        # Track agent durations
        agent_start_times: Dict[str, str] = {}
        agent_durations: Dict[str, float] = {}
        
        for event in events:
            event_type = event.get("event_type", "")
            data = event.get("data", {})
            
            # Track agent start/end times
            if event_type.endswith("Started"):
                agent = data.get("agent", "Unknown")
                agent_start_times[agent] = event.get("timestamp", "")
            
            elif event_type.endswith("Completed") or event_type.endswith("Finished"):
                agent = data.get("agent", "Unknown")
                start_time = agent_start_times.get(agent)
                if start_time:
                    try:
                        start_dt = datetime.fromisoformat(start_time)
                        end_dt = datetime.fromisoformat(event.get("timestamp", ""))
                        duration = (end_dt - start_dt).total_seconds()
                        agent_durations[agent] = duration
                    except:
                        pass
            
            # Specific metrics
            if event_type == "MatchingCompleted":
                metrics["matching_time"] = data.get("duration", 0.0)
                metrics["donors_considered"] = data.get("donors_ranked", 0)
            
            elif event_type == "CommunicationCompleted":
                metrics["communication_time"] = data.get("duration", 0.0)
                metrics["acceptance_rate"] = data.get("acceptance_rate", 0.0)
            
            elif event_type == "MemoryLookup":
                metrics["memory_lookup_time"] += data.get("duration", 0.0)
            
            elif event_type == "CommunicationAttempt":
                if data.get("status") == "declined" or data.get("status") == "no_response":
                    metrics["retries"] += 1
        
        metrics["agent_latencies"] = agent_durations
        
        # Calculate total duration from first to last event
        try:
            first = datetime.fromisoformat(events[0].get("timestamp", ""))
            last = datetime.fromisoformat(events[-1].get("timestamp", ""))
            metrics["total_duration"] = (last - first).total_seconds()
        except:
            pass
        
        self._metrics[workflow_id] = metrics
        return metrics
    
    def get_metrics(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific workflow."""
        return self._metrics.get(workflow_id)
    
    def clear(self) -> None:
        """Clear all metrics."""
        self._metrics.clear()
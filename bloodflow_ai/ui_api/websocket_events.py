"""
WebSocket Events

Provides real-time frontend updates via events.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime


class WebSocketEvents:
    """
    Broadcasts events for real-time frontend updates.
    
    Creates the "live AI" feeling:
    - Thinking...
    - Matching...
    - Found donors...
    - Contacting...
    - Accepted...
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._listeners: List[Callable] = []
        self._initialized = True
        self._event_bus = None
    
    def set_event_bus(self, event_bus) -> None:
        """Set the event bus and subscribe."""
        self._event_bus = event_bus
        self._event_bus.subscribe_all(self._on_event)
        print("[WebSocketEvents] ✅ Subscribed to event bus")
    
    def add_listener(self, callback: Callable) -> None:
        """Add a listener for WebSocket events."""
        self._listeners.append(callback)
    
    def _on_event(self, event: Dict[str, Any]) -> None:
        """Handle events and broadcast to listeners."""
        # Transform event to frontend-friendly format
        ws_event = self._transform_event(event)
        if ws_event:
            self._broadcast(ws_event)
    
    def _transform_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform backend event to frontend WebSocket event."""
        event_type = event.get("event_type", "")
        data = event.get("data", {})
        timestamp = event.get("timestamp", datetime.now().isoformat())
        workflow_id = event.get("workflow_id", "")
        
        # Map backend events to frontend messages
        frontend_map = {
            "WorkflowStarted": {"type": "thinking", "message": "🤔 Analyzing emergency request..."},
            "TriageCompleted": {"type": "triage", "message": "✅ Emergency triage complete"},
            "MatchingStarted": {"type": "matching", "message": "🔍 Searching for eligible donors..."},
            "MatchingCompleted": {"type": "found_donors", "message": f"✅ Found {data.get('donors_found', 0)} potential donors"},
            "CommunicationStarted": {"type": "contacting", "message": "📞 Contacting donors..."},
            "CommunicationAccepted": {"type": "accepted", "message": f"✅ {data.get('donor', 'Donor')} accepted!"},
            "CommunicationFailed": {"type": "failed", "message": "❌ No donor accepted"},
            "WorkflowCompleted": {"type": "completed", "message": "✅ Workflow completed successfully"},
            "WorkflowFailed": {"type": "failed", "message": f"❌ Workflow failed: {data.get('error', 'Unknown error')}"}
        }
        
        # Find mapping
        mapping = frontend_map.get(event_type)
        if not mapping:
            return None
        
        return {
            "workflow_id": workflow_id,
            "type": mapping["type"],
            "message": mapping["message"],
            "data": data,
            "timestamp": timestamp
        }
    
    def _broadcast(self, event: Dict[str, Any]) -> None:
        """Broadcast event to all listeners."""
        for listener in self._listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"[WebSocketEvents] ⚠️ Error in listener: {e}")
    
    def clear(self) -> None:
        """Clear all listeners."""
        self._listeners.clear()


# Singleton instance
_ws_events: Optional[WebSocketEvents] = None


def get_websocket_events() -> WebSocketEvents:
    """Get the global WebSocketEvents singleton."""
    global _ws_events
    if _ws_events is None:
        _ws_events = WebSocketEvents()
    return _ws_events
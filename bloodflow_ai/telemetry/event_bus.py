"""
Event Bus — Publish-Subscribe Communication Backbone

Enables agents to publish workflow events without knowing who will consume them.
"""

from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import uuid
import json
from collections import defaultdict


class EventBus:
    """
    Publish-Subscribe event bus for workflow telemetry.
    
    Features:
    - Register subscribers for specific event types
    - Publish events with workflow_id
    - Broadcast to all registered listeners
    - Maintain event ordering
    - Thread-safe (for future async support)
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
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._all_events: List[Dict[str, Any]] = []
        self._initialized = True
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Register a callback for a specific event type.
        
        Args:
            event_type: Type of event to subscribe to (e.g., "MatchingCompleted")
            callback: Function to call when event is published
        """
        if not callable(callback):
            raise ValueError("Callback must be callable")
        self._subscribers[event_type].append(callback)
        print(f"[EventBus] ✅ Subscriber registered for: {event_type}")
    
    def subscribe_all(self, callback: Callable) -> None:
        """
        Register a callback for all events.
        
        Args:
            callback: Function to call for every event
        """
        self.subscribe("*", callback)
    
    def publish(self, event_type: str, workflow_id: str, data: Dict[str, Any]) -> None:
        """
        Publish an event to all registered subscribers.
        
        Args:
            event_type: Type of event (e.g., "MatchingCompleted")
            workflow_id: Unique workflow identifier
            data: Event metadata (agent, duration, donors, etc.)
        """
        event = {
            "event_type": event_type,
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "id": str(uuid.uuid4())[:8]
        }
        
        # Store event history
        self._all_events.append(event)
        
        # Broadcast to specific subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"[EventBus] ⚠️ Error in subscriber: {e}")
        
        # Broadcast to wildcard subscribers
        if "*" in self._subscribers:
            for callback in self._subscribers["*"]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"[EventBus] ⚠️ Error in wildcard subscriber: {e}")
    
    def get_events(self, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all events, optionally filtered by workflow_id.
        
        Args:
            workflow_id: Optional workflow ID to filter by
            
        Returns:
            List of events
        """
        if workflow_id:
            return [e for e in self._all_events if e["workflow_id"] == workflow_id]
        return self._all_events.copy()
    
    def clear(self) -> None:
        """Clear all stored events (useful for testing)."""
        self._all_events.clear()


# Singleton instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global EventBus singleton."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
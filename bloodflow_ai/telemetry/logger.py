"""
Telemetry Logger

Centralized structured logging for workflow events.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path


class TelemetryLogger:
    """
    Structured logger for workflow telemetry.
    
    Replaces scattered print statements with standardized logs.
    """
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file
        self._logs: List[Dict[str, Any]] = []
    
    def log(
        self,
        agent: str,
        event: str,
        workflow_id: str,
        status: str = "info",
        details: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        duration: Optional[float] = None
    ) -> None:
        """
        Log a structured event.
        
        Args:
            agent: Agent name
            event: Event name (e.g., "START", "COMPLETE", "ERROR")
            workflow_id: Workflow ID
            status: Log level (info, warning, error, success)
            details: Human-readable details
            metadata: Additional structured data
            duration: Duration in seconds
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "event": event,
            "workflow_id": workflow_id,
            "status": status,
            "details": details,
            "metadata": metadata or {},
            "duration": duration
        }
        
        self._logs.append(log_entry)
        
        # Also print to console with formatting
        self._print_log(log_entry)
        
        # Write to file if configured
        if self.log_file:
            self._write_to_file(log_entry)
    
    def _print_log(self, log_entry: Dict[str, Any]) -> None:
        """Print a formatted log entry to console."""
        timestamp = datetime.fromisoformat(log_entry["timestamp"]).strftime("%H:%M:%S")
        status_icon = self._get_status_icon(log_entry["status"])
        agent = log_entry["agent"]
        event = log_entry["event"]
        details = log_entry["details"]
        
        if details:
            print(f"[{timestamp}] [{agent}] {status_icon} {event}: {details}")
        else:
            print(f"[{timestamp}] [{agent}] {status_icon} {event}")
        
        if log_entry["duration"] is not None:
            print(f"   ⏱️  Duration: {log_entry['duration']:.3f}s")
    
    def _get_status_icon(self, status: str) -> str:
        """Get emoji icon for status."""
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "start": "🚀",
            "complete": "✅",
            "failed": "❌"
        }
        return icons.get(status.lower(), "ℹ️")
    
    def _write_to_file(self, log_entry: Dict[str, Any]) -> None:
        """Write log entry to file."""
        if not self.log_file:
            return
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"[Logger] ⚠️ Error writing to log file: {e}")
    
    def get_logs(
        self,
        workflow_id: Optional[str] = None,
        agent: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get logs, optionally filtered.
        
        Args:
            workflow_id: Filter by workflow ID
            agent: Filter by agent
            limit: Maximum number of logs to return
            
        Returns:
            List of log entries
        """
        logs = self._logs
        
        if workflow_id:
            logs = [l for l in logs if l["workflow_id"] == workflow_id]
        
        if agent:
            logs = [l for l in logs if l["agent"] == agent]
        
        if limit:
            logs = logs[-limit:]
        
        return logs
    
    def clear(self) -> None:
        """Clear all logs."""
        self._logs.clear()
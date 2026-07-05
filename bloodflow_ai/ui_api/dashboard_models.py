"""
Dashboard Models

UI-friendly data models for the frontend.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class DashboardCard:
    """A card for the dashboard."""
    
    id: str
    title: str
    value: str
    icon: str = ""
    color: str = "blue"
    change: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "value": self.value,
            "icon": self.icon,
            "color": self.color,
            "change": self.change
        }


@dataclass
class TimelineItem:
    """An item in the workflow timeline."""
    
    time: str
    event: str
    agent: str
    status: str  # success, warning, error, info
    details: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "event": self.event,
            "agent": self.agent,
            "status": self.status,
            "details": self.details
        }


@dataclass
class MetricCard:
    """A metric displayed on the dashboard."""
    
    name: str
    value: float
    unit: str = ""
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "description": self.description
        }


@dataclass
class ProgressNode:
    """A node in the workflow progress."""
    
    id: str
    label: str
    status: str  # pending, active, completed, failed
    order: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "status": self.status,
            "order": self.order
        }


@dataclass
class DashboardModel:
    """Complete dashboard model for frontend."""
    
    workflow_id: str
    status: str
    cards: List[DashboardCard]
    timeline: List[TimelineItem]
    metrics: List[MetricCard]
    progress: List[ProgressNode]
    reasoning: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "status": self.status,
            "cards": [c.to_dict() for c in self.cards],
            "timeline": [t.to_dict() for t in self.timeline],
            "metrics": [m.to_dict() for m in self.metrics],
            "progress": [p.to_dict() for p in self.progress],
            "reasoning": self.reasoning
        }


class DashboardModelBuilder:
    """
    Builds UI-friendly dashboard models from backend data.
    """
    
    @staticmethod
    def build(
        workflow_id: str,
        state: Dict[str, Any],
        result: Any,
        timeline: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        reasoning: Optional[str] = None,
        explanation: Optional[Dict[str, Any]] = None
    ) -> DashboardModel:
        """
        Build a dashboard model from backend data.
        
        Args:
            workflow_id: Workflow ID
            state: Workflow state dict
            result: Workflow response
            timeline: Timeline events
            metrics: Metrics data
            reasoning: Natural language reasoning
            explanation: Decision explanation
            
        Returns:
            DashboardModel
        """
        status = result.status if hasattr(result, 'status') else "unknown"
        
        # Build cards
        cards = [
            DashboardCard(
                id="status",
                title="Status",
                value="✅ Success" if status == "success" else "❌ Failed",
                icon="🩸",
                color="green" if status == "success" else "red"
            ),
            DashboardCard(
                id="duration",
                title="Duration",
                value=f"{getattr(result, 'total_duration', 0):.3f}s",
                icon="⏱️",
                color="blue"
            ),
            DashboardCard(
                id="donor",
                title="Donor",
                value=getattr(result, 'donor_contacted', "None"),
                icon="👤",
                color="blue"
            ),
            DashboardCard(
                id="attempts",
                title="Attempts",
                value=str(getattr(result, 'attempts', 0)),
                icon="📞",
                color="blue"
            )
        ]
        
        # Build timeline items
        timeline_items = []
        for event in timeline:
            status_map = {
                "success": "success",
                "failed": "error",
                "completed": "success",
                "accepted": "success",
                "declined": "warning",
                "error": "error"
            }
            
            item_status = status_map.get(event.get("status", ""), "info")
            timeline_items.append(TimelineItem(
                time=event.get("time", ""),
                event=event.get("event_type", ""),
                agent=event.get("agent", "Unknown"),
                status=item_status,
                details=event.get("details", "")
            ))
        
        # Build metrics
        metric_cards = [
            MetricCard(
                name="Duration",
                value=getattr(result, 'total_duration', 0),
                unit="s",
                description="Total workflow time"
            ),
            MetricCard(
                name="Donors Considered",
                value=getattr(result, 'donors_considered', 0),
                unit="",
                description="Donors evaluated"
            ),
            MetricCard(
                name="Attempts",
                value=getattr(result, 'attempts', 0),
                unit="",
                description="Communication attempts"
            ),
            MetricCard(
                name="Acceptance Rate",
                value=1.0 if getattr(result, 'donor_contacted', None) else 0.0,
                unit="%",
                description="Donor acceptance rate"
            )
        ]
        
        # Build progress nodes
        stage_order = [
            ("Emergency Triage", "triage"),
            ("Donor Matching", "matching"),
            ("Memory Check", "memory"),
            ("Communication", "communication"),
            ("Workflow Complete", "complete")
        ]
        
        completed_names = [s.get("name", "") for s in state.get("completed_stages", [])]
        current_stage = state.get("current_stage", "")
        
        progress_nodes = []
        for order, (label, node_id) in enumerate(stage_order):
            if label in completed_names:
                node_status = "completed"
            elif label == current_stage:
                node_status = "active"
            elif "Complete" in label and status == "success":
                node_status = "completed"
            else:
                node_status = "pending"
            
            # Handle workflow complete
            if label == "Workflow Complete" and status == "success":
                node_status = "completed"
            
            progress_nodes.append(ProgressNode(
                id=node_id,
                label=label,
                status=node_status,
                order=order
            ))
        
        # Build final model
        return DashboardModel(
            workflow_id=workflow_id,
            status=status,
            cards=cards,
            timeline=timeline_items,
            metrics=metric_cards,
            progress=progress_nodes,
            reasoning=reasoning or ""
        )
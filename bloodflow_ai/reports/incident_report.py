"""
Incident Report

Aggregates every workflow artifact into one professional report.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict


@dataclass
class ReportEvent:
    """A single event in the workflow timeline."""
    
    time: str
    event: str
    agent: str
    details: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "event": self.event,
            "agent": self.agent,
            "details": self.details
        }


@dataclass
class IncidentReport:
    """
    Complete workflow incident report.
    
    Aggregates:
    - Emergency summary
    - Workflow timeline
    - Selected donor
    - Decision explanation
    - Metrics
    - Confidence
    - WHO references
    - Outcome
    """
    
    # Report metadata
    report_id: str
    generated_at: str
    workflow_id: str
    
    # Emergency summary
    hospital: str
    blood_group: str
    urgency: str
    units: int
    
    # Timeline
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    
    # Selected donor
    donor_name: Optional[str] = None
    donor_blood_group: Optional[str] = None
    donor_location: Optional[str] = None
    donor_score: Optional[float] = None
    
    # Decision explanation
    reasoning: str = ""
    score_breakdown: Dict[str, Any] = field(default_factory=dict)
    
    # Metrics
    total_duration: float = 0.0
    attempts: int = 0
    donors_considered: int = 0
    acceptance_rate: float = 0.0
    
    # Confidence
    confidence_score: float = 0.0
    
    # WHO references
    who_references: List[str] = field(default_factory=list)
    
    # Outcome
    status: str = "failed"
    message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "workflow_id": self.workflow_id,
            "emergency_summary": {
                "hospital": self.hospital,
                "blood_group": self.blood_group,
                "urgency": self.urgency,
                "units": self.units
            },
            "timeline": self.timeline,
            "selected_donor": {
                "name": self.donor_name,
                "blood_group": self.donor_blood_group,
                "location": self.donor_location,
                "score": self.donor_score
            } if self.donor_name else None,
            "reasoning": self.reasoning,
            "score_breakdown": self.score_breakdown,
            "metrics": {
                "total_duration_seconds": self.total_duration,
                "attempts": self.attempts,
                "donors_considered": self.donors_considered,
                "acceptance_rate": self.acceptance_rate
            },
            "confidence_score": self.confidence_score,
            "who_references": self.who_references,
            "outcome": {
                "status": self.status,
                "message": self.message
            }
        }
    
    def to_markdown(self) -> str:
        """Convert report to markdown."""
        lines = [
            "# 🩸 BloodFlow AI — Incident Report\n",
            f"**Report ID:** `{self.report_id}`",
            f"**Generated:** {self.generated_at}",
            f"**Workflow ID:** `{self.workflow_id}`",
            "",
            "---",
            "",
            "## 📋 Emergency Summary",
            "",
            f"| Field | Value |",
            f"| :--- | :--- |",
            f"| Hospital | {self.hospital} |",
            f"| Blood Group | {self.blood_group} |",
            f"| Urgency | {self.urgency} |",
            f"| Units | {self.units} |",
            "",
            "---",
            "",
            "## ⏱️ Workflow Timeline",
            "",
            "| Time | Event | Agent | Details |",
            "| :--- | :--- | :--- | :--- |",
        ]
        
        for event in self.timeline:
            lines.append(f"| {event.get('time', '')} | {event.get('event', '')} | {event.get('agent', '')} | {event.get('details', '')} |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 🧠 Selected Donor",
            "",
            f"| Field | Value |",
            f"| :--- | :--- |",
        ])
        
        if self.donor_name:
            lines.extend([
                f"| Name | {self.donor_name} |",
                f"| Blood Group | {self.donor_blood_group or 'N/A'} |",
                f"| Location | {self.donor_location or 'N/A'} |",
                f"| Score | {self.donor_score or 0:.1f} |",
            ])
        else:
            lines.append("| Status | No donor selected |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 📊 Decision Explanation",
            "",
            f"{self.reasoning}",
            "",
            "### Score Breakdown",
            "",
            "| Component | Score |",
            "| :--- | :--- |",
        ])
        
        for component, score in self.score_breakdown.get("components", {}).items():
            lines.append(f"| {component} | {score:.1f} |")
        
        lines.extend([
            "",
            f"**Total Score:** {self.score_breakdown.get('total', 0):.1f}",
            "",
            "---",
            "",
            "## 📈 Metrics",
            "",
            f"| Metric | Value |",
            f"| :--- | :--- |",
            f"| Total Duration | {self.total_duration:.3f}s |",
            f"| Attempts | {self.attempts} |",
            f"| Donors Considered | {self.donors_considered} |",
            f"| Acceptance Rate | {self.acceptance_rate:.1%} |",
            "",
            "---",
            "",
            "## 📊 Confidence",
            "",
            f"**Confidence Score:** {self.confidence_score:.2f}",
            "",
            "---",
            "",
            "## 📚 WHO References",
            "",
        ])
        
        if self.who_references:
            for ref in self.who_references:
                lines.append(f"- {ref}")
        else:
            lines.append("- No WHO references available")
        
        lines.extend([
            "",
            "---",
            "",
            "## ✅ Outcome",
            "",
            f"**Status:** {'✅ Success' if self.status == 'success' else '❌ Failed'}",
            f"**Message:** {self.message}",
        ])
        
        return "\n".join(lines)


class ReportGenerator:
    """
    Generates Incident Reports from workflow artifacts.
    """
    
    def __init__(self):
        self._reports: Dict[str, IncidentReport] = {}
    
    def generate(
        self,
        workflow_id: str,
        result: Any,
        timeline: List[Dict[str, Any]],
        explanation: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        request: Optional[Dict[str, Any]] = None
    ) -> IncidentReport:
        """
        Generate a complete incident report.
        
        Args:
            workflow_id: Workflow ID
            result: Workflow response
            timeline: Timeline events
            explanation: Decision explanation
            metrics: Metrics data
            request: Hospital request
            
        Returns:
            IncidentReport
        """
        # Extract request data
        hospital = "Unknown"
        blood_group = "Unknown"
        urgency = "Normal"
        units = 1
        
        if request:
            hospital = request.get("hospital", "Unknown")
            blood_group = request.get("blood_group", "Unknown")
            urgency = request.get("urgency", "Normal")
            units = request.get("units", 1)
        
        # Extract donor data
        donor_name = getattr(result, 'donor_contacted', None)
        donor_blood_group = None
        donor_location = None
        donor_score = None
        
        if explanation and explanation.get("explanation"):
            expl = explanation["explanation"]
            donor_blood_group = expl.get("blood_group")
            donor_location = "N/A"  # Will be filled from donor object
        
        if explanation and explanation.get("breakdown"):
            donor_score = explanation["breakdown"].get("total", 0)
        
        # Extract metrics
        total_duration = getattr(result, 'total_duration', 0.0)
        attempts = getattr(result, 'attempts', 0)
        donors_considered = getattr(result, 'donors_considered', 0)
        acceptance_rate = 1.0 if donor_name else 0.0
        
        # Extract reasoning
        reasoning = ""
        if explanation and explanation.get("reasoning"):
            reasoning = explanation["reasoning"]
        elif result and hasattr(result, 'message'):
            reasoning = result.message
        
        # Extract WHO references (from RAG if available)
        who_references = []
        # This would be populated from RAG results
        
        # Generate report
        report = IncidentReport(
            report_id=f"RPT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            generated_at=datetime.now().isoformat(),
            workflow_id=workflow_id,
            hospital=hospital,
            blood_group=blood_group,
            urgency=urgency,
            units=units,
            timeline=timeline,
            donor_name=donor_name,
            donor_blood_group=donor_blood_group,
            donor_location=donor_location,
            donor_score=donor_score,
            reasoning=reasoning,
            score_breakdown=explanation.get("breakdown", {}) if explanation else {},
            total_duration=total_duration,
            attempts=attempts,
            donors_considered=donors_considered,
            acceptance_rate=acceptance_rate,
            confidence_score=0.85 if donor_name else 0.0,
            who_references=who_references,
            status=getattr(result, 'status', 'failed'),
            message=getattr(result, 'message', 'Workflow completed')
        )
        
        self._reports[workflow_id] = report
        return report
    
    def get_report(self, workflow_id: str) -> Optional[IncidentReport]:
        """Get a report by workflow ID."""
        return self._reports.get(workflow_id)
    
    def list_reports(self) -> List[str]:
        """List all report IDs."""
        return list(self._reports.keys())